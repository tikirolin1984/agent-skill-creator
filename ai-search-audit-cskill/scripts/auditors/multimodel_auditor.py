"""
Pillar 4: Multi-Model Optimization Auditor

Checks platform-specific readiness for ChatGPT, Perplexity, Google AI Overviews,
Gemini, Claude, and Copilot. Each platform has unique extraction behaviors.
"""

import logging
import re
import json
from typing import Dict, Any, List, Optional

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

PLATFORM_REQUIREMENTS = {
    "chatgpt": {
        "name": "ChatGPT (OpenAI)",
        "crawler": "GPTBot",
        "key_schemas": ["FAQPage", "Article"],
        "content_needs": ["FAQ blocks", "Article schema", "Bing-indexed"],
        "behavior": "Falls back to English sources; uses Bing index; values FAQPage + Article schema",
    },
    "perplexity": {
        "name": "Perplexity",
        "crawler": "PerplexityBot",
        "key_schemas": ["Organization", "Product"],
        "content_needs": ["Multi-angle coverage", "Organization schema", "Source citations"],
        "behavior": "Generates internal search queries before answering; aggregates multiple sources",
    },
    "google_ai_overviews": {
        "name": "Google AI Overviews",
        "crawler": "Google-Extended",
        "key_schemas": ["Article", "FAQPage", "HowTo"],
        "content_needs": ["Valid GSC schema", "Featured snippet optimization", "E-E-A-T signals"],
        "behavior": "Appears in ~60% of searches; prefers pages with valid Search Console schema",
    },
    "gemini": {
        "name": "Gemini (Google)",
        "crawler": "Google-Extended",
        "key_schemas": ["Article"],
        "content_needs": ["Clean paragraphs", "Scannable formatting", "Paragraph-level answers"],
        "behavior": "Performs paragraph-level text extraction; prefers clean scannable content",
    },
    "claude": {
        "name": "Claude (Anthropic)",
        "crawler": "ClaudeBot",
        "key_schemas": ["Article", "Organization"],
        "content_needs": ["Source citations", "Data-rich content", "Factual accuracy"],
        "behavior": "Prioritizes well-structured, factual, source-cited content",
    },
    "copilot": {
        "name": "Copilot (Microsoft)",
        "crawler": "Bingbot",
        "key_schemas": ["Article", "FAQPage"],
        "content_needs": ["Bing Webmaster Tools", "Bing indexing", "Structured answers"],
        "behavior": "Leverages Bing index heavily; good Bing SEO = good Copilot visibility",
    },
}


class MultiModelAuditor:
    """Audits platform-specific optimization across AI search engines."""

    PILLAR_NAME = "Multi-Model Optimization"
    PILLAR_NUMBER = 4
    MAX_SCORE = 12

    def audit(self, url: str, platforms: Optional[List[str]] = None) -> "PillarResult":
        from scripts.main import PillarResult

        if platforms is None:
            platforms = list(PLATFORM_REQUIREMENTS.keys())

        html = self._fetch(url)
        schemas_found = self._extract_schema_types(html) if html else set()
        robots_content = self._fetch_robots(url)

        checks = []
        recommendations = []
        total_score = 0
        points_per_platform = 12 / len(platforms)

        for platform_key in platforms:
            if platform_key not in PLATFORM_REQUIREMENTS:
                continue

            platform = PLATFORM_REQUIREMENTS[platform_key]
            r = self._check_platform(platform_key, platform, html, schemas_found, robots_content, points_per_platform)
            checks.append(r["check"])
            total_score += r["score"]
            recommendations.extend(r.get("recommendations", []))

        return PillarResult(
            pillar_name=self.PILLAR_NAME,
            pillar_number=self.PILLAR_NUMBER,
            score=round(min(total_score, self.MAX_SCORE), 1),
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

    def _fetch_robots(self, url: str) -> Optional[str]:
        from urllib.parse import urljoin
        if not url.startswith("http"):
            url = f"https://{url}"
        robots_url = urljoin(url.rstrip("/") + "/", "/robots.txt")
        return self._fetch(robots_url)

    def _extract_schema_types(self, html: str) -> set:
        types = set()
        for match in re.finditer(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html, re.DOTALL | re.IGNORECASE):
            try:
                data = json.loads(match.group(1).strip())
                items = [data] if isinstance(data, dict) else data if isinstance(data, list) else []
                for item in items:
                    if "@type" in item:
                        types.add(item["@type"])
                    if "@graph" in item:
                        for g in item["@graph"]:
                            if "@type" in g:
                                types.add(g["@type"])
            except (json.JSONDecodeError, TypeError):
                continue
        return types

    def _check_platform(
        self, key: str, platform: Dict, html: Optional[str],
        schemas: set, robots: Optional[str], max_points: float
    ) -> Dict[str, Any]:
        """Check readiness for a specific AI platform."""
        signals = 0
        total_signals = 3
        issues = []

        # Signal 1: Crawler access
        crawler = platform["crawler"]
        if robots and self._crawler_allowed(robots, crawler):
            signals += 1
        elif robots:
            issues.append(f"{crawler} blocked in robots.txt")
        else:
            signals += 0.5  # Unknown

        # Signal 2: Required schemas present
        required = platform["key_schemas"]
        found = [s for s in required if s in schemas]
        if len(found) == len(required):
            signals += 1
        elif found:
            signals += 0.5
            issues.append(f"Missing schema: {', '.join(s for s in required if s not in schemas)}")
        else:
            issues.append(f"Missing all required schemas: {', '.join(required)}")

        # Signal 3: Content structure alignment
        if html:
            content_score = self._check_content_alignment(html, key)
            signals += content_score
        else:
            issues.append("Could not analyze content structure")

        score = round((signals / total_signals) * max_points, 1)
        pct = round((signals / total_signals) * 100)

        if pct >= 80:
            status = "PASS"
        elif pct >= 50:
            status = "PARTIAL"
        else:
            status = "FAIL"

        recs = []
        if issues:
            recs.append(f"{platform['name']}: Fix — {'; '.join(issues)}")

        return {
            "check": {
                "name": f"{platform['name']} Readiness",
                "status": status,
                "detail": f"{pct}% ready. {platform['behavior']}",
                "score": score,
                "max_score": round(max_points, 1),
                "issues": issues,
            },
            "score": score,
            "recommendations": recs,
        }

    def _crawler_allowed(self, robots: str, crawler_name: str) -> bool:
        lines = robots.split("\n")
        current_agent = None
        for line in lines:
            line = line.strip()
            if line.lower().startswith("user-agent:"):
                current_agent = line.split(":", 1)[1].strip().lower()
            elif line.lower().startswith("disallow:") and current_agent:
                path = line.split(":", 1)[1].strip()
                if (current_agent == crawler_name.lower() or current_agent == "*") and path == "/":
                    return False
        return True

    def _check_content_alignment(self, html: str, platform_key: str) -> float:
        """Check if content structure aligns with platform preferences."""
        if platform_key == "gemini":
            # Gemini: paragraph-level extraction — clean paragraphs
            if HAS_BS4:
                soup = BeautifulSoup(html, "html.parser")
                paragraphs = soup.find_all("p")
                good_paras = [p for p in paragraphs if 50 <= len(p.get_text(strip=True)) <= 300]
                return 1.0 if len(good_paras) >= 5 else 0.5 if good_paras else 0

        elif platform_key == "chatgpt":
            # ChatGPT: FAQ blocks, article structure
            has_faq = bool(re.search(r'FAQPage', html))
            has_article = bool(re.search(r'"@type":\s*"Article"', html))
            return 1.0 if (has_faq or has_article) else 0.5

        elif platform_key == "perplexity":
            # Perplexity: multi-source, citations
            has_external_links = len(re.findall(r'href="https?://', html)) > 5
            return 1.0 if has_external_links else 0.5

        elif platform_key == "claude":
            # Claude: factual, source-cited
            has_sources = bool(re.search(r'(source|reference|citation|according to)', html, re.I))
            has_data = bool(re.search(r'\d+%', html))
            return 1.0 if (has_sources and has_data) else 0.5 if has_sources else 0

        return 0.5  # Default partial
