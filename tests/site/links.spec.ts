import { test, expect, PAGES } from './fixtures';

test.describe.configure({ mode: 'serial' });

test('every same-origin link and asset resolves', async ({ page, request }) => {
  test.skip(test.info().project.name !== 'desktop', 'link crawl runs once');
  const checked = new Map<string, number>();
  const broken: string[] = [];

  for (const path of PAGES) {
    await page.goto(path);
    const urls = await page.$$eval('[href], [src], [data-src], [poster]', els =>
      els.flatMap(el => ['href', 'src', 'data-src', 'poster']
        .map(a => el.getAttribute(a))
        .filter((v): v is string => !!v)
        .map(v => new URL(v, location.href).href)));

    for (const raw of urls) {
      const url = new URL(raw);
      if (url.hostname !== 'localhost') continue;
      url.hash = '';
      const key = url.href;
      if (!checked.has(key)) checked.set(key, (await request.get(key)).status());
      if (checked.get(key)! >= 400) broken.push(`${path} -> ${url.pathname} (${checked.get(key)})`);
    }
  }
  expect(broken).toEqual([]);
});
