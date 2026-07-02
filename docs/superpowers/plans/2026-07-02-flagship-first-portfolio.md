# Flagship-First Portfolio Restructure — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restructure the portfolio around QA Automation AI Enabler as the flagship project, fix all broken/misleading links, remove third-party resume files, and prepare the repo for public GitHub Pages go-live.

**Architecture:** Static site (plain HTML/CSS/JS, no build step). Homepage gets a static flagship section; `js/script.js` renders tiered project cards from three constants; projects page gets flagship hero + supporting cards + compact "More Work" list. Verification is by local HTTP server + browser checks (no test framework exists or is needed).

**Tech Stack:** HTML, CSS (custom `kc-*` design system), vanilla JS, GitHub Pages.

**Spec:** `docs/superpowers/specs/2026-07-02-flagship-first-portfolio-design.md`

## Global Constraints

- Canonical flagship name everywhere: **"QA Automation AI Enabler"**.
- Canonical flagship metrics: **50K+ LOC · 72 API Endpoints · 18 AI Agents · Jira + Zephyr Integrated**.
- Flagship one-liner: *"Records browser interactions, generates production-ready Playwright tests through a 3-layer AI pipeline, self-heals failures, and syncs test cases to Jira & Zephyr Scale."*
- Supporting tier (exactly 3): Playwright BDD Framework, Multi-Agent Orchestration, QA RAG System.
- More Work tier (5): GenAI QA Automation, AI-Enabled API Automation, AI Gig Discovery, JIRA Data Analysis, Jira-TestRail Integration.
- Deleted: `projects/qa-automation-1/`, `projects/qa-automation-2/`.
- No new frameworks or build tools. Reuse existing `kc-*` classes and CSS variables; new CSS goes in `css/style-enhancements.css` only.
- Do NOT alter About/Journey/Resume/Contact content except the footer copyright year.
- No GitHub "source code" links anywhere unless the repo is verified public (as of 2026-07-02 no project repo is public — remove them all).
- `.env` stays untracked/ignored. Never commit it.
- **Caution:** `pages/about.html`, `pages/contact.html`, `pages/journey.html`, `pages/resume.html` have pre-existing uncommitted edits from earlier work. Before the first commit that touches any of them (Task 8), run `git diff pages/` and review — those edits will ride along in the commit. That is expected (they are deliberate content updates), but eyeball them first.

---

### Task 1: Remove third-party resume generator and cache dirs (pre-publication cleanup)

**Files:**
- Delete (tracked): `scripts/generate_ats_resume.py`, `scripts/tests/test_ats_resume.py`, `scripts/output/Shaifali_Yadav_ATS.docx`, `scripts/output/Shaifali_Yadav_ATS.pdf`, `scripts/output/.gitkeep`, `docs/plans/2026-02-23-shaifali-ats-resume-design.md`, `docs/plans/2026-02-23-shaifali-ats-resume-generator.md`
- Delete (untracked): `scripts/__pycache__/`, `scripts/tests/__pycache__/`, `.pytest_cache/`
- Modify: `.gitignore`

**Interfaces:** Produces a `scripts/` dir containing only `process-demo-videos.sh`. Nothing else depends on removed files (verify in Step 2).

- [ ] **Step 1: Remove the files**

```bash
git rm -f scripts/generate_ats_resume.py
git rm -rf scripts/tests scripts/output
git rm -f docs/plans/2026-02-23-shaifali-ats-resume-design.md docs/plans/2026-02-23-shaifali-ats-resume-generator.md
rm -rf scripts/__pycache__ scripts/tests .pytest_cache
```

- [ ] **Step 2: Verify nothing on the site references them**

Run: `grep -rn "generate_ats_resume\|Shaifali\|ats_resume" index.html pages/ projects/ js/ css/ README.md sitemap.xml`
Expected: no output. If any hits appear, remove those references too.

- [ ] **Step 3: Ignore Python caches**

Append to `.gitignore`:

```
__pycache__/
.pytest_cache/
.venv/
```

- [ ] **Step 4: Commit**

```bash
git add .gitignore
git commit -m "chore: remove third-party resume generator and outputs before public release"
```

---

### Task 2: Delete the two legacy project pages and update sitemap

**Files:**
- Delete: `projects/qa-automation-1/`, `projects/qa-automation-2/`
- Modify: `sitemap.xml`

**Interfaces:** Task 3 removes their `LOCAL_PROJECTS` entries; no other page links to them (verify in Step 2).

- [ ] **Step 1: Delete directories**

```bash
git rm -rf projects/qa-automation-1 projects/qa-automation-2
```

- [ ] **Step 2: Verify no remaining inbound links**

Run: `grep -rn "qa-automation-1\|qa-automation-2" index.html pages/ projects/ js/ README.md sitemap.xml`
Expected: hits only in `sitemap.xml` (fixed next step) and `js/script.js` (fixed in Task 3).

- [ ] **Step 3: Remove from sitemap.xml**

Delete these two lines:

```xml
  <url><loc>https://ydvvipin.github.io/portfolio/projects/qa-automation-1/</loc></url>
  <url><loc>https://ydvvipin.github.io/portfolio/projects/qa-automation-2/</loc></url>
```

- [ ] **Step 4: Commit**

```bash
git add sitemap.xml
git commit -m "chore: remove legacy qa-automation-1/2 project pages"
```

---

### Task 3: Restructure `js/script.js` into project tiers

**Files:**
- Modify: `js/script.js` (constants at lines 12–24, `renderLocalProjects()` at lines 366–402, `initFilters()` at lines 204–228, init block at line 40)

**Interfaces:**
- Produces: `FLAGSHIP_PROJECT` (object), `SUPPORTING_PROJECTS` (array of 3), `MORE_WORK` (array of 5); `renderLocalProjects()` fills `#project-grid` (supporting cards, all pages), `#flagship-card` (projects page only), `#more-work-list` (projects page only). Tasks 4–5 create those containers.

- [ ] **Step 1: Replace the `LOCAL_PROJECTS` constant (script.js lines 11–24) with tiered constants**

```js
// ─── Project Tiers ────────────────────────────────
const FLAGSHIP_PROJECT = {
  name: 'QA Automation AI Enabler',
  path: 'projects/ai-enabled-qa/',
  desc: 'Records browser interactions, generates production-ready Playwright tests through a 3-layer AI pipeline, self-heals failures, and syncs test cases to Jira & Zephyr Scale.',
  tags: ['Python', 'React', 'FastAPI', 'Playwright'],
  metrics: [
    { value: '50K+', label: 'Lines of Code' },
    { value: '72', label: 'API Endpoints' },
    { value: '18', label: 'AI Agents' },
    { value: 'Jira + Zephyr', label: 'Integrated' },
  ],
};

const SUPPORTING_PROJECTS = [
  { name: 'Playwright BDD Framework', path: 'projects/playwright-bdd-framework/', desc: 'TypeScript BDD framework with 3 AI agents and 9-tier intelligent locator system', tags: ['TypeScript', 'Playwright'] },
  { name: 'Multi-Agent Orchestration', path: 'projects/multi-agent-orchestration/', desc: '5 specialized agents with 5 MCP servers using CrewAI and LangChain', tags: ['Python', 'CrewAI'] },
  { name: 'QA RAG System', path: 'projects/rag-system/', desc: '25+ data collectors with FAISS vector search for intelligent QA knowledge retrieval', tags: ['Python', 'FAISS'] },
];

const MORE_WORK = [
  { name: 'GenAI QA Automation', path: 'projects/genai-qa-automation/', desc: 'Generative AI powered test case generation and execution pipeline', tags: ['Python', 'AI/ML'] },
  { name: 'AI-Enabled API Automation', path: 'projects/ai-enabled-api-automation/', desc: 'BDD framework with AI-driven API testing, Allure reports, and schema validation', tags: ['Python', 'BDD'] },
  { name: 'AI Gig Discovery', path: 'projects/gig-flow/', desc: 'AI-powered freelance gig discovery automation using Claude API', tags: ['Python', 'Claude API'] },
  { name: 'JIRA Data Analysis', path: 'projects/jira-data-analysis/', desc: 'Prophet forecasting and NLP analysis on Jira project data', tags: ['Python', 'NLP'] },
  { name: 'Jira-TestRail Integration', path: 'projects/JiraTestRailIntegration/', desc: 'Jira to TestRail sync with AI assistance', tags: ['Python', 'REST'] },
];
```

- [ ] **Step 2: Replace `renderLocalProjects()` (old lines 366–402) with tiered rendering**

Keep the existing card markup exactly; extract it into `buildProjectCard()` and add flagship + more-work renderers:

```js
// ─── Local Project Cards ──────────────────────────
function buildProjectCard(project) {
  const card = document.createElement('a');
  card.href = BASE + project.path;
  card.className = 'kc-card kc-fade';

  const tagsHTML = project.tags.map(tag =>
    `<span class="kc-card__tag" style="border-color:${getLangColor(tag)};color:${getLangColor(tag)}">${tag}</span>`
  ).join('');

  card.innerHTML = `
    <div class="kc-card__icon">
      <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
    </div>
    <h3 class="kc-card__title">${project.name}</h3>
    <p class="kc-card__desc">${project.desc}</p>
    <div class="kc-card__tags">${tagsHTML}</div>
    <div class="kc-card__cta">
      View Details
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
    </div>
  `;
  return card;
}

function renderLocalProjects() {
  const grid = document.getElementById('project-grid');
  if (grid) {
    grid.innerHTML = '';
    SUPPORTING_PROJECTS.forEach(p => grid.appendChild(buildProjectCard(p)));
  }

  const flagshipEl = document.getElementById('flagship-card');
  if (flagshipEl) {
    const p = FLAGSHIP_PROJECT;
    const metricsHTML = p.metrics.map(m =>
      `<div class="kc-flag__metric"><div class="kc-flag__metric-val">${m.value}</div><div class="kc-flag__metric-label">${m.label}</div></div>`
    ).join('');
    const tagsHTML = p.tags.map(tag =>
      `<span class="kc-card__tag" style="border-color:${getLangColor(tag)};color:${getLangColor(tag)}">${tag}</span>`
    ).join('');
    flagshipEl.innerHTML = `
      <div class="kc-flag__badge">★ Flagship Project</div>
      <h3 class="kc-flag__title">${p.name}</h3>
      <p class="kc-flag__desc">${p.desc}</p>
      <div class="kc-flag__metrics">${metricsHTML}</div>
      <div class="kc-card__tags">${tagsHTML}</div>
      <a href="${BASE + p.path}" class="kc-btn kc-btn--primary" style="margin-top:20px">
        Read the Full Case Study
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
      </a>
    `;
  }

  const moreList = document.getElementById('more-work-list');
  if (moreList) {
    moreList.innerHTML = '';
    MORE_WORK.forEach(p => {
      const row = document.createElement('a');
      row.href = BASE + p.path;
      row.className = 'kc-morework__row kc-fade';
      const tagsHTML = p.tags.map(tag =>
        `<span class="kc-card__tag" style="border-color:${getLangColor(tag)};color:${getLangColor(tag)}">${tag}</span>`
      ).join('');
      row.innerHTML = `
        <div class="kc-morework__main">
          <span class="kc-morework__name">${p.name}</span>
          <span class="kc-morework__desc">${p.desc}</span>
        </div>
        <div class="kc-morework__tags">${tagsHTML}</div>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
      `;
      moreList.appendChild(row);
    });
  }

  // Re-init animations and tilt for new cards
  initScrollAnimations();
  initCardTilt();
}
```

- [ ] **Step 3: Delete `initFilters()` (old lines 204–228) and its call in the init block (old line 45)**

The filter bar is removed from the projects page in Task 5; the function becomes dead code.

- [ ] **Step 4: Syntax check**

Run: `node --check js/script.js`
Expected: no output (exit 0).

- [ ] **Step 5: Commit**

```bash
git add js/script.js
git commit -m "feat: tier projects into flagship / supporting / more-work in card renderer"
```

---

### Task 4: Add flagship + more-work CSS to `css/style-enhancements.css`

**Files:**
- Modify: `css/style-enhancements.css` (append at end)

**Interfaces:** Produces classes consumed by Task 3 JS and Tasks 5–6 HTML: `.kc-flag`, `.kc-flag__badge`, `.kc-flag__title`, `.kc-flag__desc`, `.kc-flag__metrics`, `.kc-flag__metric`, `.kc-flag__metric-val`, `.kc-flag__metric-label`, `.kc-flag__media`, `.kc-flagship-grid`, `.kc-morework`, `.kc-morework__row`, `.kc-morework__main`, `.kc-morework__name`, `.kc-morework__desc`, `.kc-morework__tags`.

- [ ] **Step 1: Append flagship and more-work styles**

```css
/* ─── Flagship Project Section ─────────────────── */
.kc-flagship-grid {
  display: grid;
  grid-template-columns: 1.15fr 1fr;
  gap: 40px;
  align-items: center;
  background: var(--kc-surface);
  border: 1px solid var(--kc-border);
  border-radius: var(--kc-radius);
  box-shadow: var(--kc-shadow-md);
  padding: 40px;
}
@media (max-width: 860px) { .kc-flagship-grid { grid-template-columns: 1fr; padding: 24px; } }

.kc-flag__badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 5px 14px;
  border-radius: 100px;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--kc-accent);
  background: rgba(99, 102, 241, 0.08);
  border: 1px solid rgba(99, 102, 241, 0.25);
  margin-bottom: 16px;
}
.kc-flag__title { font-family: var(--kc-font); font-size: 1.6rem; font-weight: 700; margin-bottom: 10px; }
.kc-flag__desc { color: var(--kc-text2); font-size: 0.98rem; line-height: 1.7; margin-bottom: 24px; }
.kc-flag__metrics {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-bottom: 20px;
}
@media (max-width: 560px) { .kc-flag__metrics { grid-template-columns: repeat(2, 1fr); } }
.kc-flag__metric {
  background: var(--kc-bg);
  border: 1px solid var(--kc-border);
  border-radius: var(--kc-radius-sm);
  padding: 14px 10px;
  text-align: center;
}
.kc-flag__metric-val { font-family: var(--kc-font); font-weight: 700; font-size: 1.05rem; color: var(--kc-accent); }
.kc-flag__metric-label { font-size: 0.72rem; color: var(--kc-text3); margin-top: 2px; }

.kc-flag__media { position: relative; border-radius: var(--kc-radius-sm); overflow: hidden; box-shadow: var(--kc-shadow-lg); }
.kc-flag__media video { width: 100%; display: block; border-radius: var(--kc-radius-sm); background: #0a0a0f; }
.kc-flag__play {
  position: absolute; inset: 0; z-index: 2;
  display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 12px;
  background: linear-gradient(135deg, rgba(10,10,15,0.55), rgba(17,17,25,0.45));
  cursor: pointer; transition: opacity 0.4s ease;
  color: #fff; font-weight: 600; font-size: 0.85rem; letter-spacing: 0.05em;
}
.kc-flag__play-btn {
  width: 64px; height: 64px; border-radius: 50%;
  background: var(--kc-accent);
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 8px 32px rgba(99, 102, 241, 0.5);
}

/* ─── More Work List ───────────────────────────── */
.kc-morework { display: flex; flex-direction: column; gap: 10px; }
.kc-morework__row {
  display: flex; align-items: center; gap: 16px;
  padding: 16px 20px;
  background: var(--kc-surface);
  border: 1px solid var(--kc-border);
  border-radius: var(--kc-radius-sm);
  color: var(--kc-text);
  text-decoration: none;
  transition: border-color 0.2s, transform 0.2s, box-shadow 0.2s;
}
.kc-morework__row:hover { border-color: var(--kc-accent); transform: translateX(4px); box-shadow: var(--kc-shadow-md); }
.kc-morework__main { flex: 1; display: flex; flex-direction: column; gap: 2px; min-width: 0; }
.kc-morework__name { font-family: var(--kc-font); font-weight: 600; font-size: 0.95rem; }
.kc-morework__desc { font-size: 0.82rem; color: var(--kc-text2); }
.kc-morework__tags { display: flex; gap: 6px; flex-shrink: 0; }
@media (max-width: 640px) { .kc-morework__tags { display: none; } }
```

- [ ] **Step 2: Check dark theme**

Run: `grep -n "kc-theme--dark" css/style.css css/style-enhancements.css | head -5` and read how existing components override colors in dark mode. If dark mode restyles `--kc-surface`/`--kc-bg`/`--kc-border` via variable overrides on `.kc-theme--dark`, the new classes inherit automatically — nothing to do. If it uses per-component overrides, add matching `.kc-theme--dark .kc-flagship-grid`, `.kc-theme--dark .kc-flag__metric`, `.kc-theme--dark .kc-morework__row` rules using the same surface/border colors as `.kc-theme--dark .kc-card`.

- [ ] **Step 3: Commit**

```bash
git add css/style-enhancements.css
git commit -m "feat: add flagship section and more-work list styles"
```

---

### Task 5: Restructure `pages/projects.html` into tiers

**Files:**
- Modify: `pages/projects.html` (lines 45–75: header, filters, grid)

**Interfaces:** Consumes `#flagship-card`, `#project-grid`, `#more-work-list` rendering from Task 3.

- [ ] **Step 1: Replace the two header sections and the filter/grid section (lines 47–73) with the tiered layout**

Replace everything between `<main>` and `</main>` with:

```html
    <!-- Page Header -->
    <section class="kc-section" style="padding-bottom:0;padding-top:120px">
      <div class="kc-wrap">
        <h1 class="kc-section__title kc-fade">Projects</h1>
        <p class="kc-section__sub kc-fade">One flagship platform, three supporting builds, and a track record of shipped automation work.</p>
      </div>
    </section>

    <!-- Flagship -->
    <section class="kc-section" style="padding-top:32px;padding-bottom:0">
      <div class="kc-wrap">
        <div id="flagship-card" class="kc-flagship-grid kc-fade" style="display:block">
          <!-- Rendered by JS -->
        </div>
      </div>
    </section>

    <!-- Supporting Projects -->
    <section class="kc-section" style="padding-bottom:0">
      <div class="kc-wrap">
        <h2 class="kc-section__title kc-fade">Supporting Projects</h2>
        <p class="kc-section__sub kc-fade">Framework engineering, agent orchestration, and ML infrastructure — each with a full walkthrough.</p>
        <div class="kc-grid" id="project-grid">
          <!-- Rendered by JS -->
        </div>
      </div>
    </section>

    <!-- More Work -->
    <section class="kc-section">
      <div class="kc-wrap">
        <h2 class="kc-section__title kc-fade">More Work</h2>
        <p class="kc-section__sub kc-fade">Smaller builds and integrations, each with its own detail page.</p>
        <div class="kc-morework" id="more-work-list">
          <!-- Rendered by JS -->
        </div>
      </div>
    </section>
```

Note: `#flagship-card` uses `display:block` because the JS fills it with badge/title/metrics as a single column card on this page (no video here — the homepage owns the video).

- [ ] **Step 2: Verify in browser**

Run: `python3 -m http.server 8899` (background, repo root), open `http://localhost:8899/pages/projects.html` with Playwright browser.
Expected: flagship card with badge + 4 metrics on top, exactly 3 supporting cards, 5 more-work rows, no filter buttons, no duplicated subtitle, no console errors.

- [ ] **Step 3: Commit**

```bash
git add pages/projects.html
git commit -m "feat: tiered projects page — flagship hero, supporting cards, more-work list"
```

---

### Task 6: Homepage flagship section, stats fix, footer update

**Files:**
- Modify: `index.html` (stats bar lines 104–107, Featured Projects section lines 139–156, footer Top Projects lines 190–196)

**Interfaces:** Consumes `#project-grid` supporting-card rendering from Task 3; video assets `assets/posters/ai-enabled-qa-poster.svg`, `assets/videos/ai-enabled-qa-demo.mp4`.

- [ ] **Step 1: Replace the "∞ Cups of Coffee" stat (lines 104–107)**

```html
          <div class="kc-stat">
            <div class="kc-stat__value" data-target="18">18</div>
            <div class="kc-stat__label">AI Agents Built</div>
          </div>
```

- [ ] **Step 2: Replace the Featured Projects section (lines 139–156) with flagship + supporting**

```html
    <!-- Flagship Project -->
    <section class="kc-section" id="flagship">
      <div class="kc-wrap">
        <h2 class="kc-section__title kc-fade">Flagship Project</h2>
        <p class="kc-section__sub kc-fade">The build that ties it all together — AI test generation wired into the tools QA teams already live in.</p>
        <div class="kc-flagship-grid kc-fade">
          <div class="kc-flag__media">
            <video id="flagship-video" poster="assets/posters/ai-enabled-qa-poster.svg" data-src="assets/videos/ai-enabled-qa-demo.mp4" preload="none" controls></video>
            <div class="kc-flag__play" onclick="var v=document.getElementById('flagship-video');var s=v.dataset.src;if(s&&!v.src){v.src=s;v.load()}v.play();this.style.opacity='0';this.style.pointerEvents='none'">
              <div class="kc-flag__play-btn">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="#fff"><path d="M8 5v14l11-7z"/></svg>
              </div>
              Watch the 2-minute demo
            </div>
          </div>
          <div>
            <div class="kc-flag__badge">★ Flagship Project</div>
            <h3 class="kc-flag__title">QA Automation AI Enabler</h3>
            <p class="kc-flag__desc">Records browser interactions, generates production-ready Playwright tests through a 3-layer AI pipeline, self-heals failures, and syncs test cases to Jira &amp; Zephyr Scale. Multi-LLM enhancement, LangGraph healing agents, and a React dashboard — built end to end.</p>
            <div class="kc-flag__metrics">
              <div class="kc-flag__metric"><div class="kc-flag__metric-val">50K+</div><div class="kc-flag__metric-label">Lines of Code</div></div>
              <div class="kc-flag__metric"><div class="kc-flag__metric-val">72</div><div class="kc-flag__metric-label">API Endpoints</div></div>
              <div class="kc-flag__metric"><div class="kc-flag__metric-val">18</div><div class="kc-flag__metric-label">AI Agents</div></div>
              <div class="kc-flag__metric"><div class="kc-flag__metric-val">Jira + Zephyr</div><div class="kc-flag__metric-label">Integrated</div></div>
            </div>
            <a href="projects/ai-enabled-qa/" class="kc-btn kc-btn--primary">
              Read the Full Case Study
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
            </a>
          </div>
        </div>
      </div>
    </section>

    <!-- Supporting Projects -->
    <section class="kc-section" style="padding-top:0">
      <div class="kc-wrap">
        <h2 class="kc-section__title kc-fade">Supporting Projects</h2>
        <p class="kc-section__sub kc-fade">Framework engineering, multi-agent orchestration, and ML infrastructure behind the flagship.</p>

        <div class="kc-grid" id="project-grid">
          <!-- Rendered by JS — supporting tier -->
        </div>

        <div style="text-align:center;margin-top:48px" class="kc-fade">
          <a href="pages/projects.html" class="kc-btn kc-btn--outline">
            View All Projects
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
          </a>
        </div>
      </div>
    </section>
```

- [ ] **Step 3: Update footer "Top Projects" (lines 190–196)**

```html
        <h4 class="kc-footer__heading">Top Projects</h4>
        <ul class="kc-footer__links">
          <li><a href="projects/ai-enabled-qa/" class="kc-footer__link">QA Automation AI Enabler</a></li>
          <li><a href="projects/playwright-bdd-framework/" class="kc-footer__link">Playwright BDD Framework</a></li>
          <li><a href="projects/multi-agent-orchestration/" class="kc-footer__link">Multi-Agent Orchestration</a></li>
          <li><a href="projects/rag-system/" class="kc-footer__link">QA RAG System</a></li>
        </ul>
```

- [ ] **Step 4: Verify in browser**

Open `http://localhost:8899/` with Playwright browser.
Expected: flagship section with poster + play overlay, 4 metrics, exactly 3 supporting cards below, stats bar shows "18 AI Agents Built", no console errors. Click play overlay → video loads and plays. Check at 375px width: flagship grid stacks to one column.

- [ ] **Step 5: Commit**

```bash
git add index.html
git commit -m "feat: flagship-first homepage — hero case study with demo video, 3 supporting cards"
```

---

### Task 7: Flagship case-study page — fix dead GitHub button, add Jira/Zephyr, unify copy

**Files:**
- Modify: `projects/ai-enabled-qa/index.html` (hero lines 185–198; features grid — locate via `grep -n "features-grid" projects/ai-enabled-qa/index.html`)

- [ ] **Step 1: Replace the broken "View Source Code" button (lines 191–194)**

The button links to `https://github.com/vipinyadav` — someone else's profile. Replace the entire `<a ...>View Source Code</a>` element with:

```html
      <a href="#demo" class="btn btn-primary">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>
        Watch the Demo
      </a>
```

- [ ] **Step 2: Update hero paragraph (line ~189) to the unified story**

```html
    <p>An enterprise-grade platform that records browser interactions, generates production-ready Playwright tests through a 3-layer deterministic + AI pipeline, self-heals failures with a 4-agent LangGraph loop, and syncs test cases straight into Jira and Zephyr Scale.</p>
```

- [ ] **Step 3: Add a Jira/Zephyr card to the features grid**

Locate the `features-grid` div and append this card inside it, matching sibling markup:

```html
      <div class="feature-card fade-in">
        <div class="feature-icon" style="background:rgba(6,182,212,.1)">🔗</div>
        <h4>Jira &amp; Zephyr Scale Integration</h4>
        <p>Pulls Jira tickets, generates AI test cases from requirements, and pushes them into Zephyr Scale folders — with n8n workflows automating the Jira&nbsp;→&nbsp;tests pipeline end to end.</p>
      </div>
```

- [ ] **Step 4: Sanity-check for other dead links on this page**

Run: `grep -n "github.com" projects/ai-enabled-qa/index.html`
Expected: no `github.com/vipinyadav` remaining. If a footer GitHub profile link points to `github.com/YdvVipin` (the real account), keep it.

- [ ] **Step 5: Verify in browser**

Open `http://localhost:8899/projects/ai-enabled-qa/`. Expected: hero button scrolls to demo, new feature card renders, no console errors.

- [ ] **Step 6: Commit**

```bash
git add projects/ai-enabled-qa/index.html
git commit -m "fix: flagship page — remove dead GitHub link, add Jira/Zephyr integration, unify pitch"
```

---

### Task 8: Remove dead source-code links on remaining project pages + fix copyright year site-wide

**Files:**
- Modify: `projects/JiraTestRailIntegration/index.html:150`, `projects/jira-data-analysis/index.html:79`, `projects/ai-enabled-api-automation/index.html:93`, `projects/playwright-bdd-framework/index.html:56`, `projects/gig-flow/index.html:159`
- Modify (year only): `index.html`, `pages/about.html`, `pages/contact.html`, `pages/journey.html`, `pages/projects.html`, `pages/resume.html`, and all `projects/*/index.html` footers with `&copy; 2025`

- [ ] **Step 1: Review pre-existing uncommitted edits before touching shared pages**

Run: `git diff pages/about.html pages/contact.html pages/journey.html pages/resume.html | head -100`
Expected: deliberate content edits from earlier sessions. They will be committed together with the year fix in this task — confirm nothing looks accidental (if something does, stop and ask the user).

- [ ] **Step 2: Delete the five dead GitHub link elements**

Remove these `<a>` elements entirely (all five URLs 404):
- `projects/JiraTestRailIntegration/index.html:150` — `💻 GitHub Repo` → `github.com/YdvVipin/portfolio`
- `projects/jira-data-analysis/index.html:79` — `GitHub Repo` → `github.com/YdvVipin/portfolio`
- `projects/ai-enabled-api-automation/index.html:93` — `View on GitHub` → `github.com/YdvVipin/AIEnabledAPIAutomation`
- `projects/playwright-bdd-framework/index.html:56` — `View Source` → `github.com/YdvVipin/PlaywrightDemoProject`
- `projects/gig-flow/index.html:159` — `💻 GitHub Repository` → `github.com/ydvvipin/gig-automation`

- [ ] **Step 3: Verify no dead project-repo links remain**

Run: `grep -rn "github.com" index.html pages/ projects/ README.md | grep -v "github.com/YdvVipin\"" | grep -viE "linkedin|YdvVipin/?\"|YdvVipin/?'"`
Then manually confirm every remaining `github.com` URL is either the profile `https://github.com/YdvVipin` or a verified-public repo (`barsanataxiservice`, `claude-flow`, `PlaywriteFramework`, `skills`).

- [ ] **Step 4: Update copyright year**

Run: `grep -rln "&copy; 2025" index.html pages/ projects/` then in each file replace `&copy; 2025` with `&copy; 2026` (footer lines only — do not touch other "2025" strings such as journey timeline dates).

- [ ] **Step 5: Commit**

```bash
git add -A index.html pages/ projects/
git commit -m "fix: remove dead GitHub source links; bump copyright year to 2026"
```

---

### Task 9: Rewrite README highlights

**Files:**
- Modify: `README.md` (Highlights section)

- [ ] **Step 1: Replace the Highlights section**

```markdown
## Highlights

- **[QA Automation AI Enabler](https://ydvvipin.github.io/portfolio/projects/ai-enabled-qa/)** — flagship platform: records browser interactions, generates production-ready Playwright tests through a 3-layer AI pipeline, self-heals failures, and syncs test cases to Jira & Zephyr Scale. 50K+ LOC · 72 API endpoints · 18 AI agents.
- **[My Journey](https://ydvvipin.github.io/portfolio/pages/journey.html)** — from RF drive-tests in Gurgaon to architecting AI agent platforms for a Toronto team
- **[Playwright BDD Framework](https://ydvvipin.github.io/portfolio/projects/playwright-bdd-framework/)** — TypeScript framework with a 9-tier intelligent locator system
- **[Multi-Agent Orchestration](https://ydvvipin.github.io/portfolio/projects/multi-agent-orchestration/)** — 5 specialized agents with MCP servers using CrewAI and LangChain
- **[QA RAG System](https://ydvvipin.github.io/portfolio/projects/rag-system/)** — 25+ data collectors with FAISS vector search
- Plus five more builds covering GenAI test generation, API automation, and Jira analytics — see [all projects](https://ydvvipin.github.io/portfolio/pages/projects.html)
```

- [ ] **Step 2: Verify no references to deleted projects**

Run: `grep -n "qa-automation-1\|qa-automation-2\|E-Commerce\|API Testing Suite" README.md`
Expected: no output.

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "docs: flagship-first README highlights"
```

---

### Task 10: Full-site verification

**Files:** none (verification only)

- [ ] **Step 1: Link check every local href**

With the local server running, crawl all pages:

```bash
for f in index.html pages/*.html projects/*/index.html; do
  grep -oE 'href="[^"#]+"|src="[^"]+"' "$f" | sed 's/^[a-z]*="//;s/"$//' | grep -vE '^(https?:|mailto:|data:)' | while read -r link; do
    dir=$(dirname "$f"); target="$dir/$link"
    [ -e "$target" ] || [ -e "${target%%\?*}" ] || echo "BROKEN in $f: $link"
  done
done
```

Expected: no `BROKEN` lines.

- [ ] **Step 2: Browser pass with Playwright**

Visit `/`, `/pages/projects.html`, `/projects/ai-enabled-qa/`, one supporting page, one more-work page. For each: snapshot renders correctly, zero console errors. Test homepage at 375px width. Test dark-mode toggle on `/` and `/pages/projects.html` — flagship card and more-work rows must remain readable.

- [ ] **Step 3: Fix anything found, commit fixes**

```bash
git add -A && git commit -m "fix: verification pass fixes"
```

(Skip commit if nothing found.)

---

### Task 11: Go-live — squash history, publish repo, enable Pages

**⚠️ Requires explicit user confirmation immediately before Steps 2–4 — force-push and publishing are not reversible in practice.**

Git history contains Shaifali's resume PDF/DOCX and the evasion-feature commits; deleting files (Task 1) does not remove them from history. A portfolio repo doesn't need history, so squash to a single public commit.

**Files:** none (git/GitHub operations)

- [ ] **Step 1: Confirm working tree is clean and verified**

Run: `git status --porcelain`
Expected: empty (all tasks committed).

- [ ] **Step 2 (after user confirms): Squash history into one commit**

```bash
git checkout --orphan public-release
git add -A
git commit -m "Portfolio — public release

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
git branch -M public-release main
git push -f origin main
```

- [ ] **Step 3 (after user confirms): Make repo public**

```bash
gh repo edit YdvVipin/portfolio --visibility public --accept-visibility-change-consequences
```

- [ ] **Step 4: Enable GitHub Pages from main branch root**

```bash
gh api repos/YdvVipin/portfolio/pages -X POST -f "source[branch]=main" -f "source[path]=/"
```

- [ ] **Step 5: Verify live**

Wait for Pages build (~1–2 min), then:

```bash
curl -s -o /dev/null -w "%{http_code}" https://ydvvipin.github.io/portfolio/
```

Expected: `200`. Then spot-check `https://ydvvipin.github.io/portfolio/pages/projects.html` and the flagship page in the browser.
