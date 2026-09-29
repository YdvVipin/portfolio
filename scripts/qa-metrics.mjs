#!/usr/bin/env node
/**
 * Appends one run to data/qa-metrics.json for the Quality Dashboard.
 *
 *   node scripts/qa-metrics.mjs [path/to/playwright-results.json]
 *
 * - Test counts come from the Playwright JSON reporter output.
 * - Lighthouse scores are measured here against a local static server
 *   (Chromium from Playwright), averaged over LIGHTHOUSE_PAGES.
 * Env: GITHUB_SHA / GITHUB_RUN_ID / GITHUB_SERVER_URL / GITHUB_REPOSITORY are recorded when present.
 */
import { spawn, execSync } from 'node:child_process';
import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { chromium } from '@playwright/test';
import lighthouse from 'lighthouse';
import * as chromeLauncher from 'chrome-launcher';

const RESULTS = process.argv[2] || 'test-results/results.json';
const OUT = 'data/qa-metrics.json';
const KEEP = 60;
const PORT = 8123;
const LIGHTHOUSE_PAGES = ['', 'pages/projects.html', 'projects/ai-enabled-qa/'];
const CATEGORIES = ['performance', 'accessibility', 'best-practices', 'seo'];

function readTests() {
  if (!existsSync(RESULTS)) throw new Error(`No Playwright results at ${RESULTS}`);
  const { stats } = JSON.parse(readFileSync(RESULTS, 'utf8'));
  return {
    passed: stats.expected,
    failed: stats.unexpected,
    flaky: stats.flaky,
    skipped: stats.skipped,
    durationMs: Math.round(stats.duration),
  };
}

async function waitForServer(url, tries = 50) {
  for (let i = 0; i < tries; i++) {
    try { if ((await fetch(url)).ok) return; } catch {}
    await new Promise(r => setTimeout(r, 200));
  }
  throw new Error(`Server did not start at ${url}`);
}

async function runLighthouse() {
  const server = spawn('python3', ['-m', 'http.server', String(PORT)], { stdio: 'ignore' });
  const chrome = await chromeLauncher.launch({
    chromePath: chromium.executablePath(),
    chromeFlags: ['--headless=new', '--no-sandbox', '--disable-gpu'],
  });
  try {
    await waitForServer(`http://localhost:${PORT}/`);
    const perPage = {};
    for (const path of LIGHTHOUSE_PAGES) {
      const { lhr } = await lighthouse(`http://localhost:${PORT}/${path}`, {
        port: chrome.port, output: 'json', logLevel: 'error', onlyCategories: CATEGORIES,
      });
      perPage['/' + path] = Object.fromEntries(CATEGORIES.map(c => [c, Math.round(lhr.categories[c].score * 100)]));
    }
    const pages = Object.values(perPage);
    const avg = Object.fromEntries(CATEGORIES.map(c =>
      [c, Math.round(pages.reduce((s, p) => s + p[c], 0) / pages.length)]));
    return { ...avg, pages: perPage };
  } finally {
    await chrome.kill();
    server.kill();
  }
}

function gitSha() {
  if (process.env.GITHUB_SHA) return process.env.GITHUB_SHA.slice(0, 7);
  try { return execSync('git rev-parse --short HEAD').toString().trim(); } catch { return null; }
}

const entry = {
  date: new Date().toISOString(),
  commit: gitSha(),
  runUrl: process.env.GITHUB_RUN_ID
    ? `${process.env.GITHUB_SERVER_URL}/${process.env.GITHUB_REPOSITORY}/actions/runs/${process.env.GITHUB_RUN_ID}`
    : null,
  tests: readTests(),
  lighthouse: await runLighthouse(),
};

mkdirSync('data', { recursive: true });
const history = existsSync(OUT) ? JSON.parse(readFileSync(OUT, 'utf8')) : { runs: [] };
history.runs = [...history.runs, entry].slice(-KEEP);
writeFileSync(OUT, JSON.stringify(history, null, 2) + '\n');
console.log(`Recorded run ${entry.commit}: ${entry.tests.passed} passed, ${entry.tests.failed} failed;`,
  `lighthouse ${CATEGORIES.map(c => `${c}=${entry.lighthouse[c]}`).join(' ')}`);
