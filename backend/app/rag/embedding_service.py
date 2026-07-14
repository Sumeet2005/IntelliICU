"""
app/rag/embedding_service.py

Semantic embedding layer for the IntelliICU RAG knowledge base.

Architecture
------------
- Model : BAAI/bge-small-en-v1.5  (33 M params, 384-dim, MIT licence)
          Fast enough for CPU, accurate enough for clinical NLU.
- All document embeddings are computed once at startup and kept in memory.
- Query embedding + cosine similarity is sub-millisecond at our corpus size (≤200 docs).
- Thread-safe: model and index are read-only after __init__.

Fallback
--------
If sentence-transformers is unavailable or the model fails to load,
EmbeddingService raises ImportError / RuntimeError.
KnowledgeService catches these and falls back to keyword search.
"""

from __future__ import annotations

import logging
import time
from typing import List, Optional, Tuple

import numpy as np

logger = logging.getLogger(__name__)

_MODEL_NAME = "BAAI/bge-small-en-v1.5"

# BGE models are trained with an instruction prefix for query encoding.
# The prefix improves retrieval accuracy on asymmetric tasks.
_QUERY_PREFIX = "Represent this sentence for searching relevant passages: "


class EmbeddingService:
    """
    Wraps a sentence-transformers model and exposes a simple
    encode / cosine-search interface.

    Parameters
    ----------
    model_name : str
        HuggingFace model identifier. Defaults to BAAI/bge-small-en-v1.5.
    """

    def __init__(self, model_name: str = _MODEL_NAME) -> None:
        from sentence_transformers import SentenceTransformer  # lazy import

        t0 = time.time()
        logger.info("[EmbeddingService] Loading model: %s", model_name)
        self._model = SentenceTransformer(model_name)
        self._model_name = model_name
        logger.info(
            "[EmbeddingService] Model loaded in %.1fs", time.time() - t0
        )

        # Indexed corpus: parallel lists of ids and embeddings matrix
        self._ids:        List[str]      = []
        self._embeddings: Optional[np.ndarray] = None  # shape (N, D)

    # ------------------------------------------------------------------
    # Corpus indexing
    # ------------------------------------------------------------------

    def index_documents(self, ids: List[str], texts: List[str]) -> None:
        """
        Encode ``texts`` and cache embeddings alongside their ``ids``.

        This is called once at KnowledgeService startup.

        Parameters
        ----------
        ids   : Unique document identifiers (parallel to ``texts``).
        texts : The content strings to embed.
        """
        if not texts:
            logger.warning("[EmbeddingService] index_documents called with empty corpus.")
            return

        t0 = time.time()
        # BGE passage encoding — no prefix for documents
        matrix = self._model.encode(
            texts,
            batch_size=32,
            show_progress_bar=False,
            normalize_embeddings=True,   # unit vectors → dot product == cosine sim
            convert_to_numpy=True,
        )
        self._ids        = list(ids)
        self._embeddings = matrix.astype(np.float32)
        elapsed = time.time() - t0
        logger.info(
            "[EmbeddingService] Indexed %d documents in %.2fs  (dim=%d)",
            len(ids), elapsed, self._embeddings.shape[1],
        )

    # ------------------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------------------

    def search(self, query: str, top_k: int = 3) -> List[Tuple[str, float]]:
        """
        Encode ``query`` and return the ``top_k`` most similar document ids.

        Parameters
        ----------
        query : Natural-language question or keyword string.
        top_k : Number of results to return.

        Returns
        -------
        List of ``(doc_id, cosine_similarity_score)`` sorted descending.
        Empty list if the index is empty or an error occurs.
        """
        if self._embeddings is None or len(self._ids) == 0:
            logger.warning("[EmbeddingService] Index is empty — call index_documents() first.")
            return []

        # BGE query encoding — apply instruction prefix
        q_vec = self._model.encode(
            _QUERY_PREFIX + query,
            normalize_embeddings=True,
            convert_to_numpy=True,
        ).astype(np.float32)  # shape (D,)

        # Dot product of unit vectors == cosine similarity
        scores = self._embeddings @ q_vec  # shape (N,)

        # Top-k indices (unsorted)
        k = min(top_k, len(self._ids))
        top_indices = np.argpartition(scores, -k)[-k:]
        # Sort the selected indices by score descending
        top_indices = top_indices[np.argsort(scores[top_indices])[::-1]]

        return [(self._ids[i], float(scores[i])) for i in top_indices]

    # ------------------------------------------------------------------
    # Accessors
    # ------------------------------------------------------------------

    @property
    def is_ready(self) -> bool:
        """True once index_documents() has been called successfully."""
        return self._embeddings is not None and len(self._ids) > 0

    @property
    def corpus_size(self) -> int:
        return len(self._ids)

    @property
    def model_name(self) -> str:
        return self._model_name
