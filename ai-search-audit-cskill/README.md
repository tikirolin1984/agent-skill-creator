# AI Search Audit Skill

Comprehensive AI search visibility audit and GEO (Generative Engine Optimization) framework for brand dominance across ChatGPT, Perplexity, Google AI Overviews, Claude, Copilot, and Gemini.

## What It Does

Audits any website or brand across **7 pillars** and generates a **GEO Readiness Score (0-100)** with a prioritized optimization roadmap.

### The 7 Pillars

| # | Pillar | What It Checks |
|---|--------|---------------|
| 1 | **Technical Crawlability** | robots.txt, llms.txt, JSON-LD schema, SSR, sitemap, noindex |
| 2 | **Content Extractability** | Answer-first structure, FAQ schema, data density, citations, quotes |
| 3 | **Entity Authority** | Organization schema, sameAs linking, author markup, topical depth |
| 4 | **Multi-Model Optimization** | Platform-specific readiness (ChatGPT, Perplexity, Gemini, etc.) |
| 5 | **Citation & Mention Velocity** | Share of Model, mention rate, citation rate, competitive SoM |
| 6 | **Content Freshness** | Timestamps, copyright currency, original research, content decay |
| 7 | **Cross-Channel Authority** | Social presence, press mentions, reviews, community signals |

### GEO Readiness Grades

- **85-100:** AI Search Leader
- **70-84:** AI Search Ready
- **50-69:** AI Search Developing
- **30-49:** AI Search Vulnerable
- **0-29:** AI Search Invisible

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Full audit
python scripts/main.py https://example.com --brand "Your Brand" --depth full

# Quick technical check only
python scripts/main.py https://example.com --check technical

# With competitors
python scripts/main.py https://example.com --brand "Your Brand" --competitors comp1.com comp2.com

# Output to file
python scripts/main.py https://example.com --output my_audit.json
```

## Usage with Claude

Just ask naturally:

- "Audit my website example.com for AI search visibility"
- "How visible is my brand in ChatGPT and Perplexity?"
- "Check if my robots.txt blocks AI crawlers"
- "Create an AI search dominance strategy for my brand"
- "Compare my AI visibility against competitor.com"

## Output

The audit generates:

1. **GEO Readiness Score** — Single 0-100 score with grade
2. **Pillar Breakdown** — Score per pillar with pass/partial/fail per check
3. **Top Recommendations** — Prioritized by effort vs. impact
4. **Optimization Roadmap** — Phased: Quick Wins → Foundation → Strategic → Ongoing

## Key Metrics

| Metric | Target |
|--------|--------|
| Share of Model (SoM) | >30% in your niche |
| Mention Rate | >25% of relevant queries |
| Citation Rate | >15% with URL cited |
| Schema Coverage | >80% of pages |
| Crawler Access | 100% AI crawlers allowed |
| Content Freshness | >60% updated within 6 months |

## Dependencies

- `requests` — HTTP fetching
- `beautifulsoup4` — HTML parsing
- `lxml` — XML parsing
- `tldextract` — Domain parsing

## Sources & Methodology

Built on research from:
- Forbes Agency Council: AI Search Dominance Framework (2026)
- Princeton University GEO Research (citations/stats improve visibility 30-40%)
- Brandlight: Google-AI citation overlap dropped from 70% to <20%
- Industry data: ChatGPT 800M+ weekly users, Perplexity 780M monthly queries
- GEO market: $848M (2025) → projected $33.7B by 2034

---

**Version:** 1.0.0 | **Created:** 2026-03-23
