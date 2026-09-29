import { test, expect } from './fixtures';

// 404.html uses <base href="/portfolio/"> because GitHub Pages serves it at any depth.
// Map /portfolio/* back to the local site root so its assets and links resolve here.
test.beforeEach(async ({ page }) => {
  await page.route('http://localhost:*/portfolio/**', route =>
    route.continue({ url: route.request().url().replace('/portfolio/', '/') }));
});

test('404 page renders with working links', async ({ page, consoleErrors }) => {
  await page.goto('404.html');
  await expect(page.locator('h1')).toHaveText("This page didn't pass QA");
  await expect(page.locator('meta[name="robots"]')).toHaveAttribute('content', 'noindex');
  expect(consoleErrors).toEqual([]);
  await page.getByRole('link', { name: 'View Projects' }).click();
  await expect(page).toHaveURL(/pages\/projects\.html$/);
});
