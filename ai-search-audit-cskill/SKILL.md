# AI Search Audit Skill

**Version:** 1.0.0
**Type:** Simple Skill
**Architecture:** Simple Skill (Single focused objective)
**Created by:** Agent-Skill-Creator v2.1

---

## Overview

The **AI Search Audit Skill** is a comprehensive framework for auditing and optimizing brand visibility across AI-powered search platforms — ChatGPT, Google AI Overviews, Perplexity, Claude, Copilot, and Gemini.

Traditional SEO got you ranked among 10 blue links. GEO (Generative Engine Optimization) gets you cited in the 2-7 sources AI models reference when answering questions. This skill bridges the gap from concept to execution.

### The Problem

- 50% of consumers now use AI-powered search
- Only 12% of ChatGPT citations match Google's first page URLs
- AI referral traffic surged 527% in 2025
- Traditional search traffic projected to drop 25% by 2026
- Most brands have zero visibility into how AI engines perceive them

### The Solution: 7-Pillar Audit Framework

This skill implements a complete audit-to-optimization pipeline built on 7 pillars derived from industry research and the Forbes Agency Council's AI search dominance framework:

1. **Technical Crawlability** — Can AI bots actually read your site?
2. **Content Extractability** — Is your content structured for AI synthesis?
3. **Entity Authority** — Does AI recognize your brand as an authority?
4. **Multi-Model Optimization** — Are you optimized for each AI platform's unique behavior?
5. **Citation & Mention Velocity** — How often does AI cite you vs. competitors?
6. **Content Freshness & Originality** — Do you have content worth citing?
7. **Cross-Channel Authority Signals** — Do third-party signals reinforce your brand?

---

## Core Capabilities

### 1. Technical Crawlability Audit

Analyzes whether AI systems can actually access and read your content.

**Checks performed:**
- `robots.txt` analysis for AI crawler directives (GPTBot, ClaudeBot, PerplexityBot, Google-Extended, Amazonbot, Applebot-Extended, Bytespider, CCBot)
- `llms.txt` presence and quality assessment
- JSON-LD structured data validation (Organization, Article, FAQPage, HowTo, Product, BreadcrumbList schemas)
- Server-side rendering check (JavaScript-hidden content detection)
- XML sitemap freshness and completeness
- Page load performance for crawler efficiency
- Cloudflare/WAF AI bot blocking detection
- `noindex` / `nofollow` tag audit on key pages

**Scoring:** Each check is scored Pass (2pts) / Partial (1pt) / Fail (0pts). Maximum 16 points.

**Output example:**
```
TECHNICAL CRAWLABILITY SCORE: 11/16 (69% - Needs Improvement)

[PASS] robots.txt allows GPTBot
[PASS] robots.txt allows PerplexityBot
[FAIL] robots.txt blocks ClaudeBot (User-agent: ClaudeBot / Disallow: /)
[FAIL] No llms.txt file detected at /llms.txt
[PASS] JSON-LD Organization schema present
[PARTIAL] FAQPage schema found but missing 3 recommended properties
[PASS] Server-side rendered content detected
[FAIL] XML sitemap last modified 8 months ago
```

### 2. Content Extractability Audit

Evaluates whether your content is structured for AI synthesis and citation.

**Checks performed:**
- Answer-first / TLDR-first structure (first 200 words contain direct answer)
- Question-based H2 headings matching AI query patterns
- FAQ blocks with proper schema markup
- Statistic and data point density
- Source citation presence (outbound authority signals)
- Expert quote inclusion
- Content depth scoring (word count, heading hierarchy, section completeness)
- Inverted pyramid structure validation

**Key insight:** Princeton research shows citing sources, adding statistics, and including expert quotes can improve AI visibility by 30-40%.

**Scoring:** Maximum 16 points across 8 checks.

### 3. Entity Authority Assessment

Measures whether AI systems recognize your brand as a distinct, authoritative entity.

**Checks performed:**
- Knowledge Graph presence (Google Knowledge Panel)
- `sameAs` schema linking (Wikipedia, Wikidata, social profiles)
- Topical coverage depth (content cluster completeness)
- Author entity markup (person schema, author pages)
- Brand consistency across web properties
- Wikipedia/Wikidata entity existence
- Unlinked brand mention volume
- Industry-specific authority signals

**Key insight:** Brands with comprehensive topical coverage get cited 6.2x more often. Unlinked brand mentions carry weight — AI systems give mentions credit even without links.

**Scoring:** Maximum 16 points across 8 checks.

### 4. Multi-Model Optimization Analysis

Each AI platform has unique extraction and citation behaviors. This pillar audits platform-specific readiness.

**Platform-specific behaviors:**

| Platform | Behavior | Optimization Priority |
|----------|----------|----------------------|
| **ChatGPT** | Falls back to English sources even for non-English queries; values FAQPage + Article schema; uses Bing index | FAQPage schema, Article schema, Bing indexing |
| **Google AI Overviews** | Appears in ~60% of searches; prefers pages with valid Search Console schema | Valid schema in GSC, featured snippet optimization |
| **Perplexity** | Generates internal search queries before answering; aggregates multiple sources per response | Organization + Product schema, multiple angle coverage |
| **Gemini** | Performs paragraph-level text extraction | Clean paragraph structure, scannable formatting |
| **Claude** | Prioritizes well-structured, factual content | Source citations, data-rich content |
| **Copilot** | Leverages Bing index heavily | Bing Webmaster Tools optimization |

**Scoring:** Maximum 12 points across 6 platform checks.

### 5. Citation & Mention Velocity Measurement

Tracks how often AI platforms cite your brand relative to competitors.

**Metrics tracked:**
- **Mention Rate:** % of relevant AI queries where your brand appears
- **Citation Rate:** % where your content URL is listed as source
- **Average Position:** Your rank within multi-brand AI responses
- **Share of Model (SoM):** Primary metric — how often your brand appears vs. competitors for relevant queries
- **Sentiment Analysis:** Positive/neutral/negative tone in AI mentions

**Methodology:**
1. Define 20-50 industry-relevant queries users would ask AI
2. Query each AI platform with those prompts
3. Record brand mentions, citations, and positions
4. Calculate SoM = (Your mentions / Total competitor mentions) x 100
5. Track velocity over time (weekly/monthly delta)

**Scoring:** Maximum 10 points based on SoM percentile vs. industry benchmarks.

### 6. Content Freshness & Originality Audit

AI platforms prefer current, original content with unique data.

**Checks performed:**
- "Last updated" timestamps on cornerstone content
- Content age distribution (% of content updated within 6 months)
- Original research / proprietary data presence
- Unique frameworks, methodologies, or datasets
- First-to-publish signals on key topics
- Content decay detection (outdated statistics, broken references)

**Key insight:** A 2024 guide with no updates will lose ground to a 2026 article. Original research and proprietary data attract citations because AI engines need unique sources.

**Scoring:** Maximum 10 points across 5 checks.

### 7. Cross-Channel Authority Signals

AI systems don't just look at your website — they evaluate your entire digital footprint.

**Checks performed:**
- PR-driven credibility (editorial mentions in authoritative publications)
- Social reinforcement signals (consistent brand presence)
- Third-party review site presence and ratings
- Industry award / certification mentions
- Podcast / video transcript citations
- Community engagement signals (Reddit, Quora, Stack Overflow mentions)

**Key insight:** Brands cited by independent editorial sources achieve measurably higher AI recommendation rates than brands relying solely on owned content.

**Scoring:** Maximum 10 points across 5 checks.

---

## The 50-Point GEO Readiness Score

All 7 pillars combine into a single **GEO Readiness Score** out of 100:

| Pillar | Max Points | Weight |
|--------|-----------|--------|
| Technical Crawlability | 16 | High |
| Content Extractability | 16 | High |
| Entity Authority | 16 | High |
| Multi-Model Optimization | 12 | Medium |
| Citation & Mention Velocity | 10 | Medium |
| Content Freshness & Originality | 10 | Medium |
| Cross-Channel Authority | 10 | Medium |
| **TOTAL** | **90 → normalized to 100** | |

**Score Interpretation:**
- **85-100: AI Search Leader** — Your brand is well-positioned for AI search dominance
- **70-84: AI Search Ready** — Strong foundation, optimize specific gaps
- **50-69: AI Search Developing** — Significant opportunities for improvement
- **30-49: AI Search Vulnerable** — Major gaps risk competitive disadvantage
- **0-29: AI Search Invisible** — Urgent action needed

---

## Audit Pipeline

```
Input (URL/Domain/Brand)
    │
    ▼
┌─────────────────────┐
│  1. Technical Audit  │ → robots.txt, llms.txt, schema, SSR, sitemap
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│  2. Content Audit    │ → Structure, extractability, FAQ, data density
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│  3. Entity Audit     │ → Knowledge Graph, sameAs, topical depth
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│  4. Multi-Model Audit│ → ChatGPT/Perplexity/Gemini/AIO specifics
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│  5. Citation Audit   │ → SoM, mention rate, citation rate, position
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│  6. Freshness Audit  │ → Content age, originality, unique data
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│  7. Cross-Channel    │ → PR, social, reviews, community signals
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│  Score & Roadmap     │ → GEO Readiness Score + Prioritized Actions
└─────────────────────┘
```

---

## Usage Examples

### Full Audit
```
User: "Audit my website example.com for AI search visibility"

Skill performs complete 7-pillar audit, generates:
- 50-point GEO Readiness Score
- Pillar-by-pillar breakdown with pass/partial/fail for each check
- Top 10 prioritized optimizations ranked by effort vs. impact
- Implementation timeline (quick wins in week 1, strategic plays months 2-3)
```

### Competitive Benchmark
```
User: "Compare my AI search visibility against competitor1.com and competitor2.com"

Skill performs SoM analysis:
- Defines 30 industry-relevant queries
- Measures citation/mention rates per brand per platform
- Generates visibility matrix: brands × platforms
- Identifies where competitors are cited and you're not
- Recommends content gaps to close
```

### Technical Quick Check
```
User: "Check if my robots.txt blocks AI crawlers"

Skill performs focused technical audit:
- Fetches robots.txt
- Checks all known AI crawler user-agents
- Reports which are allowed/blocked
- Provides corrected robots.txt snippet
```

### Strategy Development
```
User: "Create an AI search dominance strategy for my SaaS brand"

Skill generates:
- Current state assessment (abbreviated audit)
- Industry benchmark context
- 90-day optimization roadmap
- Content calendar for GEO-optimized content
- Technical implementation checklist
- Measurement framework with KPIs
```

---

## Optimization Roadmap Template

After audit, the skill generates a prioritized roadmap:

### Quick Wins (Week 1-2, Low Effort, High Impact)
1. Fix robots.txt to allow AI crawlers (GPTBot, ClaudeBot, PerplexityBot)
2. Add llms.txt file with brand context and content priorities
3. Add Organization JSON-LD schema with sameAs links
4. Add "Last updated" dates to top 10 pages
5. Restructure top 5 pages with answer-first pattern

### Foundation Building (Month 1, Medium Effort, High Impact)
6. Implement FAQPage schema on key service/product pages
7. Add Article schema to all blog posts with proper author markup
8. Create author bio pages with Person schema
9. Build topic cluster content maps for core topics
10. Add statistics, citations, and expert quotes to cornerstone content

### Strategic Plays (Month 2-3, Higher Effort, Compounding Impact)
11. Publish original research / benchmark study for your industry
12. Develop proprietary frameworks with unique naming
13. PR campaign targeting editorial mentions in authoritative publications
14. Build Wikidata entity and supporting Wikipedia content
15. Launch content refresh program (update all content >6 months old)

### Measurement & Iteration (Ongoing)
16. Weekly SoM tracking across top 20 queries
17. Monthly competitive benchmark updates
18. Quarterly full 7-pillar re-audit
19. Content freshness monitoring
20. AI citation alert system

---

## Technical Implementation

### Scripts Structure

```
ai-search-audit-cskill/
├── scripts/
│   ├── main.py                    # Orchestrator
│   ├── auditors/
│   │   ├── technical_auditor.py   # Pillar 1: Crawlability
│   │   ├── content_auditor.py     # Pillar 2: Extractability
│   │   ├── entity_auditor.py      # Pillar 3: Authority
│   │   ├── multimodel_auditor.py  # Pillar 4: Platform-specific
│   │   ├── citation_auditor.py    # Pillar 5: SoM & mentions
│   │   ├── freshness_auditor.py   # Pillar 6: Content age
│   │   └── crosschannel_auditor.py# Pillar 7: External signals
│   ├── analyzers/
│   │   ├── robots_analyzer.py     # robots.txt parsing
│   │   ├── schema_analyzer.py     # JSON-LD validation
│   │   ├── content_structure.py   # Content pattern analysis
│   │   └── competitor_analyzer.py # Competitive benchmarking
│   └── generators/
│       ├── score_calculator.py    # GEO Readiness Score
│       ├── report_generator.py    # Audit report output
│       └── roadmap_generator.py   # Prioritized action plan
```

### Dependencies

- `requests` — HTTP fetching for target sites
- `beautifulsoup4` — HTML parsing and content extraction
- `lxml` — XML/HTML parsing (sitemap, schema)
- `extruct` — Structured data extraction (JSON-LD, microdata, RDFa)
- `tldextract` — Domain parsing
- `trafilatura` — Main content extraction

---

## AI Crawler User-Agent Reference

| Crawler | Company | User-Agent String |
|---------|---------|-------------------|
| GPTBot | OpenAI | `GPTBot` |
| ChatGPT-User | OpenAI | `ChatGPT-User` |
| ClaudeBot | Anthropic | `ClaudeBot` |
| PerplexityBot | Perplexity | `PerplexityBot` |
| Google-Extended | Google | `Google-Extended` |
| Amazonbot | Amazon | `Amazonbot` |
| Applebot-Extended | Apple | `Applebot-Extended` |
| Bytespider | ByteDance | `Bytespider` |
| CCBot | Common Crawl | `CCBot` |
| Cohere-ai | Cohere | `cohere-ai` |
| Meta-ExternalAgent | Meta | `Meta-ExternalAgent` |

---

## llms.txt Specification

The `llms.txt` file (placed at site root) tells AI systems how to interpret your brand:

```markdown
# Brand Name

> One-line brand description

## About
Brief brand overview, mission, and core value proposition.

## Core Topics
- Topic 1: Description
- Topic 2: Description

## Key Pages
- [Product Page](https://example.com/product): Description
- [About Us](https://example.com/about): Description
- [Blog](https://example.com/blog): Description

## Contact
- Website: https://example.com
- Support: support@example.com
```

---

## Schema Markup Priority Guide

### Tier 1 (Must-Have, implement first)
- **Organization** — Brand entity with sameAs links
- **Article** — Blog posts and content pages with author
- **FAQPage** — Service/product pages with Q&A
- **BreadcrumbList** — Site navigation structure

### Tier 2 (Should-Have, implement month 1)
- **HowTo** — Tutorial and guide content
- **Product** — E-commerce product pages
- **Person** — Author bio pages
- **WebSite** — Site-level search action

### Tier 3 (Nice-to-Have, implement month 2+)
- **Event** — Industry events, webinars
- **VideoObject** — Video content
- **Dataset** — Original research data
- **ClaimReview** — Fact-check content

---

## Key Metrics Glossary

| Metric | Definition | Target |
|--------|-----------|--------|
| **Share of Model (SoM)** | % of relevant queries where your brand appears vs. competitors | >30% in your niche |
| **Mention Rate** | % of relevant AI queries that mention your brand | >25% |
| **Citation Rate** | % of queries where your URL is listed as source | >15% |
| **Average Position** | Your rank within multi-brand AI responses | Top 3 |
| **GEO Readiness Score** | 100-point audit score across 7 pillars | >70 |
| **Content Freshness Ratio** | % of content updated within 6 months | >60% |
| **Schema Coverage** | % of pages with valid JSON-LD | >80% |
| **Crawler Access Score** | % of AI crawlers allowed in robots.txt | 100% |

---

## Competitive Analysis Framework

### Step 1: Define Query Universe
Identify 20-50 queries your ideal customer would ask AI:
- "What is the best [your category] tool?"
- "Compare [your brand] vs [competitor]"
- "[Industry] best practices 2026"
- "How to solve [problem your product solves]"

### Step 2: Multi-Platform Query Execution
Run each query across:
- ChatGPT (GPT-4o)
- Perplexity
- Google (check for AI Overviews)
- Claude
- Copilot

### Step 3: Record & Score
For each query × platform combination, record:
- Was your brand mentioned? (Y/N)
- Was your URL cited? (Y/N)
- What position? (1st, 2nd, 3rd, etc.)
- Sentiment? (Positive/Neutral/Negative)
- Which competitors were mentioned instead?

### Step 4: Calculate SoM
```
Your SoM = (Your total mentions across all queries & platforms) /
           (Total mentions for all tracked brands) × 100
```

### Step 5: Gap Analysis
Identify queries where competitors are cited and you're not. These are your highest-impact content opportunities.

---

## Sources & Research

This skill's methodology is synthesized from:

- Forbes Agency Council: "7 Ways to Prepare Your Brand for AI Search Dominance in 2026"
- Princeton University GEO research: Source citations, statistics, and quotations improve AI visibility 30-40%
- Brandlight research: Overlap between Google top links and AI-cited sources dropped from 70% to below 20%
- GEO market data: $848M (2025) → projected $33.7B by 2034 (50.5% CAGR)
- Industry benchmarks: ChatGPT 800M+ weekly users, Perplexity 780M monthly queries, AI Overviews in ~60% of searches
- Multi-source 2026 GEO frameworks from Search Engine Land, Semrush, and specialist GEO publications

---

## Error Handling & Recovery

- **Target site unreachable:** Report which checks could not be performed, score remaining pillars, flag incomplete audit
- **robots.txt not found:** Score as "no restrictions" but flag as potential issue (some CDNs serve default blocks)
- **Schema parsing failure:** Fall back to regex-based structured data detection
- **Rate limiting:** Implement exponential backoff for multi-page crawls
- **Partial results:** Always generate report with available data rather than failing entirely

---

## Quality Standards

- All audit checks produce deterministic, reproducible results
- Scoring methodology is transparent and documented
- No placeholder scores — every check runs real analysis
- Reports include specific, actionable recommendations (not generic advice)
- Competitive benchmarks use identical methodology across all brands
- All recommendations include effort level and expected impact

---

**Document Version:** 1.0
**Last Updated:** 2026-03-23
**Author:** Agent-Skill-Creator v2.1
