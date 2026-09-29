import { readFileSync } from 'node:fs';
import { test, expect } from './fixtures';

/** Number of entries in SUPPORTING_PROJECTS in js/script.js — the homepage renders one card per entry. */
const SUPPORTING_COUNT = (readFileSync('js/script.js', 'utf8')
  .match(/const SUPPORTING_PROJECTS = \[([\s\S]*?)\n\];/)?.[1].match(/^\s*\{ name:/gm) ?? []).length;

test('homepage shows the flagship and supporting projects', async ({ page }) => {
  await page.goto('index.html');
  await expect(page.locator('#flagship .kc-flag__title')).toHaveText('QA Automation AI Enabler');
  expect(SUPPORTING_COUNT).toBeGreaterThan(0);
  await expect(page.locator('#project-grid > *')).toHaveCount(SUPPORTING_COUNT);
});

test('flagship demo video loads its source on play', async ({ page }) => {
  await page.goto('index.html');
  const video = page.locator('#flagship-video');
  await expect(video).not.toHaveAttribute('src', /.+/);
  await page.locator('.kc-flag__play').click();
  await expect(video).toHaveAttribute('src', /ai-enabled-qa-demo\.mp4$/);
});

test('projects page renders flagship, supporting and more-work tiers', async ({ page }) => {
  await page.goto('pages/projects.html');
  await expect(page.locator('#flagship-card .kc-flag__title')).toBeVisible();
  expect(await page.locator('#project-grid > *').count()).toBeGreaterThan(0);
  expect(await page.locator('#more-work-list .kc-morework__row').count()).toBeGreaterThan(0);
});
