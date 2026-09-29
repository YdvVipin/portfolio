import AxeBuilder from '@axe-core/playwright';
import { test, expect, PAGES } from './fixtures';

for (const path of PAGES) {
  test(`/${path} has no serious accessibility violations`, async ({ page }) => {
    test.skip(test.info().project.name !== 'desktop', 'axe runs once per page');
    await page.goto(path);
    await page.waitForLoadState('networkidle');
    // Scroll-triggered fade-ins start at opacity 0; reveal them so contrast is measured on the real state.
    await page.addStyleTag({ content: '*, *::before, *::after { transition: none !important; animation: none !important; }' });
    await page.evaluate(() => document.querySelectorAll('.kc-fade').forEach(el => el.classList.add('kc-fade--visible')));
    const { violations } = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa']).analyze();
    const serious = violations
      .filter(v => v.impact === 'serious' || v.impact === 'critical')
      .map(v => `${v.id}: ${v.help} (${v.nodes.length}) e.g. ${v.nodes[0].target.join(' ')}`);
    expect(serious).toEqual([]);
  });
}
