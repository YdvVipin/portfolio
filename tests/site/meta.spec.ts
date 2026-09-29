import { test, expect, PAGES } from './fixtures';

const SITE = 'https://ydvvipin.github.io/portfolio/';

for (const path of PAGES) {
  test(`/${path} has description, canonical and social preview tags`, async ({ page }) => {
    test.skip(test.info().project.name !== 'desktop', 'meta checked once');
    await page.goto(path);
    const content = (sel: string) => page.locator(sel).getAttribute('content');
    expect(await content('meta[name="description"]')).toMatch(/\S{10,}/);
    expect(await content('meta[property="og:title"]')).toMatch(/\S/);
    expect(await content('meta[property="og:image"]')).toMatch(/^https:\/\//);
    await expect(page.locator('link[rel="canonical"]')).toHaveAttribute('href', SITE + path);
  });
}
