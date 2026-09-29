import { test, expect } from './fixtures';

const run = (i: number, failed = 0) => ({
  date: new Date(Date.UTC(2026, 8, 1 + i)).toISOString(),
  commit: `abc${i}def`.slice(0, 7),
  runUrl: null,
  tests: { passed: 100 + i, failed, flaky: 0, skipped: 10, durationMs: 40000 },
  lighthouse: { performance: 90 + (i % 5), accessibility: 98, 'best-practices': 96, seo: 100 },
});

test('renders KPIs, both charts and the table from metrics data', async ({ page, consoleErrors }) => {
  const runs = [run(0), run(1, 3), run(2)];
  await page.route('**/data/qa-metrics.json', r => r.fulfill({ json: { runs } }));
  await page.goto('pages/dashboard.html');
  await expect(page.locator('.kc-stat__value').first()).toHaveText('100%');
  await expect(page.locator('#tests-chart .kc-viz__bar--bad')).toHaveCount(1);
  await expect(page.locator('#lh-chart .kc-viz__line')).toHaveCount(4);
  await expect(page.locator('.kc-dash__table tbody tr')).toHaveCount(3);
  await page.locator('#tests-chart .kc-viz__hit').nth(1).hover();
  await expect(page.locator('#tests-chart .kc-viz__tip')).toContainText('Failed 3');
  expect(consoleErrors).toEqual([]);
});

test('shows an empty state when no metrics exist', async ({ page }) => {
  await page.route('**/data/qa-metrics.json', r => r.fulfill({ status: 404, body: '' }));
  await page.goto('pages/dashboard.html');
  await expect(page.getByRole('heading', { name: 'No runs recorded yet' })).toBeVisible();
});
