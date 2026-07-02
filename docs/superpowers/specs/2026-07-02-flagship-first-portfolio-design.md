# Flagship-First Portfolio Restructure — Design

**Date:** 2026-07-02
**Goal:** Restructure the portfolio around QA Automation AI Enabler as the single flagship project, demote other projects into a supporting tier and a compact list, and fix credibility bugs found during review.

## Why

The current site renders all 11 projects as visually equal cards on both the homepage ("Featured Projects") and the projects page. Nothing stands out, the weakest projects (two generic pages from an older site era) drag down the strongest, and nine AI-flavored projects blur into one story. Reviewers give a portfolio under a minute — the flagship must be unmissable.

## The unified flagship story

Verified against the actual `QAAutomationAIEnabler` codebase (PROJECT_SUMMARY.md, backend/, core/, mcp_servers/, modules/):

> **Record → AI-generate → self-heal → sync to Jira/Zephyr.**
> An AI-powered QA platform that records browser interactions with Playwright, generates production-ready test code through a 3-layer deterministic + AI pipeline (SelectorResolver → CodeBuilder → AIEnrichment) with multi-LLM enhancement (Claude + GPT-4o + Grok), self-heals broken tests via a 4-agent LangGraph pipeline, learns from failures (ChromaDB pattern learning), and pushes test cases to Jira and Zephyr Scale — automated end-to-end with n8n workflows.

**Canonical name everywhere:** "QA Automation AI Enabler"
**Canonical metrics:** 50K+ LOC · 72 FastAPI endpoints · 18 AI agents · Jira + Zephyr integrated

## Project tiers

| Tier | Projects | Treatment |
|------|----------|-----------|
| Flagship | QA Automation AI Enabler | Dedicated homepage section with demo video; hero card on projects page; full case-study page (existing, updated) |
| Supporting (3) | Playwright BDD Framework, Multi-Agent Orchestration, QA RAG System | Regular cards on homepage + projects page; keep detail pages |
| More work (5) | GenAI QA Automation, AI-Enabled API Automation, AI Gig Discovery, JIRA Data Analysis, Jira-TestRail Integration | One-line entries (name + one-liner + tags) in a compact "More Work" list on projects page only; keep detail pages, linked from list |
| Removed (2) | E-Commerce Testing (qa-automation-1), API Testing Suite (qa-automation-2) | Delete directories; remove from all listings |

## Changes by file

### `index.html` (homepage)
- Replace the "Featured Projects" grid section with:
  1. **Flagship section** — section title ("Flagship Project" label), unified pitch copy, the existing demo video (`assets/videos/ai-enabled-qa-demo.mp4` + poster, reusing the `.kc-video` player), a 4-metric strip (50K+ LOC / 72 API endpoints / 18 AI agents / Jira + Zephyr), primary CTA "Read the Full Case Study" → `projects/ai-enabled-qa/`.
  2. **Supporting cards** — the 3 supporting projects as `.kc-card`s, then a "View All Projects" outline button (kept).
- Stats bar: replace "∞ Cups of Coffee → Code" with "18 AI Agents Built" (honest, counter-animatable).
- Footer "Top Projects": QA Automation AI Enabler first, then the 3 supporting projects.

### `pages/projects.html`
- Remove duplicated header (two identical subtitle blocks at lines ~48–59) — keep one.
- Remove category filter buttons (pointless with 4 cards).
- New structure: flagship hero card (wide card, short pitch, metrics, video poster image or icon, "Case Study" CTA) → 3 supporting cards → "More Work" compact list (one line each: name, one-liner, tags, link to detail page).

### `js/script.js`
- Restructure `LOCAL_PROJECTS` into tiers (e.g. `FLAGSHIP`, `SUPPORTING`, `MORE_WORK`) or add a `tier` field.
- `renderLocalProjects()` renders per-page: homepage grid gets only the 3 supporting cards (flagship section is static HTML); projects page renders flagship hero + supporting cards + more-work list.
- Remove qa-automation-1/2 entries. Remove filter logic if no longer used (`initFilters` can stay dormant or be deleted).
- Update flagship card description to the unified story.

### `projects/ai-enabled-qa/index.html` (flagship case study)
- Fix **"View Source Code" button pointing to `https://github.com/vipinyadav` (someone else's profile)**. Point to the real repo if public, otherwise remove the button and keep "Explore Architecture".
- Add a **"Jira & Zephyr Integration"** section/feature block: Jira ticket sync, AI Jira test-case generator, Zephyr Scale push, n8n Jira→Tests workflow.
- Align hero copy with the unified story (mention Jira/Zephyr in the pitch).

### Other project pages
Verified 2026-07-02: the only public repos on the account are `barsanataxiservice`, `claude-flow`, `PlaywriteFramework`, `skills`. **Every "source code" link on the site 404s**, including `AIEnabledAPIAutomation`, `PlaywrightDemoProject`, `gig-automation`, and all links to `YdvVipin/portfolio` (private).
- Remove all GitHub source-code buttons/links from project pages until the corresponding repo is actually public. The case-study pages stand on their own.
- If/when repos are made public later, links can be restored.

### `README.md`
- Rewrite Highlights: flagship first with unified one-liner and metrics, then the 3 supporting projects, then "plus more" line pointing at projects page. Remove references to deleted projects.

### Site-wide
- Footer year: 2025 → 2026 (all pages).
- Delete `projects/qa-automation-1/` and `projects/qa-automation-2/`; remove any inbound links; update `sitemap.xml`.
- Consistent flagship naming ("QA Automation AI Enabler") across index, cards, footer, README, case-study page.

## Critical: the site is not live

Verified 2026-07-02: `YdvVipin/portfolio` is **private** and GitHub Pages is **not enabled** — `https://ydvvipin.github.io/portfolio/` returns 404. The README, OG tags, sitemap, and canonical URLs all advertise a dead URL.

**Go-live plan (needs user decision):** make the repo public and enable Pages (free), or deploy to Netlify/Vercel/Cloudflare Pages from the private repo. Before making the repo public, remove/relocate non-portfolio content that should not be published: `scripts/generate_ats_resume.py` + `scripts/output/` (a third party's resume and generator, including an `apply_evasion` zero-width-character feature that would be publicly visible), `analysis/` Jira tooling if it contains client data, `.playwright-mcp/` logs, and git history review if needed.

## Non-goals
- No visual redesign, new frameworks, or new pages — reuse existing `.kc-*` components and CSS (new small CSS only for the flagship section/metric strip and more-work list, added to `style-enhancements.css`).
- No changes to About / Journey / Resume / Contact content (they have uncommitted edits from other work — leave untouched).
- No changes to the `scripts/` resume generator or `analysis/` tooling.

## Testing
- Serve locally, verify with Playwright browser: homepage flagship section renders with playable video, exactly 3 supporting cards, projects page shows tiered layout, more-work links resolve, no 404s to deleted pages, no console errors.
- Check mobile width (375px) for the new flagship section and metric strip.
- Verify all GitHub links resolve to the correct account (`YdvVipin`).
