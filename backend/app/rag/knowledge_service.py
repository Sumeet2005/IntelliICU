"""
app/rag/knowledge_service.py

In-memory Clinical Knowledge Service — Phase 12.4: Semantic Retrieval.

Search strategy
---------------
Primary  : Embedding-based cosine similarity (BAAI/bge-small-en-v1.5)
Fallback : TF-IDF-style keyword scoring (used if sentence-transformers
           is unavailable or model loading fails)

The public API is identical to Phase 12.1/12.2:
    load_documents()   – (re)load corpus and rebuild embedding index
    search(query)      – returns top-k documents with score
    get_by_id(id)      – direct lookup
    list_categories()
    count()
"""

from __future__ import annotations

import re
import logging
from typing import List, Optional, Dict

from app.rag.document import ClinicalDocument
from app.rag.sources import ALL_CLINICAL_DOCUMENTS

logger = logging.getLogger(__name__)


class KnowledgeService:
    """
    Singleton-friendly in-memory clinical knowledge service.

    On construction the corpus is loaded and an embedding index is built.
    If sentence-transformers is unavailable the service silently falls back
    to keyword scoring so the application always starts successfully.

    Usage
    -----
        ks = KnowledgeService()
        results = ks.search("norepinephrine dosing in septic shock")
    """

    def __init__(self) -> None:
        self._store:    Dict[str, ClinicalDocument] = {}
        self._embedder = None   # EmbeddingService | None
        self._semantic_ready = False

        self.load_documents()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def load_documents(self, extra: Optional[List[ClinicalDocument]] = None) -> None:
        """
        Load the default corpus plus any caller-supplied extras, then
        (re)build the embedding index.

        Parameters
        ----------
        extra : additional documents to merge (e.g. from tests).
        """
        docs = ALL_CLINICAL_DOCUMENTS + (extra or [])
        self._store = {doc.id: doc for doc in docs}
        logger.info("[KnowledgeService] Loaded %d clinical documents.", len(self._store))
        self._build_embedding_index()

    def search(
        self,
        query: str,
        top_k: int = 3,
        category: Optional[str] = None,
    ) -> List[Dict]:
        """
        Return the top-k most relevant documents for ``query``.

        First queries ChromaDB using pre-computed embeddings.
        If ChromaDB fails or has no documents, automatically falls back
        to the existing in-memory RAG (semantic or keyword).
        """
        if not query:
            return []

        # 1. Hybrid Search Phase: Try ChromaDB first
        try:
            from app.vector_db.chroma_service import chroma_service
            if chroma_service.health_check():
                # We need the query embedding vector
                if self._semantic_ready and self._embedder:
                    from app.rag.embedding_service import _QUERY_PREFIX
                    q_vec = self._embedder._model.encode(
                        _QUERY_PREFIX + query,
                        normalize_embeddings=True,
                        convert_to_numpy=True,
                    ).tolist()

                    where_filter = None
                    if category:
                        where_filter = {"category": category}

                    res = chroma_service.query_documents(
                        query_embeddings=q_vec,
                        n_results=top_k,
                        where=where_filter
                    )

                    # Convert Chroma format to List[Dict] with expected keys
                    docs = []
                    if res and res.get("ids") and len(res["ids"]) > 0 and len(res["ids"][0]) > 0:
                        for i in range(len(res["ids"][0])):
                            doc_id = res["ids"][0][i]
                            distance = res["distances"][0][i] if "distances" in res else 0.0
                            # Convert L2 distance to cosine similarity
                            sim_score = max(0.0, min(1.0, 1.0 - (distance / 2.0)))

                            metadata = res["metadatas"][0][i] if "metadatas" in res else {}
                            content = res["documents"][0][i] if "documents" in res else ""
                            
                            tags_raw = metadata.get("tags", "")
                            tags = tags_raw.split(",") if isinstance(tags_raw, str) and tags_raw else []

                            docs.append({
                                "id": doc_id,
                                "title": metadata.get("title", ""),
                                "source": metadata.get("source", metadata.get("organization", "")),
                                "category": metadata.get("category", ""),
                                "section": metadata.get("section", ""),
                                "content": content,
                                "tags": tags,
                                "score": round(sim_score, 4),
                            })
                        
                        if docs:
                            logger.info("[KnowledgeService] Hybrid search: ChromaDB returned %d results.", len(docs))
                            return docs
        except Exception as e:
            logger.warning("[KnowledgeService] ChromaDB query failed; falling back: %s", e)

        # 2. Fallback Phase: In-memory RAG
        if self._semantic_ready:
            return self._semantic_search(query, top_k, category)
        else:
            return self._keyword_search(query, top_k, category)

    def get_by_id(self, doc_id: str) -> Optional[ClinicalDocument]:
        """Return a single document by id, or None if not found."""
        return self._store.get(doc_id)

    def list_categories(self) -> List[str]:
        """Distinct clinical categories present in the store."""
        return sorted({doc.category for doc in self._store.values()})

    def count(self) -> int:
        """Total number of loaded documents."""
        return len(self._store)

    @property
    def search_mode(self) -> str:
        """'semantic' or 'keyword' — for logging / health checks."""
        return "semantic" if self._semantic_ready else "keyword"

    # ------------------------------------------------------------------
    # Embedding index bootstrap
    # ------------------------------------------------------------------

    def _build_embedding_index(self) -> None:
        """
        Instantiate EmbeddingService and index all documents.
        Gracefully degrades to keyword search on any error.
        """
        try:
            from app.rag.embedding_service import EmbeddingService
            if self._embedder is None:
                self._embedder = EmbeddingService()

            ids   = list(self._store.keys())
            # Embed a rich concatenation of title + section + content
            texts = [
                f"{doc.title}. {doc.section}. {doc.content}"
                for doc in self._store.values()
            ]
            self._embedder.index_documents(ids, texts)
            self._semantic_ready = self._embedder.is_ready
            logger.info(
                "[KnowledgeService] Embedding index ready — %d vectors (model: %s)",
                self._embedder.corpus_size,
                self._embedder.model_name,
            )
        except ImportError:
            logger.warning(
                "[KnowledgeService] sentence-transformers not installed — "
                "falling back to keyword search."
            )
            self._semantic_ready = False
        except Exception as exc:
            logger.warning(
                "[KnowledgeService] Embedding index build failed (%s) — "
                "falling back to keyword search.", exc
            )
            self._semantic_ready = False

    def _infer_intent(self, query: str) -> dict:
        """
        Infer clinical query intent for category and term boosts.
        Returns a dictionary:
            "categories": dict mapping lower-case category names to boost values
            "tags": list of lower-case query words (for exact title/tag matches)
        """
        query_lower = query.lower()
        boosts = {
            "categories": {},
            "tags": [w for w in re.sub(r"[^a-z0-9]", " ", query_lower).split() if len(w) > 2]
        }

        # 1. Drug intent: trigger if drug names or drug-dosing keywords are present
        drug_keywords = ["dose", "dosing", "renal adjustment", "indication", "adverse effect", "side effect", "interaction", "contraindication", "mechanism"]
        drug_names = ["norepinephrine", "vasopressin", "epinephrine", "dobutamine", "meropenem", "piperacillin", "tazobactam", "vancomycin", "furosemide", "drug"]
        if any(k in query_lower for k in drug_keywords) or any(d in query_lower for d in drug_names):
            boosts["categories"]["drug"] = 0.25

        # 2. Sepsis / Shock intent (excluding drug names to prevent dilution)
        sepsis_keywords = ["sepsis", "septic", "shock", "infection", "antibiotic", "lactate", "surviving sepsis", "ssc"]
        if any(k in query_lower for k in sepsis_keywords):
            boosts["categories"]["sepsis"] = 0.08
            boosts["categories"]["shock"] = 0.04

        # 3. AKI / Kidney / Renal / Creatinine / Urine output intent
        aki_keywords = ["aki", "kidney", "renal", "creatinine", "urine", "kdigo", "dialysis", "rrt", "hyperkalemia", "bun", "lasix", "furosemide"]
        if any(k in query_lower for k in aki_keywords):
            boosts["categories"]["aki"] = 0.12
            if "diagnosis" in query_lower or "detect" in query_lower or "stage" in query_lower or "criteria" in query_lower:
                boosts["categories"]["aki"] += 0.05

        # 4. Oxygen Therapy / Respiration / SpO2 / HFNO / NIV intent
        oxygen_keywords = ["oxygen", "spo2", "pao2", "hypoxia", "hyperoxia", "respiratory", "ventilation", "ventilator", "hfno", "niv", "breathing", "cyanosis"]
        if any(k in query_lower for k in oxygen_keywords):
            boosts["categories"]["oxygen therapy"] = 0.12

        return boosts

    # ------------------------------------------------------------------
    # Semantic search
    # ------------------------------------------------------------------

    def _semantic_search(
        self, query: str, top_k: int, category: Optional[str]
    ) -> List[Dict]:
        """Cosine-similarity retrieval via EmbeddingService with query intent boosts."""
        # Retrieve similarity scores for all documents in the corpus
        hits = self._embedder.search(query, top_k=self.count())

        boosts = self._infer_intent(query)
        scored_docs = []

        for doc_id, semantic_score in hits:
            doc = self._store.get(doc_id)
            if doc is None:
                continue
            if category and doc.category.lower() != category.lower():
                continue

            # 1. Category boost
            cat_boost = boosts["categories"].get(doc.category.lower(), 0.0)

            # 2. Title boost: match query terms against document title
            title_lower = doc.title.lower()
            title_matches = sum(1 for term in boosts["tags"] if term in title_lower)
            title_boost = min(title_matches * 0.01, 0.05)

            # 3. Tag boost: match query terms against document tags
            doc_tags_lower = [t.lower() for t in doc.tags]
            tag_matches = sum(1 for term in boosts["tags"] if any(term in tag or tag in term for tag in doc_tags_lower))
            tag_boost = min(tag_matches * 0.01, 0.04)

            # Final hybrid score capped at 1.0
            final_score = min(semantic_score + cat_boost + title_boost + tag_boost, 1.0)

            entry = doc.to_dict()
            entry["score"] = round(final_score, 4)
            scored_docs.append(entry)

        # Re-sort using the boosted scores
        scored_docs.sort(key=lambda x: (-x["score"], x["id"]))
        results = scored_docs[:top_k]

        logger.debug(
            "[KnowledgeService] hybrid search: %r → %d results", query, len(results)
        )
        return results

    # ------------------------------------------------------------------
    # Keyword search (fallback)
    # ------------------------------------------------------------------

    def _keyword_search(
        self, query: str, top_k: int, category: Optional[str]
    ) -> List[Dict]:
        """Weighted keyword scoring over content, title, category, and tags."""
        terms = self._tokenise(query)
        if not terms:
            return []

        scored: List[tuple] = []
        for doc in self._store.values():
            if category and doc.category.lower() != category.lower():
                continue
            score = self._score(doc, terms)
            if score > 0:
                scored.append((score, doc))

        scored.sort(key=lambda t: (-t[0], t[1].id))
        results = []
        for score, doc in scored[:top_k]:
            entry = doc.to_dict()
            entry["score"] = round(score, 4)
            results.append(entry)

        logger.debug(
            "[KnowledgeService] keyword search: %r → %d results", query, len(results)
        )
        return results

    # ------------------------------------------------------------------
    # Keyword helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _tokenise(text: str) -> List[str]:
        raw = re.sub(r"[^a-z0-9\s]", " ", text.lower())
        return list({w for w in raw.split() if len(w) > 2})

    def _score(self, doc: ClinicalDocument, terms: List[str]) -> float:
        score = 0.0
        content_lower  = doc.content.lower()
        title_lower    = doc.title.lower()
        tags_lower     = [t.lower() for t in doc.tags]
        category_lower = doc.category.lower()
        content_len    = max(len(content_lower.split()), 1)

        for term in terms:
            tf = content_lower.count(term) / content_len
            score += tf * 1.0
            if term in title_lower:
                score += 1.5
            if term in category_lower:
                score += 3.0
            for tag in tags_lower:
                if term == tag or term in tag.split():
                    score += 2.0
                    break
        return score
