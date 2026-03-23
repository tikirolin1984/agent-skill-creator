"""
GEO Readiness Score Calculator

Normalizes 7-pillar scores into a single 0-100 GEO Readiness Score
with weighted grading and prioritized recommendation ranking.
"""

import logging
from typing import Dict, Any, List, Tuple

logger = logging.getLogger(__name__)

GRADE_THRESHOLDS = [
    (85, "AI Search Leader"),
    (70, "AI Search Ready"),
    (50, "AI Search Developing"),
    (30, "AI Search Vulnerable"),
    (0, "AI Search Invisible"),
]

EFFORT_IMPACT_MAP = {
    "robots.txt": {"effort": "low", "impact": "high", "timeline": "week_1"},
    "llms.txt": {"effort": "low", "impact": "high", "timeline": "week_1"},
    "Organization": {"effort": "low", "impact": "high", "timeline": "week_1"},
    "FAQPage": {"effort": "medium", "impact": "high", "timeline": "month_1"},
    "Article": {"effort": "medium", "impact": "high", "timeline": "month_1"},
    "Person": {"effort": "medium", "impact": "medium", "timeline": "month_1"},
    "answer-first": {"effort": "medium", "impact": "high", "timeline": "month_1"},
    "sameAs": {"effort": "low", "impact": "medium", "timeline": "week_1"},
    "original research": {"effort": "high", "impact": "high", "timeline": "month_2_3"},
    "press": {"effort": "high", "impact": "high", "timeline": "month_2_3"},
    "Wikidata": {"effort": "high", "impact": "medium", "timeline": "month_2_3"},
    "copyright": {"effort": "low", "impact": "low", "timeline": "week_1"},
    "timestamps": {"effort": "low", "impact": "medium", "timeline": "week_1"},
    "dateModified": {"effort": "low", "impact": "medium", "timeline": "week_1"},
    "social": {"effort": "low", "impact": "medium", "timeline": "week_1"},
    "reviews": {"effort": "medium", "impact": "medium", "timeline": "month_1"},
    "community": {"effort": "medium", "impact": "medium", "timeline": "month_1"},
}


class ScoreCalculator:
    """Calculates GEO Readiness Score and prioritizes recommendations."""

    def calculate(self, pillar_results: list) -> Tuple[float, str]:
        """
        Calculate normalized GEO Readiness Score (0-100).

        Args:
            pillar_results: List of PillarResult objects

        Returns:
            Tuple of (score, grade_label)
        """
        total_raw = sum(p.score for p in pillar_results)
        total_max = sum(p.max_score for p in pillar_results)

        if total_max == 0:
            return 0.0, "AI Search Invisible"

        normalized = round((total_raw / total_max) * 100, 1)

        grade = "AI Search Invisible"
        for threshold, label in GRADE_THRESHOLDS:
            if normalized >= threshold:
                grade = label
                break

        return normalized, grade

    def prioritize_recommendations(
        self, pillar_results: list, max_recommendations: int = 15
    ) -> List[Dict[str, Any]]:
        """
        Prioritize recommendations by effort/impact across all pillars.

        Returns list of recommendations sorted by priority (high impact + low effort first).
        """
        all_recs = []

        for pillar in pillar_results:
            for check in pillar.checks:
                if check.get("status") in ("FAIL", "PARTIAL"):
                    for rec in pillar.recommendations:
                        priority_info = self._classify_recommendation(rec)
                        all_recs.append({
                            "recommendation": rec,
                            "pillar": pillar.pillar_name,
                            "pillar_number": pillar.pillar_number,
                            "current_score": f"{pillar.score}/{pillar.max_score}",
                            **priority_info,
                        })
                    break  # One set of recs per pillar

        # Sort: high impact first, then low effort first
        impact_order = {"high": 0, "medium": 1, "low": 2}
        effort_order = {"low": 0, "medium": 1, "high": 2}

        all_recs.sort(key=lambda r: (
            impact_order.get(r.get("impact", "medium"), 1),
            effort_order.get(r.get("effort", "medium"), 1),
        ))

        # Deduplicate
        seen = set()
        unique_recs = []
        for rec in all_recs:
            key = rec["recommendation"][:80]
            if key not in seen:
                seen.add(key)
                unique_recs.append(rec)

        return unique_recs[:max_recommendations]

    def _classify_recommendation(self, rec: str) -> Dict[str, str]:
        """Classify a recommendation by effort, impact, and timeline."""
        rec_lower = rec.lower()

        for keyword, info in EFFORT_IMPACT_MAP.items():
            if keyword.lower() in rec_lower:
                return {
                    "effort": info["effort"],
                    "impact": info["impact"],
                    "timeline": info["timeline"],
                }

        # Default classification based on heuristics
        if any(w in rec_lower for w in ["add", "create", "update", "fix", "remove"]):
            return {"effort": "medium", "impact": "medium", "timeline": "month_1"}
        if any(w in rec_lower for w in ["publish", "build", "develop", "launch"]):
            return {"effort": "high", "impact": "high", "timeline": "month_2_3"}

        return {"effort": "medium", "impact": "medium", "timeline": "month_1"}
