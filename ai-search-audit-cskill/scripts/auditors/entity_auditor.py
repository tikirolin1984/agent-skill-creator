"""
Pillar 3: Entity Authority Auditor

Measures whether AI systems recognize the brand as a distinct, authoritative entity.
Checks Knowledge Graph presence, sameAs linking, topical depth, and author markup.
"""

import logging
import re
import json
from typing import Dict, Any, Optional

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


class EntityAuditor:
    """Audits entity authority signals for AI search engines."""

    PILLAR_NAME = "Entity Authority"
    PILLAR_NUMBER = 3
    MAX_SCORE = 16

    def audit(self, url: str, brand_name: str = "", industry: str = "") -> "PillarResult":
        from scripts.main import PillarResult

        checks = []
        recommendations = []
        total_score = 0

        html = self._fetch(url)

        # Check 1: Organization schema with sameAs (max 3)
        r = self._check_organization_schema(html)
        checks.append(r["check"]); total_score += r["score"]
        recommendations.extend(r.get("recommendations", []))

        # Check 2: sameAs linking breadth (max 2)
        r = self._check_sameas_links(html)
        checks.append(r["check"]); total_score += r["score"]
        recommendations.extend(r.get("recommendations", []))

        # Check 3: Author entity markup (max 2)
        r = self._check_author_markup(html)
        checks.append(r["check"]); total_score += r["score"]
        recommendations.extend(r.get("recommendations", []))

        # Check 4: Brand consistency signals (max 2)
        r = self._check_brand_consistency(html, brand_name)
        checks.append(r["check"]); total_score += r["score"]
        recommendations.extend(r.get("recommendations", []))

        # Check 5: Topical coverage depth (max 3)
        r = self._check_topical_depth(html, url)
        checks.append(r["check"]); total_score += r["score"]
        recommendations.extend(r.get("recommendations", []))

        # Check 6: About page entity signals (max 2)
        r = self._check_about_page(url)
        checks.append(r["check"]); total_score += r["score"]
        recommendations.extend(r.get("recommendations", []))

        # Check 7: Contact/trust signals (max 2)
        r = self._check_trust_signals(html)
        checks.append(r["check"]); total_score += r["score"]
        recommendations.extend(r.get("recommendations", []))

        return PillarResult(
            pillar_name=self.PILLAR_NAME,
            pillar_number=self.PILLAR_NUMBER,
            score=min(total_score, self.MAX_SCORE),
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

    def _extract_jsonld(self, html: str) -> list:
        if not html:
            return []
        results = []
        for match in re.finditer(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html, re.DOTALL | re.IGNORECASE):
            try:
                data = json.loads(match.group(1).strip())
                if isinstance(data, list):
                    results.extend(data)
                elif isinstance(data, dict):
                    if "@graph" in data:
                        results.extend(data["@graph"])
                    else:
                        results.append(data)
            except (json.JSONDecodeError, TypeError):
                continue
        return results

    def _check_organization_schema(self, html: Optional[str]) -> Dict[str, Any]:
        if not html:
            return {"check": {"name": "Organization Schema", "status": "FAIL", "detail": "Could not analyze", "score": 0, "max_score": 3}, "score": 0, "recommendations": ["Add Organization JSON-LD schema with name, url, logo, and sameAs properties"]}

        schemas = self._extract_jsonld(html)
        org = next((s for s in schemas if s.get("@type") == "Organization"), None)

        if org:
            has_name = bool(org.get("name"))
            has_url = bool(org.get("url"))
            has_logo = bool(org.get("logo"))
            has_sameas = bool(org.get("sameAs"))
            has_description = bool(org.get("description"))

            completeness = sum([has_name, has_url, has_logo, has_sameas, has_description])
            if completeness >= 4:
                return {"check": {"name": "Organization Schema", "status": "PASS", "detail": f"Organization schema with {completeness}/5 key properties", "score": 3, "max_score": 3}, "score": 3}
            elif completeness >= 2:
                missing = []
                if not has_sameas: missing.append("sameAs")
                if not has_logo: missing.append("logo")
                if not has_description: missing.append("description")
                return {"check": {"name": "Organization Schema", "status": "PARTIAL", "detail": f"Organization schema missing: {', '.join(missing)}", "score": 2, "max_score": 3}, "score": 2, "recommendations": [f"Add missing Organization schema properties: {', '.join(missing)}"]}

        return {"check": {"name": "Organization Schema", "status": "FAIL", "detail": "No Organization schema found", "score": 0, "max_score": 3}, "score": 0, "recommendations": ["Add Organization JSON-LD schema — this is how AI identifies your brand as a unique entity"]}

    def _check_sameas_links(self, html: Optional[str]) -> Dict[str, Any]:
        if not html:
            return {"check": {"name": "sameAs Linking", "status": "FAIL", "detail": "Could not analyze", "score": 0, "max_score": 2}, "score": 0}

        schemas = self._extract_jsonld(html)
        sameas_urls = []
        for s in schemas:
            sa = s.get("sameAs", [])
            if isinstance(sa, str):
                sameas_urls.append(sa)
            elif isinstance(sa, list):
                sameas_urls.extend(sa)

        platforms = {"wikipedia": False, "wikidata": False, "linkedin": False, "twitter": False, "facebook": False, "crunchbase": False}
        for url in sameas_urls:
            for platform in platforms:
                if platform in url.lower():
                    platforms[platform] = True

        linked_count = sum(platforms.values())
        if linked_count >= 4:
            return {"check": {"name": "sameAs Linking", "status": "PASS", "detail": f"Linked to {linked_count} platforms: {', '.join(k for k, v in platforms.items() if v)}", "score": 2, "max_score": 2}, "score": 2}
        elif linked_count >= 2:
            missing = [k for k, v in platforms.items() if not v]
            return {"check": {"name": "sameAs Linking", "status": "PARTIAL", "detail": f"Linked to {linked_count} platforms, missing: {', '.join(missing[:3])}", "score": 1, "max_score": 2}, "score": 1, "recommendations": [f"Add sameAs links for: {', '.join(missing[:3])} — especially Wikipedia/Wikidata for AI entity resolution"]}
        return {"check": {"name": "sameAs Linking", "status": "FAIL", "detail": "No or minimal sameAs linking", "score": 0, "max_score": 2}, "score": 0, "recommendations": ["Add sameAs links to Wikipedia, Wikidata, LinkedIn, and social profiles in Organization schema"]}

    def _check_author_markup(self, html: Optional[str]) -> Dict[str, Any]:
        if not html:
            return {"check": {"name": "Author Entity Markup", "status": "WARN", "detail": "Could not analyze", "score": 0, "max_score": 2}, "score": 0}

        schemas = self._extract_jsonld(html)
        has_person = any(s.get("@type") == "Person" for s in schemas)
        has_author = any("author" in s for s in schemas)
        has_rel_author = bool(re.search(r'rel=["\']author["\']', html, re.I))

        if has_person or has_author:
            return {"check": {"name": "Author Entity Markup", "status": "PASS", "detail": "Author/Person schema markup found", "score": 2, "max_score": 2}, "score": 2}
        elif has_rel_author:
            return {"check": {"name": "Author Entity Markup", "status": "PARTIAL", "detail": "rel=author found but no Person schema", "score": 1, "max_score": 2}, "score": 1, "recommendations": ["Add Person JSON-LD schema for content authors"]}
        return {"check": {"name": "Author Entity Markup", "status": "FAIL", "detail": "No author entity markup", "score": 0, "max_score": 2}, "score": 0, "recommendations": ["Add author markup with Person schema — AI systems attribute content authority to named authors"]}

    def _check_brand_consistency(self, html: Optional[str], brand_name: str) -> Dict[str, Any]:
        if not html or not brand_name:
            return {"check": {"name": "Brand Consistency", "status": "WARN", "detail": "Brand name not provided or page not accessible", "score": 1, "max_score": 2}, "score": 1}

        title_match = bool(re.search(re.escape(brand_name), html[:500], re.I))
        og_match = bool(re.search(rf'og:site_name["\'][^>]*content=["\'][^"\']*{re.escape(brand_name)}', html, re.I))
        mention_count = len(re.findall(re.escape(brand_name), html, re.I))

        if title_match and mention_count >= 3:
            return {"check": {"name": "Brand Consistency", "status": "PASS", "detail": f"Brand '{brand_name}' consistently referenced ({mention_count} mentions)", "score": 2, "max_score": 2}, "score": 2}
        elif mention_count >= 1:
            return {"check": {"name": "Brand Consistency", "status": "PARTIAL", "detail": f"Brand mentioned {mention_count} times", "score": 1, "max_score": 2}, "score": 1, "recommendations": ["Increase brand name consistency — use exact brand name in title, meta, and body content"]}
        return {"check": {"name": "Brand Consistency", "status": "FAIL", "detail": "Brand name not found on page", "score": 0, "max_score": 2}, "score": 0, "recommendations": ["Ensure brand name appears in title tag, OG meta, and body content consistently"]}

    def _check_topical_depth(self, html: Optional[str], url: str) -> Dict[str, Any]:
        """Heuristic check for topical coverage depth via internal link analysis."""
        if not html or not HAS_BS4:
            return {"check": {"name": "Topical Coverage Depth", "status": "WARN", "detail": "Could not analyze internal links", "score": 1, "max_score": 3}, "score": 1}

        from urllib.parse import urlparse
        soup = BeautifulSoup(html, "html.parser")
        parsed = urlparse(url)
        domain = parsed.netloc

        internal_links = set()
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if domain in href or href.startswith("/"):
                internal_links.add(href)

        # More internal links suggests deeper topical coverage
        count = len(internal_links)
        if count >= 50:
            return {"check": {"name": "Topical Coverage Depth", "status": "PASS", "detail": f"{count} internal links suggesting deep topical coverage", "score": 3, "max_score": 3}, "score": 3}
        elif count >= 20:
            return {"check": {"name": "Topical Coverage Depth", "status": "PARTIAL", "detail": f"{count} internal links — moderate coverage", "score": 2, "max_score": 3}, "score": 2, "recommendations": ["Build topic clusters with 20+ interlinked pages per core topic for deeper authority"]}
        return {"check": {"name": "Topical Coverage Depth", "status": "FAIL", "detail": f"Only {count} internal links — thin topical coverage", "score": 0, "max_score": 3}, "score": 0, "recommendations": ["Brands with comprehensive topical coverage get cited 6.2x more — build deep content clusters"]}

    def _check_about_page(self, url: str) -> Dict[str, Any]:
        from urllib.parse import urljoin
        about_candidates = ["/about", "/about-us", "/company", "/about/"]
        for path in about_candidates:
            about_url = urljoin(url, path)
            html = self._fetch(about_url)
            if html:
                schemas = self._extract_jsonld(html)
                has_org = any(s.get("@type") == "Organization" for s in schemas)
                word_count = len(html.split()) if html else 0
                if has_org and word_count > 500:
                    return {"check": {"name": "About Page Entity Signals", "status": "PASS", "detail": f"Rich about page found at {path} with Organization schema", "score": 2, "max_score": 2}, "score": 2}
                elif html:
                    return {"check": {"name": "About Page Entity Signals", "status": "PARTIAL", "detail": f"About page found at {path} but missing schema", "score": 1, "max_score": 2}, "score": 1, "recommendations": ["Add Organization schema to about page with full company details"]}
        return {"check": {"name": "About Page Entity Signals", "status": "FAIL", "detail": "No about page found", "score": 0, "max_score": 2}, "score": 0, "recommendations": ["Create a comprehensive about page with Organization schema — this anchors your brand entity"]}

    def _check_trust_signals(self, html: Optional[str]) -> Dict[str, Any]:
        if not html:
            return {"check": {"name": "Trust Signals", "status": "WARN", "detail": "Could not analyze", "score": 0, "max_score": 2}, "score": 0}

        has_address = bool(re.search(r'<address|streetAddress|postalCode', html, re.I))
        has_phone = bool(re.search(r'telephone|tel:', html, re.I))
        has_privacy = bool(re.search(r'privacy.?policy|terms.?of.?service', html, re.I))

        signals = sum([has_address, has_phone, has_privacy])
        if signals >= 2:
            return {"check": {"name": "Trust Signals", "status": "PASS", "detail": "Strong trust signals (address, contact, policies)", "score": 2, "max_score": 2}, "score": 2}
        elif signals >= 1:
            return {"check": {"name": "Trust Signals", "status": "PARTIAL", "detail": "Some trust signals present", "score": 1, "max_score": 2}, "score": 1, "recommendations": ["Add physical address, phone number, and privacy policy links — trust signals reinforce entity authority"]}
        return {"check": {"name": "Trust Signals", "status": "FAIL", "detail": "No trust signals detected", "score": 0, "max_score": 2}, "score": 0, "recommendations": ["Add contact info, physical address, and policy links to reinforce brand legitimacy"]}
