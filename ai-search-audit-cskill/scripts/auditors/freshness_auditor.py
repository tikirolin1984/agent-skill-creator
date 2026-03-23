"""
Pillar 6: Content Freshness & Originality Auditor

AI platforms prefer current, original content with unique data.
Checks content age, update frequency, original research, and decay signals.
"""

import logging
import re
from datetime import datetime
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False


class FreshnessAuditor:
    """Audits content freshness and originality for AI citation preference."""

    PILLAR_NAME = "Content Freshness & Originality"
    PILLAR_NUMBER = 6
    MAX_SCORE = 10

    def audit(self, url: str, depth: str = "full") -> "PillarResult":
        from scripts.main import PillarResult

        checks = []
        recommendations = []
        total_score = 0

        html = self._fetch(url)

        # Check 1: Last updated timestamps (max 2)
        r = self._check_timestamps(html)
        checks.append(r["check"]); total_score += r["score"]
        recommendations.extend(r.get("recommendations", []))

        # Check 2: Copyright year currency (max 2)
        r = self._check_copyright_year(html)
        checks.append(r["check"]); total_score += r["score"]
        recommendations.extend(r.get("recommendations", []))

        # Check 3: Original data/research signals (max 2)
        r = self._check_originality(html)
        checks.append(r["check"]); total_score += r["score"]
        recommendations.extend(r.get("recommendations", []))

        # Check 4: Content decay indicators (max 2)
        r = self._check_content_decay(html)
        checks.append(r["check"]); total_score += r["score"]
        recommendations.extend(r.get("recommendations", []))

        # Check 5: Datemodified schema (max 2)
        r = self._check_date_schema(html)
        checks.append(r["check"]); total_score += r["score"]
        recommendations.extend(r.get("recommendations", []))

        return PillarResult(
            pillar_name=self.PILLAR_NAME,
            pillar_number=self.PILLAR_NUMBER,
            score=total_score,
            max_score=self.MAX_SCORE,
            checks=checks,
            recommendations=recommendations,
        )

    def _fetch(self, url: str) -> Optional[str]:
        if not HAS_REQUESTS:
            return None
        try:
            resp = requests.get(url, timeout=10, headers={"User-Agent": "AISearchAudit/1.0"})
            return resp.text if resp.status_code == 200 else None
        except Exception:
            return None

    def _check_timestamps(self, html: Optional[str]) -> Dict[str, Any]:
        if not html:
            return {"check": {"name": "Content Timestamps", "status": "WARN", "detail": "Could not analyze", "score": 0, "max_score": 2}, "score": 0}

        # Look for "last updated", "modified", "published" dates
        patterns = [
            r'(?:last\s+)?(?:updated|modified|edited)\s*(?:on|:)?\s*(\w+\s+\d{1,2},?\s+\d{4}|\d{4}-\d{2}-\d{2})',
            r'(?:published|posted)\s*(?:on|:)?\s*(\w+\s+\d{1,2},?\s+\d{4}|\d{4}-\d{2}-\d{2})',
        ]

        has_update_date = False
        has_publish_date = False
        for i, pattern in enumerate(patterns):
            match = re.search(pattern, html, re.I)
            if match:
                if i == 0:
                    has_update_date = True
                else:
                    has_publish_date = True

        if has_update_date:
            return {"check": {"name": "Content Timestamps", "status": "PASS", "detail": "Last updated timestamp found", "score": 2, "max_score": 2}, "score": 2}
        elif has_publish_date:
            return {"check": {"name": "Content Timestamps", "status": "PARTIAL", "detail": "Publish date found but no 'last updated' timestamp", "score": 1, "max_score": 2}, "score": 1, "recommendations": ["Add 'Last updated: [date]' to cornerstone content — freshness signals boost AI citation"]}
        return {"check": {"name": "Content Timestamps", "status": "FAIL", "detail": "No visible content dates", "score": 0, "max_score": 2}, "score": 0, "recommendations": ["Add visible 'Last updated' dates to all key pages — AI prefers fresh content over stale"]}

    def _check_copyright_year(self, html: Optional[str]) -> Dict[str, Any]:
        if not html:
            return {"check": {"name": "Copyright Currency", "status": "WARN", "detail": "Could not analyze", "score": 0, "max_score": 2}, "score": 0}

        current_year = datetime.now().year
        copyright_match = re.search(r'(?:©|\bcopyright\b)\s*(\d{4})', html, re.I)

        if copyright_match:
            year = int(copyright_match.group(1))
            if year >= current_year:
                return {"check": {"name": "Copyright Currency", "status": "PASS", "detail": f"Copyright year is current ({year})", "score": 2, "max_score": 2}, "score": 2}
            elif year >= current_year - 1:
                return {"check": {"name": "Copyright Currency", "status": "PARTIAL", "detail": f"Copyright year is {year} (last year)", "score": 1, "max_score": 2}, "score": 1, "recommendations": [f"Update copyright year to {current_year}"]}
            return {"check": {"name": "Copyright Currency", "status": "FAIL", "detail": f"Outdated copyright: {year}", "score": 0, "max_score": 2}, "score": 0, "recommendations": [f"Update copyright year from {year} to {current_year} — signals active maintenance"]}
        return {"check": {"name": "Copyright Currency", "status": "PARTIAL", "detail": "No copyright year found", "score": 1, "max_score": 2}, "score": 1}

    def _check_originality(self, html: Optional[str]) -> Dict[str, Any]:
        if not html:
            return {"check": {"name": "Original Research Signals", "status": "WARN", "detail": "Could not analyze", "score": 0, "max_score": 2}, "score": 0}

        text = html.lower()
        originality_signals = [
            bool(re.search(r'(our\s+research|our\s+study|our\s+data|our\s+analysis|our\s+survey|our\s+findings)', text)),
            bool(re.search(r'(proprietary|exclusive|original\s+research|benchmark\s+study|first.to.publish)', text)),
            bool(re.search(r'(methodology|framework|model|index)\s+we\s+(developed|created|built|designed)', text)),
            bool(re.search(r'(data\s+from|survey\s+of)\s+\d+', text)),
            bool(re.search(r'(figure|chart|graph|table)\s+\d+', text)),
        ]

        count = sum(originality_signals)
        if count >= 3:
            return {"check": {"name": "Original Research Signals", "status": "PASS", "detail": f"{count} originality signals found (research, data, frameworks)", "score": 2, "max_score": 2}, "score": 2}
        elif count >= 1:
            return {"check": {"name": "Original Research Signals", "status": "PARTIAL", "detail": f"{count} originality signals — add more unique content", "score": 1, "max_score": 2}, "score": 1, "recommendations": ["Publish original research, benchmark studies, or proprietary data — AI engines cite unique sources"]}
        return {"check": {"name": "Original Research Signals", "status": "FAIL", "detail": "No original research or proprietary data signals", "score": 0, "max_score": 2}, "score": 0, "recommendations": ["Create original research: surveys, benchmark studies, unique datasets, or proprietary frameworks"]}

    def _check_content_decay(self, html: Optional[str]) -> Dict[str, Any]:
        if not html:
            return {"check": {"name": "Content Decay", "status": "WARN", "detail": "Could not analyze", "score": 0, "max_score": 2}, "score": 0}

        current_year = datetime.now().year
        # Look for old year references that suggest stale content
        old_years = re.findall(r'\b(201\d|202[0-3])\b', html)
        current_refs = re.findall(rf'\b{current_year}\b', html)
        recent_refs = re.findall(rf'\b{current_year - 1}\b', html)

        has_old = len(old_years) > 5
        has_current = len(current_refs) >= 2 or len(recent_refs) >= 2

        if has_current and not has_old:
            return {"check": {"name": "Content Decay", "status": "PASS", "detail": "Content references current year, no decay signals", "score": 2, "max_score": 2}, "score": 2}
        elif has_current:
            return {"check": {"name": "Content Decay", "status": "PARTIAL", "detail": "Mix of current and outdated references", "score": 1, "max_score": 2}, "score": 1, "recommendations": ["Update old year references and statistics to current data"]}
        elif has_old:
            return {"check": {"name": "Content Decay", "status": "FAIL", "detail": f"Content references outdated years with no current data", "score": 0, "max_score": 2}, "score": 0, "recommendations": ["Content shows decay — refresh all statistics, examples, and year references to current"]}
        return {"check": {"name": "Content Decay", "status": "PARTIAL", "detail": "No clear temporal signals found", "score": 1, "max_score": 2}, "score": 1}

    def _check_date_schema(self, html: Optional[str]) -> Dict[str, Any]:
        if not html:
            return {"check": {"name": "Date Schema Markup", "status": "WARN", "detail": "Could not analyze", "score": 0, "max_score": 2}, "score": 0}

        has_date_modified = bool(re.search(r'dateModified', html))
        has_date_published = bool(re.search(r'datePublished', html))

        if has_date_modified and has_date_published:
            return {"check": {"name": "Date Schema Markup", "status": "PASS", "detail": "Both datePublished and dateModified in schema", "score": 2, "max_score": 2}, "score": 2}
        elif has_date_published:
            return {"check": {"name": "Date Schema Markup", "status": "PARTIAL", "detail": "datePublished found but no dateModified", "score": 1, "max_score": 2}, "score": 1, "recommendations": ["Add dateModified to Article schema — AI systems use this to prioritize fresh content"]}
        return {"check": {"name": "Date Schema Markup", "status": "FAIL", "detail": "No date schema markup", "score": 0, "max_score": 2}, "score": 0, "recommendations": ["Add datePublished and dateModified to Article JSON-LD schema"]}
