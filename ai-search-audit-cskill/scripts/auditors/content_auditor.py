"""
Pillar 2: Content Extractability Auditor

Evaluates whether content is structured for AI synthesis and citation.
Checks answer-first patterns, FAQ schema, data density, and source citations.
"""

import logging
import re
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


class ContentAuditor:
    """Audits content extractability for AI search engines."""

    PILLAR_NAME = "Content Extractability"
    PILLAR_NUMBER = 2
    MAX_SCORE = 16

    def audit(self, url: str, depth: str = "full") -> "PillarResult":
        """Run content extractability audit on target URL."""
        from scripts.main import PillarResult

        checks = []
        recommendations = []
        total_score = 0

        html = self._fetch(url)
        if html is None:
            return PillarResult(
                pillar_name=self.PILLAR_NAME,
                pillar_number=self.PILLAR_NUMBER,
                score=0, max_score=self.MAX_SCORE,
                checks=[{"name": "Fetch", "status": "ERROR", "detail": "Could not fetch URL"}],
                recommendations=["Ensure URL is accessible"],
            )

        text, soup = self._parse(html)

        # Check 1: Answer-first / TLDR structure (max 2)
        r = self._check_answer_first(text, soup)
        checks.append(r["check"]); total_score += r["score"]
        recommendations.extend(r.get("recommendations", []))

        # Check 2: Question-based H2 headings (max 2)
        r = self._check_question_headings(soup)
        checks.append(r["check"]); total_score += r["score"]
        recommendations.extend(r.get("recommendations", []))

        # Check 3: FAQ blocks with schema (max 2)
        r = self._check_faq_schema(html, soup)
        checks.append(r["check"]); total_score += r["score"]
        recommendations.extend(r.get("recommendations", []))

        # Check 4: Statistics and data density (max 2)
        r = self._check_data_density(text)
        checks.append(r["check"]); total_score += r["score"]
        recommendations.extend(r.get("recommendations", []))

        # Check 5: Source citations (max 2)
        r = self._check_source_citations(soup)
        checks.append(r["check"]); total_score += r["score"]
        recommendations.extend(r.get("recommendations", []))

        # Check 6: Expert quotes (max 2)
        r = self._check_expert_quotes(text)
        checks.append(r["check"]); total_score += r["score"]
        recommendations.extend(r.get("recommendations", []))

        # Check 7: Content depth (max 2)
        r = self._check_content_depth(text, soup)
        checks.append(r["check"]); total_score += r["score"]
        recommendations.extend(r.get("recommendations", []))

        # Check 8: Heading hierarchy (max 2)
        r = self._check_heading_hierarchy(soup)
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
        except Exception as e:
            logger.warning(f"Fetch failed: {e}")
            return None

    def _parse(self, html: str):
        text = html
        soup = None
        if HAS_BS4:
            soup = BeautifulSoup(html, "html.parser")
            text = soup.get_text(separator=" ", strip=True)
        return text, soup

    def _check_answer_first(self, text: str, soup) -> Dict[str, Any]:
        """Check if first 200 words directly answer a query."""
        words = text.split()[:200]
        first_200 = " ".join(words)

        # Heuristics: answer-first content contains definitive statements early
        has_definition = bool(re.search(r'\b(is|are|means|refers to|defined as)\b', first_200, re.I))
        has_numbers = bool(re.search(r'\d+%|\$\d+|\d+\.\d+', first_200))
        has_direct_answer = bool(re.search(r'^(The |A |An |In |For |This )', first_200.strip()))

        signals = sum([has_definition, has_numbers, has_direct_answer])
        if signals >= 2:
            return {"check": {"name": "Answer-First Structure", "status": "PASS", "detail": "Content leads with direct answers in first 200 words", "score": 2, "max_score": 2}, "score": 2}
        elif signals >= 1:
            return {"check": {"name": "Answer-First Structure", "status": "PARTIAL", "detail": "Content partially answers queries in opening", "score": 1, "max_score": 2}, "score": 1, "recommendations": ["Restructure opening 200 words to directly answer the primary query"]}
        return {"check": {"name": "Answer-First Structure", "status": "FAIL", "detail": "Opening content does not directly answer queries", "score": 0, "max_score": 2}, "score": 0, "recommendations": ["Lead with a TLDR summary that directly answers the primary question in the first 200 words"]}

    def _check_question_headings(self, soup) -> Dict[str, Any]:
        """Check if H2 headings match question patterns users ask AI."""
        if not soup:
            return {"check": {"name": "Question-Based Headings", "status": "WARN", "detail": "Could not parse HTML", "score": 0, "max_score": 2}, "score": 0}

        h2s = [h.get_text(strip=True) for h in soup.find_all("h2")]
        question_h2s = [h for h in h2s if re.search(r'^(What|How|Why|When|Where|Which|Can|Do|Is|Are|Should)\b', h, re.I) or h.endswith("?")]

        if not h2s:
            return {"check": {"name": "Question-Based Headings", "status": "FAIL", "detail": "No H2 headings found", "score": 0, "max_score": 2}, "score": 0, "recommendations": ["Add H2 headings structured as questions that match how users query AI systems"]}

        ratio = len(question_h2s) / len(h2s) if h2s else 0
        if ratio >= 0.3:
            return {"check": {"name": "Question-Based Headings", "status": "PASS", "detail": f"{len(question_h2s)}/{len(h2s)} H2s are question-formatted", "score": 2, "max_score": 2}, "score": 2}
        elif question_h2s:
            return {"check": {"name": "Question-Based Headings", "status": "PARTIAL", "detail": f"Only {len(question_h2s)}/{len(h2s)} H2s use question format", "score": 1, "max_score": 2}, "score": 1, "recommendations": ["Convert more H2 headings to question format matching AI query patterns"]}
        return {"check": {"name": "Question-Based Headings", "status": "FAIL", "detail": f"0/{len(h2s)} H2s use question format", "score": 0, "max_score": 2}, "score": 0, "recommendations": ["Rewrite H2 headings as questions: 'What is X?', 'How to Y?', 'Why does Z matter?'"]}

    def _check_faq_schema(self, html: str, soup) -> Dict[str, Any]:
        """Check for FAQ blocks with proper schema markup."""
        has_faq_schema = bool(re.search(r'FAQPage', html))
        has_faq_content = bool(re.search(r'<(details|dt|dl)', html, re.I))
        if soup:
            has_faq_content = has_faq_content or bool(soup.find_all(class_=re.compile(r'faq', re.I)))

        if has_faq_schema:
            return {"check": {"name": "FAQ Schema", "status": "PASS", "detail": "FAQPage schema markup detected", "score": 2, "max_score": 2}, "score": 2}
        elif has_faq_content:
            return {"check": {"name": "FAQ Schema", "status": "PARTIAL", "detail": "FAQ content found but no FAQPage schema", "score": 1, "max_score": 2}, "score": 1, "recommendations": ["Add FAQPage JSON-LD schema to your FAQ sections — FAQ blocks with schema get cited 3.2x more"]}
        return {"check": {"name": "FAQ Schema", "status": "FAIL", "detail": "No FAQ content or schema found", "score": 0, "max_score": 2}, "score": 0, "recommendations": ["Add FAQ section with FAQPage schema targeting questions users ask AI about your topic"]}

    def _check_data_density(self, text: str) -> Dict[str, Any]:
        """Check for statistics, numbers, and data points."""
        stats = re.findall(r'\d+(?:\.\d+)?%|\$[\d,.]+\b|\d{1,3}(?:,\d{3})+\b', text)
        word_count = len(text.split())
        density = (len(stats) / max(word_count, 1)) * 1000  # per 1000 words

        if density >= 5:
            return {"check": {"name": "Data & Statistics Density", "status": "PASS", "detail": f"{len(stats)} data points found ({density:.1f} per 1K words)", "score": 2, "max_score": 2}, "score": 2}
        elif density >= 2:
            return {"check": {"name": "Data & Statistics Density", "status": "PARTIAL", "detail": f"{len(stats)} data points ({density:.1f} per 1K words)", "score": 1, "max_score": 2}, "score": 1, "recommendations": ["Add more statistics and data points — Princeton research shows this improves AI visibility 30-40%"]}
        return {"check": {"name": "Data & Statistics Density", "status": "FAIL", "detail": f"Low data density ({len(stats)} points)", "score": 0, "max_score": 2}, "score": 0, "recommendations": ["Embed statistics, percentages, and data points throughout your content to boost AI citation rates"]}

    def _check_source_citations(self, soup) -> Dict[str, Any]:
        """Check for outbound authority citations."""
        if not soup:
            return {"check": {"name": "Source Citations", "status": "WARN", "detail": "Could not parse", "score": 0, "max_score": 2}, "score": 0}

        external_links = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.startswith("http") and not re.search(r'(facebook|twitter|linkedin|instagram|youtube)\.com', href):
                external_links.append(href)

        if len(external_links) >= 5:
            return {"check": {"name": "Source Citations", "status": "PASS", "detail": f"{len(external_links)} outbound authority links", "score": 2, "max_score": 2}, "score": 2}
        elif external_links:
            return {"check": {"name": "Source Citations", "status": "PARTIAL", "detail": f"Only {len(external_links)} outbound links", "score": 1, "max_score": 2}, "score": 1, "recommendations": ["Cite more authoritative external sources to signal credibility to AI"]}
        return {"check": {"name": "Source Citations", "status": "FAIL", "detail": "No outbound authority citations", "score": 0, "max_score": 2}, "score": 0, "recommendations": ["Add citations to authoritative sources — AI systems trust content that cites its sources"]}

    def _check_expert_quotes(self, text: str) -> Dict[str, Any]:
        """Check for expert quotes and attributions."""
        quote_patterns = [
            r'"[^"]{20,}"',  # Quoted text
            r'\u201c[^\u201d]{20,}\u201d',  # Smart quotes
            r'according to\s+\w+',
            r'says?\s+\w+\s+\w+,?\s+(CEO|CTO|VP|Director|Professor|Dr\.)',
            r'(CEO|CTO|VP|Director|Professor|Dr\.)\s+\w+\s+\w+\s+says?',
        ]
        quote_count = sum(len(re.findall(p, text, re.I)) for p in quote_patterns)

        if quote_count >= 3:
            return {"check": {"name": "Expert Quotes", "status": "PASS", "detail": f"{quote_count} expert quotes/attributions detected", "score": 2, "max_score": 2}, "score": 2}
        elif quote_count >= 1:
            return {"check": {"name": "Expert Quotes", "status": "PARTIAL", "detail": f"Only {quote_count} quotes found", "score": 1, "max_score": 2}, "score": 1, "recommendations": ["Add more expert quotes with attribution — this boosts AI citation likelihood"]}
        return {"check": {"name": "Expert Quotes", "status": "FAIL", "detail": "No expert quotes detected", "score": 0, "max_score": 2}, "score": 0, "recommendations": ["Include expert quotes with name and title attribution in your content"]}

    def _check_content_depth(self, text: str, soup) -> Dict[str, Any]:
        """Check content depth (word count, comprehensiveness)."""
        word_count = len(text.split())

        if word_count >= 2000:
            return {"check": {"name": "Content Depth", "status": "PASS", "detail": f"{word_count} words — comprehensive depth", "score": 2, "max_score": 2}, "score": 2}
        elif word_count >= 800:
            return {"check": {"name": "Content Depth", "status": "PARTIAL", "detail": f"{word_count} words — moderate depth", "score": 1, "max_score": 2}, "score": 1, "recommendations": ["Expand cornerstone content to 2000+ words for better AI citation chances"]}
        return {"check": {"name": "Content Depth", "status": "FAIL", "detail": f"Only {word_count} words — too thin for AI citation", "score": 0, "max_score": 2}, "score": 0, "recommendations": ["Significantly expand content depth — AI systems prefer comprehensive sources"]}

    def _check_heading_hierarchy(self, soup) -> Dict[str, Any]:
        """Check for proper heading hierarchy (H1 > H2 > H3)."""
        if not soup:
            return {"check": {"name": "Heading Hierarchy", "status": "WARN", "detail": "Could not parse", "score": 0, "max_score": 2}, "score": 0}

        h1s = soup.find_all("h1")
        h2s = soup.find_all("h2")
        h3s = soup.find_all("h3")

        has_single_h1 = len(h1s) == 1
        has_h2s = len(h2s) >= 3
        has_h3s = len(h3s) >= 1

        signals = sum([has_single_h1, has_h2s, has_h3s])
        if signals >= 3:
            return {"check": {"name": "Heading Hierarchy", "status": "PASS", "detail": f"Clean hierarchy: 1 H1, {len(h2s)} H2s, {len(h3s)} H3s", "score": 2, "max_score": 2}, "score": 2}
        elif signals >= 2:
            return {"check": {"name": "Heading Hierarchy", "status": "PARTIAL", "detail": f"{len(h1s)} H1s, {len(h2s)} H2s, {len(h3s)} H3s", "score": 1, "max_score": 2}, "score": 1, "recommendations": ["Improve heading hierarchy: 1 H1, multiple H2s, H3s for sub-sections"]}
        return {"check": {"name": "Heading Hierarchy", "status": "FAIL", "detail": "Poor heading structure", "score": 0, "max_score": 2}, "score": 0, "recommendations": ["Restructure headings: single H1, descriptive H2s for sections, H3s for sub-topics"]}
