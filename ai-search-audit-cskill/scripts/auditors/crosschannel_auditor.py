"""
Pillar 7: Cross-Channel Authority Signals Auditor

AI systems evaluate the entire digital footprint, not just the website.
Checks PR mentions, social presence, reviews, and community signals.
"""

import logging
import re
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


class CrossChannelAuditor:
    """Audits cross-channel authority signals for AI recommendation rates."""

    PILLAR_NAME = "Cross-Channel Authority"
    PILLAR_NUMBER = 7
    MAX_SCORE = 10

    def audit(self, brand_name: str, url: str) -> "PillarResult":
        from scripts.main import PillarResult

        checks = []
        recommendations = []
        total_score = 0

        html = self._fetch(url)

        # Check 1: Social profile linking (max 2)
        r = self._check_social_presence(html)
        checks.append(r["check"]); total_score += r["score"]
        recommendations.extend(r.get("recommendations", []))

        # Check 2: Press/media mentions signals (max 2)
        r = self._check_press_signals(html)
        checks.append(r["check"]); total_score += r["score"]
        recommendations.extend(r.get("recommendations", []))

        # Check 3: Review platform presence (max 2)
        r = self._check_review_signals(html)
        checks.append(r["check"]); total_score += r["score"]
        recommendations.extend(r.get("recommendations", []))

        # Check 4: Industry authority signals (max 2)
        r = self._check_industry_authority(html)
        checks.append(r["check"]); total_score += r["score"]
        recommendations.extend(r.get("recommendations", []))

        # Check 5: Community engagement signals (max 2)
        r = self._check_community_signals(html, brand_name)
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

    def _check_social_presence(self, html: Optional[str]) -> Dict[str, Any]:
        if not html:
            return {"check": {"name": "Social Profile Linking", "status": "WARN", "detail": "Could not analyze", "score": 0, "max_score": 2}, "score": 0}

        platforms = {
            "LinkedIn": r'linkedin\.com',
            "Twitter/X": r'(?:twitter|x)\.com',
            "Facebook": r'facebook\.com',
            "YouTube": r'youtube\.com',
            "Instagram": r'instagram\.com',
            "GitHub": r'github\.com',
        }

        found = [name for name, pattern in platforms.items() if re.search(pattern, html, re.I)]

        if len(found) >= 4:
            return {"check": {"name": "Social Profile Linking", "status": "PASS", "detail": f"Linked to {len(found)} platforms: {', '.join(found)}", "score": 2, "max_score": 2}, "score": 2}
        elif len(found) >= 2:
            return {"check": {"name": "Social Profile Linking", "status": "PARTIAL", "detail": f"Only {len(found)} social links: {', '.join(found)}", "score": 1, "max_score": 2}, "score": 1, "recommendations": ["Add links to all major social profiles — AI systems cross-reference brand presence"]}
        return {"check": {"name": "Social Profile Linking", "status": "FAIL", "detail": "Minimal social presence linked", "score": 0, "max_score": 2}, "score": 0, "recommendations": ["Link to LinkedIn, Twitter/X, YouTube, and other social profiles from your site"]}

    def _check_press_signals(self, html: Optional[str]) -> Dict[str, Any]:
        if not html:
            return {"check": {"name": "Press/Media Signals", "status": "WARN", "detail": "Could not analyze", "score": 0, "max_score": 2}, "score": 0}

        press_signals = [
            r'(?:featured|mentioned|seen)\s+(?:in|on)',
            r'(?:Forbes|TechCrunch|Wired|Bloomberg|WSJ|NYT|BBC|CNN|Reuters)',
            r'press(?:\s+|-)?(?:release|coverage|mention)',
            r'(?:as seen|featured) (?:in|on)',
            r'media\s+(?:coverage|mention|feature)',
            r'award|certification|recognized',
        ]

        found = sum(1 for p in press_signals if re.search(p, html, re.I))

        if found >= 3:
            return {"check": {"name": "Press/Media Signals", "status": "PASS", "detail": f"{found} press/authority signals found", "score": 2, "max_score": 2}, "score": 2}
        elif found >= 1:
            return {"check": {"name": "Press/Media Signals", "status": "PARTIAL", "detail": f"Some press signals ({found})", "score": 1, "max_score": 2}, "score": 1, "recommendations": ["Showcase press mentions prominently — editorial citations boost AI recommendation rates"]}
        return {"check": {"name": "Press/Media Signals", "status": "FAIL", "detail": "No press or media authority signals", "score": 0, "max_score": 2}, "score": 0, "recommendations": ["Pursue PR strategy — brands cited by independent editorial sources get higher AI recommendation rates"]}

    def _check_review_signals(self, html: Optional[str]) -> Dict[str, Any]:
        if not html:
            return {"check": {"name": "Review Platform Presence", "status": "WARN", "detail": "Could not analyze", "score": 0, "max_score": 2}, "score": 0}

        review_platforms = [
            r'g2\.com', r'capterra', r'trustpilot', r'glassdoor',
            r'yelp', r'google\s+reviews?', r'trustradius',
            r'(?:\d+(?:\.\d)?)\s*(?:/5|stars?|rating)',
            r'(?:customer|client)\s+(?:reviews?|testimonials?)',
        ]

        found = sum(1 for p in review_platforms if re.search(p, html, re.I))

        if found >= 3:
            return {"check": {"name": "Review Platform Presence", "status": "PASS", "detail": f"{found} review/rating signals", "score": 2, "max_score": 2}, "score": 2}
        elif found >= 1:
            return {"check": {"name": "Review Platform Presence", "status": "PARTIAL", "detail": f"{found} review signals", "score": 1, "max_score": 2}, "score": 1, "recommendations": ["Showcase ratings from G2, Capterra, Trustpilot, or Google Reviews on your site"]}
        return {"check": {"name": "Review Platform Presence", "status": "FAIL", "detail": "No review platform signals", "score": 0, "max_score": 2}, "score": 0, "recommendations": ["Build review presence on G2, Capterra, or Trustpilot — AI systems reference third-party ratings"]}

    def _check_industry_authority(self, html: Optional[str]) -> Dict[str, Any]:
        if not html:
            return {"check": {"name": "Industry Authority", "status": "WARN", "detail": "Could not analyze", "score": 0, "max_score": 2}, "score": 0}

        authority_signals = [
            r'(?:case\s+stud(?:y|ies))',
            r'(?:white\s*paper|ebook|report|guide)',
            r'(?:webinar|conference|speaking|keynote)',
            r'(?:partner|integration|certification)',
            r'(?:client|customer)\s+(?:logo|story|success)',
        ]

        found = sum(1 for p in authority_signals if re.search(p, html, re.I))

        if found >= 3:
            return {"check": {"name": "Industry Authority", "status": "PASS", "detail": f"{found} industry authority signals", "score": 2, "max_score": 2}, "score": 2}
        elif found >= 1:
            return {"check": {"name": "Industry Authority", "status": "PARTIAL", "detail": f"{found} authority signals", "score": 1, "max_score": 2}, "score": 1, "recommendations": ["Add case studies, white papers, and partner logos to strengthen authority signals"]}
        return {"check": {"name": "Industry Authority", "status": "FAIL", "detail": "No industry authority signals", "score": 0, "max_score": 2}, "score": 0, "recommendations": ["Publish case studies, white papers, and showcase partnerships for authority building"]}

    def _check_community_signals(self, html: Optional[str], brand_name: str) -> Dict[str, Any]:
        if not html:
            return {"check": {"name": "Community Engagement", "status": "WARN", "detail": "Could not analyze", "score": 0, "max_score": 2}, "score": 0}

        community_signals = [
            r'(?:community|forum|discussion|slack|discord)',
            r'(?:open.source|github|contribute)',
            r'(?:newsletter|subscribe|join)',
            r'(?:blog|podcast|video|tutorial)',
        ]

        found = sum(1 for p in community_signals if re.search(p, html, re.I))

        if found >= 3:
            return {"check": {"name": "Community Engagement", "status": "PASS", "detail": f"{found} community signals", "score": 2, "max_score": 2}, "score": 2}
        elif found >= 1:
            return {"check": {"name": "Community Engagement", "status": "PARTIAL", "detail": f"{found} community signals", "score": 1, "max_score": 2}, "score": 1, "recommendations": ["Build community presence — forums, newsletters, and content hubs increase unlinked brand mentions"]}
        return {"check": {"name": "Community Engagement", "status": "FAIL", "detail": "No community engagement signals", "score": 0, "max_score": 2}, "score": 0, "recommendations": ["Launch blog, newsletter, or community forum — unlinked brand mentions carry weight in AI"]}
