"""
Mock LLM Provider.
Returns simulated reasoning based on patient context, supporting token streaming.
"""

import time
from typing import Dict, Any, Generator
from app.ai.providers.base import BaseLLMProvider
from app.services.explainable_reasoning_service import ExplainableReasoningService

class MockLLMProvider(BaseLLMProvider):
    """
    Simulates clinical LLM responses by delegating to ExplainableReasoningService.
    """

    def generate(self, question: str, context: Dict[str, Any]) -> Dict[str, Any]:
        explanation = ExplainableReasoningService.process_explainable_query(question, context)
        # Populate legacy fields for backward compatibility
        explanation["summary"] = explanation["reasoning"]
        explanation["findings"] = explanation["risk_drivers"] + explanation["abnormal_vitals"] + explanation["abnormal_labs"]
        explanation["risk"] = explanation["risk_drivers"][0] if explanation["risk_drivers"] else "Unknown"
        return explanation

    def generate_stream(self, question: str, context: Dict[str, Any]) -> Generator[Dict[str, Any], None, None]:
        """
        Simulates word-by-word streaming of clinical reasoning.
        """
        final_response = self.generate(question, context)
        reasoning = final_response.get("reasoning", "")

        words = reasoning.split(" ")
        for word in words:
            yield {"type": "token", "content": word + " "}
            time.sleep(0.02)

        yield {"type": "final", "content": final_response}
