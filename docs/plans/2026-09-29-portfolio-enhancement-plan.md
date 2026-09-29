# Portfolio Enhancement Plan

**Date:** 2026-09-29
**Owner:** Vipin Yadav (reviewer / approver)
**Executor:** a coding agent working on branch `claude/optimistic-mayer-xysc5m`
**Goal:** Clean up the repo, retell the flagship as a Web + API + Mobile AI QA system with human review, and make the portfolio *prove* QA skill (self-testing site + live quality dashboard).

---

## 0. Ground rules for the executing agent

Read this section before touching anything.

1. **Stack stays as-is.** Plain static HTML/CSS/JS served by GitHub Pages from the repo root. No frameworks, no bundler, no build step for the site itself. Reuse the existing `kc-*` design system (`css/style.css`, `css/style-enhancements.css`) and tokens on `:root` (`--kc-accent`, `--kc-surface`, …).
2. **Dark mode must keep working.** The theme toggle lives in `js/script.js` → `initThemeToggle()` and adds `.kc-theme--dark` on `<html>`. Every new component needs a `:root.kc-theme--dark` override in `css/style-enhancements.css`.
3. **Never invent facts.** No made-up metrics, company names, client names, or features. Anything marked `⚠ NEEDS INPUT` must be filled from Vipin's answers (section 3.1) — if an answer is missing, leave an HTML comment `<!-- TODO(vipin): ... -->` and skip that element rather than guessing.
4. **No confidential employer data.** Nothing from Bright Order Inc. beyond what is already public on the site (company name, city, role). No internal URLs, customer names, screenshots of internal tools.
5. **One commit per phase** (or per task inside a big phase), conventional-commit style (`chore:`, `feat:`, `fix:`, `test:`, `docs:`). Push after each phase: `git push -u origin claude/optimistic-mayer-xysc5m`.
6. **Verify before every push:**
   - Serve locally: `python3 -m http.server 8000` from repo root.
   - Run the smoke suite once it exists (Phase 4).
   - Screenshot changed pages at **1280px and 375px**, light and dark, and check there is no horizontal scroll on mobile.
7. **When adding a page:** add it to the nav on *all* pages, to the footer "Quick Links", and to `sitemap.xml`.
8. **Never rewrite git history** (no force-push, no filter-repo) unless Vipin explicitly asks.

---

## Phase 1 — Repo hygiene (small, do first)

**Why:** 384 generated files (~9 MB of Allure raw results + committed `.pyc`) make the repo look unmaintained to any reviewer who opens it.

### Tasks
1. Stop tracking generated artifacts (keep files on disk untracked; they're ignored afterwards):
   ```bash
   git rm -r --cached projects/ai-enabled-api-automation/reports/allure-results
   git rm -r --cached $(git ls-files | grep __pycache__)
   ```
2. **Keep** `projects/ai-enabled-api-automation/reports/allure-report/` and the small `*_report.html` files — `projects/ai-enabled-api-automation/index.html:93` links to `reports/allure-report/index.html` as a live demo. Confirm the link still works after step 1.
3. Extend `.gitignore`:
   ```
   *.pyc
   **/allure-results/
   .pytest_cache/
   node_modules/
   test-results/
   playwright-report/
   ```
4. Wording fix in `pages/about.html:67`: `Bright Order Inc. — Toronto, ON` → `Bright Order Inc. — Toronto, ON (Remote)` so it matches the "based in India, working remotely" line used everywhere else.

### Done when
- `git ls-files | grep -cE "pycache|allure-results"` → `0`
- Allure report link on the API project page opens correctly.
- Commit: `chore: stop tracking generated test artifacts`

---

## Phase 2 — Privacy & contact decisions (tiny, needs Vipin)

`pages/contact.html` publishes a personal phone number (`+91 …`) and WhatsApp on a public site.

- ⚠ NEEDS INPUT: keep phone/WhatsApp public, or remove and keep email + LinkedIn only?
- ⚠ NEEDS INPUT: add a contact form? If yes, Vipin creates a free Formspree form and supplies the form ID. Agent then adds a `<form action="https://formspree.io/f/<ID>" method="POST">` card (name, email, message, honeypot field `_gotcha`) styled with existing `kc-contact-*` classes, with client-side required-field validation and a success/error message. Without an ID → skip.

Commit: `feat(contact): ...` or `chore(contact): ...`

---

## Phase 3 — Flagship retold: Web + API + Mobile with Human-in-the-Loop (biggest value)

**Why:** The flagship page (`projects/ai-enabled-qa/index.html`) presents a Playwright **web-only** tool. Vipin's actual direction is an **AI Enabler for Web, API and Mobile automation where a human reviews and fixes what the AI produces**. That human-review angle is a strength (trustworthy AI, not "magic") and should be the headline.

### 3.1 Questions Vipin must answer first (agent: stop and ask if not answered)

| # | Question | Used in |
|---|---|---|
| Q1 | Which layers exist today vs planned? (Web ✅ / API ? / Mobile ?) | badges "Live" vs "In progress" |
| Q2 | API layer: tools/libraries (e.g. requests/httpx, pytest, Behave, schema validation, OpenAPI import?) and what the AI does (generate tests from OpenAPI? from Jira stories?) | API section |
| Q3 | Mobile layer: Appium? Android/iOS? real devices/emulators/cloud (BrowserStack/Sauce)? What the AI does (locator generation, healing, test generation?) | Mobile section |
| Q4 | Human review step: where exactly does a human step in? (review generated tests before commit? approve self-healed locators? triage failures?) What UI/tool do they use (React dashboard, PR review, Jira)? | HITL section + diagram |
| Q5 | Any real numbers you're comfortable publishing? (tests generated, % healed automatically, time saved, review acceptance rate) | metrics strip — omit if none |
| Q6 | Are the existing metrics (50K+ LOC, 72 endpoints, 18 agents) still accurate? | hero + homepage |
| Q7 | Is the flagship code in a GitHub repo that can be shared (public) or referenced? | CTA button |

### 3.2 Changes

**`projects/ai-enabled-qa/index.html`** (keep existing sections; insert/adjust):
1. **Hero pitch** — rewrite to: *one AI-assisted QA system covering Web, API and Mobile, with a human reviewer in the loop*. Keep "Watch It In Action" video section as-is.
2. **New section "Three Surfaces, One Pipeline"** (after "Why This Exists"): 3 cards — Web (Playwright), API, Mobile — each with: what the AI does, what the human reviews, status badge (Live / In progress). Content from Q1–Q3.
3. **New section "Human in the Loop"** (before "Self-Healing Pipeline"): inline SVG flow diagram:
   `Source (recording / OpenAPI / Jira story) → AI generates tests → Human review gate (approve / edit / reject) → CI run → Failure → AI proposes heal → Human approves heal → Jira/Zephyr sync`
   - Diagram rules: inline `<svg>` with `viewBox`, colors via `currentColor` / CSS variables so it works in dark mode, `role="img"` + `<title>`/`<desc>` for accessibility, stacks vertically below 640px (provide a second vertical SVG or use CSS to swap).
   - Short text below: *why* human review — trust, no silent false positives, AI suggestions become training signal (only if true per Q4).
4. **Tech Stack section** — add API + Mobile tools from Q2/Q3.
5. **Metrics** — update only with confirmed numbers (Q5/Q6).

**Also update for consistency:**
- `js/script.js` → `FLAGSHIP_PROJECT.desc` and `tags` (e.g. add `Appium`, API tool).
- `index.html` → flagship `kc-flag__desc` paragraph (line ~162) and meta description if needed.
- `README.md` → flagship highlight bullet.
- `pages/projects.html` flagship hero card is rendered from `FLAGSHIP_PROJECT` — verify it looks right.

### Done when
- Flagship page shows all three surfaces + HITL diagram, correct in light/dark, 375px/1280px.
- Homepage, projects page, README use the same one-line pitch.
- No `TODO(vipin)` left unless Vipin agreed to ship without that item.
- Commit: `feat(flagship): retell as web+api+mobile with human-in-the-loop`

---

## Phase 4 — The portfolio tests itself (QA signal)

**Why:** A QA automation specialist's portfolio with its own green CI badge is a strong, honest proof point.

### Tasks
1. Add Playwright test suite (Node, `@playwright/test`) at repo root:
   - `package.json` (devDependencies only: `@playwright/test`), `playwright.config.ts` with `webServer: { command: 'python3 -m http.server 8000', url: 'http://localhost:8000' }`, projects: `desktop-chromium` (1280×800) and `mobile` (iPhone 13 device preset).
   - Tests in `tests/site/`:
     - `pages.spec.ts` — every URL in `sitemap.xml` (rewritten to localhost) loads with status 200, has a non-empty `<title>`, exactly one `<h1>`, **no console errors**, no failed network requests to same-origin.
     - `links.spec.ts` — crawl all same-origin `href`/`src` on every page; each returns < 400. External links: only check they're well-formed (no network flakiness in CI).
     - `nav.spec.ts` — nav links reach the right pages; hamburger menu opens on mobile.
     - `layout.spec.ts` — on mobile, `document.documentElement.scrollWidth <= innerWidth` on every page (no horizontal scroll).
     - `theme.spec.ts` — theme toggle adds `.kc-theme--dark` and persists across reload.
     - `flagship.spec.ts` — homepage renders flagship section + supporting cards (count = `SUPPORTING_PROJECTS.length`); clicking play sets the video `src`.
     - `a11y.spec.ts` — run `@axe-core/playwright` on each page; fail on `serious`/`critical` violations (fix the site, don't weaken the test).
   - Note: `js/script.js` calls the GitHub API (`loadGitHubData`) — in tests, mock `api.github.com` with `page.route` so runs are deterministic and don't count its failures as console errors.
2. Add `.github/workflows/site-tests.yml`: on `push` and `pull_request`; `actions/setup-node`, `npm ci`, `npx playwright install --with-deps chromium`, `npx playwright test`; upload `playwright-report/` as artifact on failure; also write a JSON summary (`--reporter=json`) as an artifact for Phase 5.
3. Add a status badge for the workflow to `README.md`.
4. Fix whatever the suite finds (expect axe findings like missing `alt`, contrast, or icon-only buttons without labels).

### Done when
- `npx playwright test` green locally and in Actions on both projects.
- Commits: `test: add playwright smoke suite for the site`, `ci: run site tests on push`, plus `fix:` commits for issues found.

---

## Phase 5 — "Quality Dashboard" page (live proof)

**Why:** Shows real test data instead of claims. Uses honest data only: this site's own test runs (Phase 4) + Lighthouse scores. Optionally later: sanitized results exported from the flagship system.

### Tasks
1. Extend `site-tests.yml` (only on `push` to `main`): after tests, run Lighthouse CI (`@lhci/cli`, 3 runs on home + projects + flagship pages), then a small Node script `scripts/build-metrics.mjs` that appends one entry to `data/qa-metrics.json`:
   ```json
   { "date": "...", "commit": "abc1234", "tests": { "passed": 0, "failed": 0, "flaky": 0, "durationMs": 0 },
     "lighthouse": { "performance": 0, "accessibility": 0, "bestPractices": 0, "seo": 0 } }
   ```
   Keep the last 60 entries. Commit it back with `github-actions[bot]` using `[skip ci]` in the message (workflow needs `permissions: contents: write`).
2. New page `pages/dashboard.html` ("Quality Dashboard") using the standard page shell (nav, footer, `data-base-path="../"`):
   - KPI tiles: latest pass rate, total tests, last run date, Lighthouse scores.
   - Trend chart: pass/fail per run and Lighthouse over time. Use Chart.js from `cdnjs.cloudflare.com` **or** hand-drawn inline SVG; colors from CSS variables; readable in dark mode.
   - Short "How this works" block: GitHub Actions → Playwright + axe + Lighthouse → JSON → this page.
   - Graceful empty state if `data/qa-metrics.json` is missing/empty.
3. Seed `data/qa-metrics.json` with the first real run (run the pipeline locally once — do not fabricate history).
4. Add to nav/footer/sitemap on all pages (see rule 7). Add a pages test for it.

### Done when
- Dashboard renders real data locally and after the first push to `main`.
- Commit: `feat: add quality dashboard fed by CI`

---

## Phase 6 — Performance & polish

1. **Video weight** (12 MB in `assets/videos/`): ensure all videos keep `preload="none"` + poster (homepage already does); re-encode with the existing `scripts/process-demo-videos.sh` if Lighthouse flags them. Only replace committed videos if the new ones look the same.
2. **Images:** add `width`/`height` + `loading="lazy"` to below-the-fold `<img>`; convert `images/*.jpg` to WebP with JPG fallback via `<picture>` only if Lighthouse flags them.
3. **Fonts:** keep Google Fonts with `display=swap` (already set).
4. **Meta:** confirm every page has its own `description`, `og:title`, canonical URL.
5. **404 page:** add `404.html` at repo root (GitHub Pages serves it automatically) in site style with links to Home/Projects.
6. Target Lighthouse ≥ 90 in all four categories on home, projects and flagship pages.

Commit: `perf: ...`, `feat: add 404 page`

---

## Phase 7 — Optional / later (don't start without Vipin's go-ahead)

- **Lab Notes (blog):** `pages/notes.html` + `notes/<slug>.html` static posts, written by Vipin (agent can scaffold template + one example layout; content from Vipin only). Topics idea: "Why my AI test generator needs a human reviewer", "Self-healing locators: what works, what doesn't".
- **Interactive demo:** a "playground" on the flagship page with 3–4 **pre-recorded** examples (user story → generated Gherkin → Playwright/API/Appium code, with a "human edits" diff view). Static data only — no live LLM calls or API keys in a public site.
- **Sanitized flagship metrics** on the dashboard, if Vipin can export them without employer data.

---

## Pre-flight checklist (Vipin, before handing off)

- [ ] Open https://ydvvipin.github.io/portfolio/ — is it live? If 404: repo Settings → Pages → Deploy from branch `main` / root (repo must be public on a free plan). Phases 4–5 CI still work either way.
- [ ] Answer Phase 2 questions (phone public? Formspree ID?).
- [ ] Answer Q1–Q7 in Phase 3.1.
- [ ] Decide which optional Phase 7 items you want.

## Suggested execution order

`Phase 1 → Phase 4 → Phase 6 → Phase 3 → Phase 5 → Phase 2 → Phase 7`

(Phase 4 goes early so every later change is protected by tests; Phase 3 can start as soon as Q1–Q7 are answered.)
