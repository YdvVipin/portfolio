import { test, expect, PAGES } from './fixtures';

for (const path of PAGES) {
  test.describe(`/${path}`, () => {
    test('loads cleanly with a title and one h1', async ({ page, consoleErrors }) => {
      const res = await page.goto(path);
      expect(res?.status()).toBe(200);
      await page.waitForLoadState('networkidle');
      await expect(page).toHaveTitle(/\S/);
      await expect(page.locator('h1')).toHaveCount(1);
      expect(consoleErrors).toEqual([]);
    });

    test('has no horizontal scroll', async ({ page }) => {
      await page.goto(path);
      const overflow = await page.evaluate(() =>
        document.documentElement.scrollWidth - document.documentElement.clientWidth);
      expect(overflow).toBeLessThanOrEqual(1);
    });
  });
}
