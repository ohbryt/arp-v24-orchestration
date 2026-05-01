"""
ARP v26 - Hypothesis Agent
Auto hypothesis generation from literature and data

Based on Nature Medicine 2026 "Agentic framework for autonomous scientific discovery"
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any
import json


@dataclass
class Hypothesis:
    """A generated research hypothesis"""
    id: str
    target: str
    disease: str
    description: str
    mechanism: str
    predicted_outcome: str
    supporting_evidence: List[str]
    testable_predictions: List[str]
    confidence: float  # 0-1
    priority: str  # high, medium, low
    created: str = ""

    def __post_init__(self):
        if not self.created:
            self.created = datetime.now().isoformat()


class HypothesisAgent:
    """
    Agent that generates research hypotheses.
    Analyzes targets, diseases, and literature to produce testable hypotheses.
    """

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.llm_provider = self.config.get("llm_provider", "groq")
        self.model = self.config.get("model", "llama-3.3-70b")
        self.hypotheses: List[Hypothesis] = []
        self.history: List[Dict] = []

    async def generate(
        self,
        target: str,
        disease: str,
        context: Optional[Dict] = None,
        num_hypotheses: int = 3
    ) -> List[Hypothesis]:
        """
        Generate hypotheses for a target-disease pair.
        """
        context = context or {}
        prompt = self._build_prompt(target, disease, context)
        result = await self._call_llm(prompt)
        hypotheses = self._parse_hypotheses(result, target, disease)
        hypotheses = hypotheses[:num_hypotheses]
        self.hypotheses.extend(hypotheses)
        self.history.append({
            "target": target,
            "disease": disease,
            "num_generated": len(hypotheses),
            "timestamp": datetime.now().isoformat()
        })
        return hypotheses

    def _build_prompt(self, target: str, disease: str, context: Dict) -> str:
        context_str = ""
        if context.get("literature"):
            context_str += f"\nLiterature: {context['literature']}"
        if context.get("expression_data"):
            context_str += f"\nExpression: {context['expression_data']}"

        return f"""
You are a biomedical research hypothesis generator.

Generate testable hypotheses for targeting {target} in {disease}.

Consider:
1. Mechanism of action
2. Potential off-target effects
3. Biomarkers for patient selection
4. Combination therapy potential
5. Resistance mechanisms{context_str}

Generate exactly 3 hypotheses in JSON format.
"""

    async def _call_llm(self, prompt: str) -> str:
        """Call LLM for hypothesis generation"""
        try:
            from integration.groq_client import GroqClient
            client = GroqClient()
            response = await client.generate(prompt=prompt, model=self.model, temperature=0.2)
            return response
        except Exception:
            return "[]"

    def _parse_hypotheses(self, llm_response: str, target: str, disease: str) -> List[Hypothesis]:
        """Parse LLM response into Hypothesis objects"""
        import uuid
        hypotheses = []
        try:
            if "[" in llm_response and "]" in llm_response:
                json_str = llm_response[llm_response.index("["):llm_response.rindex("]")+1]
                data = json.loads(json_str)
                for item in data:
                    h = Hypothesis(
                        id=f"hyp_{uuid.uuid4().hex[:8]}",
                        target=target,
                        disease=disease,
                        description=item.get("description", ""),
                        mechanism=item.get("mechanism", ""),
                        predicted_outcome=item.get("predicted_outcome", ""),
                        supporting_evidence=item.get("supporting_evidence", []),
                        testable_predictions=item.get("testable_predictions", []),
                        confidence=item.get("confidence", 0.5),
                        priority=item.get("priority", "medium")
                    )
                    hypotheses.append(h)
        except (json.JSONDecodeError, ValueError):
            pass
        return hypotheses

    def get_hypotheses(
        self,
        target: Optional[str] = None,
        disease: Optional[str] = None,
        min_confidence: float = 0.0
    ) -> List[Hypothesis]:
        """Get stored hypotheses with optional filtering"""
        results = self.hypotheses
        if target:
            results = [h for h in results if target.lower() in h.target.lower()]
        if disease:
            results = [h for h in results if disease.lower() in h.disease.lower()]
        if min_confidence > 0:
            results = [h for h in results if h.confidence >= min_confidence]
        return results

    def rank_hypotheses(self, hypotheses: List[Hypothesis] = None) -> List[Hypothesis]:
        """Rank hypotheses by confidence and priority"""
        if hypotheses is None:
            hypotheses = self.hypotheses
        priority_weights = {"high": 3, "medium": 2, "low": 1}
        return sorted(
            hypotheses,
            key=lambda h: (h.confidence, priority_weights.get(h.priority, 0)),
            reverse=True
        )

    def export_hypotheses(self, format: str = "json") -> str:
        """Export hypotheses in specified format"""
        data = [
            {
                "id": h.id,
                "target": h.target,
                "disease": h.disease,
                "description": h.description,
                "mechanism": h.mechanism,
                "predicted_outcome": h.predicted_outcome,
                "supporting_evidence": h.supporting_evidence,
                "testable_predictions": h.testable_predictions,
                "confidence": h.confidence,
                "priority": h.priority,
                "created": h.created,
            }
            for h in self.hypotheses
        ]
        if format == "json":
            return json.dumps(data, indent=2)
        elif format == "csv":
            lines = ["id,target,disease,description,confidence,priority"]
            for h in data:
                lines.append(f'{h["id"]},{h["target"]},{h["disease"]},{h["description"]},{h["confidence"]},{h["priority"]}')
            return "\n".join(lines)
        return str(data)
