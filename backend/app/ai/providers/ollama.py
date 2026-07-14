"""
Ollama LLM Provider.
Integrates local Ollama instances via HTTP API with streaming support.
"""

import os
import json
import logging
import urllib.request
from typing import Dict, Any, Generator

from app.ai.providers.base import BaseLLMProvider
from app.ai.providers.mock import MockLLMProvider

logger = logging.getLogger(__name__)

class OllamaLLMProvider(BaseLLMProvider):
    """
    Connects to a local Ollama instance to analyze patient charts.
    """

    def __init__(self):
        self.host = os.getenv("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
        self.model = os.getenv("OLLAMA_MODEL", "llama3")
        self.mock_fallback = MockLLMProvider()

    def generate(self, question: str, context: Dict[str, Any]) -> Dict[str, Any]:
        system_prompt = (
            "You are an expert ICU Clinical Decision Support AI. Analyze the provided patient context and answer the clinical question.\n"
            "You MUST respond ONLY with a valid JSON object matching this schema:\n"
            "{\n"
            "  \"reasoning\": \"Detailed reasoning explaining findings\",\n"
            "  \"risk_drivers\": [\"List of positive/negative features contributing to risk\"],\n"
            "  \"abnormal_vitals\": [\"List of out-of-range vital signs\"],\n"
            "  \"abnormal_labs\": [\"List of out-of-range lab results\"],\n"
            "  \"recommendations\": [\"Recommended clinical stabilization guidelines\"],\n"
            "  \"evidence\": [\"Biomarkers or reference data values justifying findings\"],\n"
            "  \"confidence\": 0.95\n"
            "}\n"
            "Do not include markdown tags."
        )

        user_content = f"Patient Clinical Context:\n{json.dumps(context, indent=2)}\n\nQuestion:\n{question}"

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            "stream": False,
            "format": "json",
            "options": {
                "temperature": 0.2
            }
        }

        try:
            req = urllib.request.Request(
                f"{self.host}/api/chat",
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            # Timeout set to 10 seconds to detect offline services quickly
            with urllib.request.urlopen(req, timeout=10.0) as response:
                body = response.read().decode("utf-8")
                res_data = json.loads(body)
                raw_text = res_data["message"]["content"]
                data = json.loads(raw_text)

                # Map legacy fields for compatibility
                data["summary"] = data.get("reasoning", "")
                data["findings"] = data.get("risk_drivers", []) + data.get("abnormal_vitals", []) + data.get("abnormal_labs", [])
                data["risk"] = data.get("risk_drivers", ["Unknown"])[0] if data.get("risk_drivers") else "Unknown"

                return data
        except Exception as e:
            logger.warning(f"Ollama completion failed: {e}. Falling back to MockProvider.")
            return self.mock_fallback.generate(question, context)

    def generate_stream(self, question: str, context: Dict[str, Any]) -> Generator[Dict[str, Any], None, None]:
        system_prompt = (
            "You are an expert ICU Clinical Decision Support AI. Analyze the provided patient context and answer the clinical question.\n"
            "You MUST respond ONLY with a valid JSON object matching this schema:\n"
            "{\n"
            "  \"reasoning\": \"Detailed reasoning explaining findings\",\n"
            "  \"risk_drivers\": [\"List of positive/negative features contributing to risk\"],\n"
            "  \"abnormal_vitals\": [\"List of out-of-range vital signs\"],\n"
            "  \"abnormal_labs\": [\"List of out-of-range lab results\"],\n"
            "  \"recommendations\": [\"Recommended clinical stabilization guidelines\"],\n"
            "  \"evidence\": [\"Biomarkers or reference data values justifying findings\"],\n"
            "  \"confidence\": 0.95\n"
            "}\n"
            "Do not include markdown tags."
        )

        user_content = f"Patient Clinical Context:\n{json.dumps(context, indent=2)}\n\nQuestion:\n{question}"

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            "stream": True,
            "format": "json",
            "options": {
                "temperature": 0.2
            }
        }

        try:
            req = urllib.request.Request(
                f"{self.host}/api/chat",
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            # Timeout set to 30 seconds for local streaming
            with urllib.request.urlopen(req, timeout=30.0) as response:
                accumulated_text = ""
                for line in response:
                    line_str = line.decode("utf-8").strip()
                    if not line_str:
                        continue
                    try:
                        chunk = json.loads(line_str)
                        if "message" in chunk and "content" in chunk["message"]:
                            token = chunk["message"]["content"]
                            accumulated_text += token
                            yield {"type": "token", "content": token}
                    except Exception:
                        continue

                try:
                    data = json.loads(accumulated_text)
                    data["summary"] = data.get("reasoning", "")
                    data["findings"] = data.get("risk_drivers", []) + data.get("abnormal_vitals", []) + data.get("abnormal_labs", [])
                    data["risk"] = data.get("risk_drivers", ["Unknown"])[0] if data.get("risk_drivers") else "Unknown"
                    yield {"type": "final", "content": data}
                except Exception:
                    yield {"type": "final", "content": self.mock_fallback.generate(question, context)}

        except Exception as e:
            logger.warning(f"Ollama streaming failed: {e}. Falling back to MockProvider.")
            yield from self.mock_fallback.generate_stream(question, context)
