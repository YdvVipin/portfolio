#!/usr/bin/env python3
"""Capture screenshots from project detail pages using Playwright.

Usage:
    python capture.py --project ai-enabled-qa --url http://localhost:52305
    python capture.py --project ai-enabled-qa --file ../../projects/ai-enabled-qa/index.html
"""

import argparse
import asyncio
from pathlib import Path

from playwright.async_api import async_playwright


SCREENSHOTS_DIR = Path(__file__).parent / "screenshots"


async def capture_project_page(
    project_name: str,
    url: str,
    sections: list[str] | None = None,
) -> list[Path]:
    """Capture screenshots from a project's detail page.

    Args:
        project_name: Name for the output directory.
        url: URL of the project page.
        sections: CSS selectors for sections to capture. If None, captures full page.
    """
    output_dir = SCREENSHOTS_DIR / project_name
    output_dir.mkdir(parents=True, exist_ok=True)

    captured = []

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1280, "height": 720})

        await page.goto(url, wait_until="networkidle")
        await page.wait_for_timeout(1000)  # Let animations settle

        if sections:
            for i, selector in enumerate(sections):
                try:
                    element = page.locator(selector).first
                    await element.wait_for(timeout=5000)
                    path = output_dir / f"{i+1:02d}-{selector.replace('.', '').replace('#', '')[:30]}.png"
                    await element.screenshot(path=str(path))
                    captured.append(path)
                    print(f"  [Capture] {path.name}")
                except Exception as e:
                    print(f"  [Skip] {selector}: {e}")
        else:
            # Full page screenshot
            path = output_dir / "01-full-page.png"
            await page.screenshot(path=str(path), full_page=True)
            captured.append(path)
            print(f"  [Capture] {path.name}")

            # Also capture viewport
            path = output_dir / "02-hero.png"
            await page.screenshot(path=str(path))
            captured.append(path)
            print(f"  [Capture] {path.name}")

        await browser.close()

    return captured


def main():
    parser = argparse.ArgumentParser(description="Capture project screenshots")
    parser.add_argument("--project", required=True, help="Project name")
    parser.add_argument("--url", help="URL to capture")
    parser.add_argument("--file", help="Local HTML file path")
    parser.add_argument("--sections", nargs="*", help="CSS selectors to capture")
    args = parser.parse_args()

    url = args.url
    if args.file:
        url = f"file://{Path(args.file).resolve()}"

    if not url:
        print("Error: Provide --url or --file")
        return

    asyncio.run(capture_project_page(args.project, url, args.sections))


if __name__ == "__main__":
    main()
