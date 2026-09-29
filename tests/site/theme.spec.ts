import { test, expect } from './fixtures';

test('theme toggle switches to dark and persists across reload', async ({ page }) => {
  await page.goto('index.html');
  const html = page.locator('html');
  await expect(html).not.toHaveClass(/kc-theme--dark/);
  await page.getByRole('button', { name: 'Toggle theme' }).click();
  await expect(html).toHaveClass(/kc-theme--dark/);
  await page.reload();
  await expect(html).toHaveClass(/kc-theme--dark/);
});
