import { test as base, expect, Page } from '@playwright/test';
import { existsSync, readFileSync } from 'node:fs';
import { basename, join } from 'node:path';

/** Site paths from sitemap.xml, relative to the site root (e.g. "pages/about.html"). */
export const PAGES: string[] = [...readFileSync('sitemap.xml', 'utf8').matchAll(/<loc>([^<]+)<\/loc>/g)]
  .map(m => new URL(m[1]).pathname.replace(/^\/portfolio\//, ''));

/**
 * Stubs every third-party request so runs are deterministic and offline-safe:
 * Google Fonts, the GitHub API used by js/script.js, and anything else external.
 * Script CDNs are let through by default so a broken library URL still fails the suite.
 * Set SITE_TESTS_OFFLINE=1 (e.g. in a sandbox without CDN access) to serve tiny shims instead,
 * or point SITE_TESTS_CDN_DIR at a folder of real library files (matched by file name).
 */
const SCRIPT_CDNS = ['cdn.jsdelivr.net', 'cdnjs.cloudflare.com', 'unpkg.com'];
const OFFLINE = !!process.env.SITE_TESTS_OFFLINE;
const CDN_SHIMS: Record<string, string> = {
  mermaid: 'window.mermaid = { initialize() {}, run() { return Promise.resolve(); } };',
  html2pdf: 'window.html2pdf = () => { const c = { set: () => c, from: () => c, save: () => Promise.resolve() }; return c; };',
};

async function stubExternal(page: Page) {
  await page.route(url => url.hostname !== 'localhost', route => {
    const url = new URL(route.request().url());
    if (SCRIPT_CDNS.includes(url.hostname)) {
      if (!OFFLINE) return route.continue();
      const local = process.env.SITE_TESTS_CDN_DIR && join(process.env.SITE_TESTS_CDN_DIR, basename(url.pathname));
      if (local && existsSync(local)) return route.fulfill({ status: 200, contentType: 'text/javascript', body: readFileSync(local) });
      const shim = Object.keys(CDN_SHIMS).find(name => url.pathname.includes(name));
      return route.fulfill({ status: 200, contentType: 'text/javascript', body: shim ? CDN_SHIMS[shim] : '' });
    }
    if (url.hostname === 'fonts.googleapis.com') {
      return route.fulfill({ status: 200, contentType: 'text/css', body: '' });
    }
    if (url.hostname === 'api.github.com') {
      const body = url.pathname.endsWith('/repos') ? '[]' : '{}';
      return route.fulfill({ status: 200, contentType: 'application/json', body });
    }
    return route.fulfill({ status: 204, body: '' });
  });
}

type Fixtures = { consoleErrors: string[] };

export const test = base.extend<Fixtures>({
  page: async ({ page }, use) => {
    await stubExternal(page);
    await use(page);
  },
  consoleErrors: async ({ page }, use) => {
    const errors: string[] = [];
    page.on('console', msg => { if (msg.type() === 'error') errors.push(msg.text()); });
    page.on('pageerror', err => errors.push(err.message));
    page.on('response', res => {
      if (new URL(res.url()).hostname === 'localhost' && res.status() >= 400) {
        errors.push(`${res.status()} ${res.url()}`);
      }
    });
    await use(errors);
  },
});

export { expect };
