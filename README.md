# Vipin Yadav — QA Automation & AI Engineering Portfolio

[![Site Tests](https://github.com/YdvVipin/portfolio/actions/workflows/site-tests.yml/badge.svg)](https://github.com/YdvVipin/portfolio/actions/workflows/site-tests.yml)

**Live site:** https://ydvvipin.github.io/portfolio/

QA Automation Specialist with 8+ years across RF network testing, mobile QA, and enterprise web automation — now building AI-powered testing platforms, multi-agent orchestration systems, and CI/CD-integrated frameworks. Remote-first, based in India, working with teams across Canada, the US, and global time zones. **Open to remote full-time, contract, and freelance roles.**

## Highlights

- **[QA Automation AI Enabler](https://ydvvipin.github.io/portfolio/projects/ai-enabled-qa/)** — flagship platform: records browser interactions, generates production-ready Playwright tests through a 3-layer AI pipeline, self-heals failures, and syncs test cases to Jira & Zephyr Scale. 50K+ LOC · 72 API endpoints · 18 AI agents.
- **[My Journey](https://ydvvipin.github.io/portfolio/pages/journey.html)** — from RF drive-tests in Gurgaon to building AI agent platforms for a Toronto team, told as a milestone roadmap
- **[Playwright BDD Framework](https://ydvvipin.github.io/portfolio/projects/playwright-bdd-framework/)** — TypeScript framework with a 9-tier intelligent locator system
- **[Multi-Agent Orchestration](https://ydvvipin.github.io/portfolio/projects/multi-agent-orchestration/)** — 5 specialized agents with MCP servers using CrewAI and LangChain
- **[QA RAG System](https://ydvvipin.github.io/portfolio/projects/rag-system/)** — 25+ data collectors with FAISS vector search
- Plus five more builds covering GenAI test generation, API automation, and Jira analytics — see [all projects](https://ydvvipin.github.io/portfolio/pages/projects.html)

## Tech Stack

- **Automation:** Playwright, Selenium, Appium, Cucumber/Behave BDD, REST Assured
- **Languages:** Python, TypeScript, JavaScript, Java, SQL
- **AI/ML:** Agentic AI, LangChain, CrewAI, MCP, RAG, FAISS, Claude API
- **DevOps:** Docker, GitHub Actions, Jenkins, CI/CD pipelines
- **QA Tools:** Jira, TestRail, Zephyr, Allure, Postman

## How this site is tested

A portfolio from a QA engineer should test itself. Every push runs a Playwright suite in GitHub Actions on desktop and mobile viewports:

- every page in `sitemap.xml` loads with no console errors, one `<h1>` and no horizontal scroll on mobile
- every same-origin link and asset resolves
- nav, mobile menu, theme toggle and the flagship demo video work
- axe-core finds no serious or critical WCAG 2 A/AA violations

Run it locally:

```bash
npm ci
npx playwright install chromium
npm test                       # serves the site on :8000 and runs the suite
SITE_TESTS_OFFLINE=1 npm test  # stub third-party CDNs when offline
```

## Contact

- **Email:** [ydvvipin1793@gmail.com](mailto:ydvvipin1793@gmail.com)
- **LinkedIn:** [linkedin.com/in/vipin-ydv](https://www.linkedin.com/in/vipin-ydv/)
- **GitHub:** [github.com/YdvVipin](https://github.com/YdvVipin)
