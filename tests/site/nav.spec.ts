import { test, expect } from './fixtures';

const NAV = ['Projects', 'About', 'Journey', 'Resume', 'Contact'];

test('nav links reach their pages', async ({ page, isMobile }) => {
  for (const label of NAV) {
    await page.goto('index.html');
    if (isMobile) await page.locator('.kc-nav__hamburger').click();
    await page.locator('.kc-nav__links').getByRole('link', { name: label, exact: true }).click();
    await expect(page).toHaveURL(new RegExp(`pages/${label.toLowerCase()}\\.html$`));
  }
});

test('hamburger opens the menu on mobile', async ({ page, isMobile }) => {
  test.skip(!isMobile, 'mobile only');
  await page.goto('index.html');
  const links = page.locator('.kc-nav__links');
  await expect(links).not.toBeInViewport();
  await page.locator('.kc-nav__hamburger').click();
  await expect(links.getByRole('link', { name: 'Projects' })).toBeVisible();
});
