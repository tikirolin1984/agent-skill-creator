# Architectural Decisions

Key architectural and design decisions for the AI Search Audit Skill.

---

## Decision 1: Simple Skill Architecture

**Decision:** Implemented as a Simple Skill with single focused objective.

**Rationale:**
- One clear purpose: audit + optimize AI search visibility
- All 7 pillars serve a unified goal
- Easier to maintain as a single cohesive tool

**Rejected:** Skill Suite with separate sub-skills per pillar — too fragmented for users.

---

## Decision 2: 7-Pillar Framework

**Decision:** Structure audit around 7 distinct pillars covering technical → strategic.

**Pillars:**
1. Technical Crawlability
2. Content Extractability
3. Entity Authority
4. Multi-Model Optimization
5. Citation & Mention Velocity
6. Content Freshness & Originality
7. Cross-Channel Authority

**Rationale:**
- Covers full spectrum from technical foundations to strategic positioning
- Each pillar is independently scoreable
- Maps to Forbes Agency Council's AI search dominance framework
- Enables phased implementation (technical quick wins → strategic plays)

---

## Decision 3: Normalized 100-Point Scoring

**Decision:** Normalize 7-pillar raw scores (90 max) to a 0-100 GEO Readiness Score.

**Rationale:**
- 100-point scale is universally understood
- Enables benchmarking across industries
- Grade labels (Leader/Ready/Developing/Vulnerable/Invisible) provide instant interpretation
- Weighted scoring reflects pillar importance (Technical/Content/Entity weighted higher)

---

## Decision 4: Pass/Partial/Fail Per Check

**Decision:** Each individual check scores Pass (full points), Partial (half), or Fail (zero).

**Rationale:**
- Binary pass/fail misses nuance (partial implementations deserve credit)
- Three-tier scoring provides clear improvement targets
- Simple enough to understand at a glance

---

## Decision 5: Platform-Specific Multi-Model Analysis

**Decision:** Audit each AI platform separately based on documented behavioral differences.

**Platform behaviors documented:**
- ChatGPT: Bing index, FAQ/Article schema preference
- Perplexity: Internal query generation, multi-source aggregation
- Google AI Overviews: GSC schema validation, ~60% query coverage
- Gemini: Paragraph-level extraction
- Claude: Factual/source-cited content preference
- Copilot: Heavy Bing dependency

**Rationale:**
- One-size-fits-all optimization misses platform nuances
- Platform-specific recommendations are more actionable
- As AI search diversifies, platform-specific strategy becomes critical

---

## Decision 6: Effort/Impact Prioritization for Roadmap

**Decision:** Classify all recommendations by effort (low/medium/high) and impact (low/medium/high).

**Rationale:**
- Users need to know what to do first
- Quick wins build momentum and prove value
- Strategic plays need time investment — shouldn't block quick progress

**Timeline phases:**
- Week 1-2: Quick wins (low effort, high impact)
- Month 1: Foundation building (medium effort, high impact)
- Month 2-3: Strategic plays (higher effort, compounding impact)
- Ongoing: Measurement and iteration

---

## Decision 7: Graceful Degradation Without APIs

**Decision:** Skill works without external API access by analyzing public-facing website data.

**What works without APIs:**
- robots.txt analysis
- llms.txt detection
- Schema markup extraction
- Content structure analysis
- HTML-based entity signals
- Cross-channel link analysis

**What requires manual/API input:**
- Live AI platform querying (SoM measurement)
- Real-time citation tracking
- Competitive mention monitoring

**Rationale:**
- Maximum value with zero setup
- API-dependent features provided as frameworks/methodologies
- Users can layer in API access incrementally

---

## Decision 8: Minimal Dependencies

**Decision:** Only 4 Python dependencies: requests, beautifulsoup4, lxml, tldextract.

**Rationale:**
- Lightweight installation
- Widely available packages
- No API keys required for core functionality
- Each dependency earns its place with clear necessity

---

## Decision 9: Share of Model as Primary Metric

**Decision:** SoM (Share of Model) as the north-star metric for AI search visibility.

**Formula:** SoM = (Your brand mentions / Total all-brand mentions) × 100

**Rationale:**
- Analogous to Share of Voice (familiar to marketers)
- Captures competitive positioning, not just absolute presence
- Trackable over time for trend analysis
- Industry-standard metric emerging in GEO field

---

**Document Version:** 1.0
**Last Updated:** 2026-03-23
