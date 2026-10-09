"""Render the MSDS social graphics for one week into a folder.

Usage: python3 scripts/render_week.py "Week 2"
Output: "<folder>/" with the same filenames as Week 1.
Requires: pip install playwright && playwright install chromium (or use preinstalled Chromium).
"""
import asyncio, os, sys
from playwright.async_api import async_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(ROOT, "templates")

# (template file, selector, viewport width, device scale, output name)
JOBS = [
    ("hidden-costs-photo.html", ".art", 1200, 1, "01-hidden-costs-1200x627.png"),
    ("tue-ask-expert-square.html", ".art", 1080, 1, "02-ask-expert-1080x1080.png"),
    ("tue-ask-expert-landscape.html", ".art", 1200, 1, "03-ask-expert-landscape-1200x900.png"),
    ("wed-support-plan-photo-v4.html", ".art", 1200, 1, "04-support-plan-1200x900.png"),
    ("fri-front-office-card-v2.html", ".art", 1080, 1, "06-front-office-1080x1080.png"),
]

async def main(week):
    out = os.path.join(ROOT, week)
    os.makedirs(out, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for f, sel, w, s, name in JOBS:
            pg = await b.new_page(viewport={"width": w, "height": 1400}, device_scale_factor=s)
            await pg.goto(f"file://{TPL}/{f}")
            await pg.wait_for_load_state("load")
            await pg.add_style_tag(content="body{margin:0!important}")
            await pg.locator(sel).first.screenshot(path=os.path.join(out, name))
            await pg.close()
        pg = await b.new_page(viewport={"width": 480, "height": 1000}, device_scale_factor=2.25)
        await pg.goto(f"file://{TPL}/thu-hacked-carousel-photo.html")
        await pg.wait_for_load_state("load")
        for i in range(5):
            await pg.locator(".slide").nth(i).screenshot(path=os.path.join(out, f"05-hacked-slide{i+1}-1080x1350.png"))
        await b.close()
    print("rendered", out)

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1]))
