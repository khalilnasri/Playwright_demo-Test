import pytest
import asyncio
from playwright.async_api import async_playwright
import os

# Sicherstellen, dass screenshots-Ordner existiert
os.makedirs("screenshots", exist_ok=True)

# URLs und erwartete Titel
test_data = [
    ("https://playwright.dev", "Playwright"),
    ("https://example.com", "Example Domain"),
    ("https://python.org", "Python"),
]

# 🔁 Diese Funktion testet EINE Seite
async def check_title(playwright, url, expected_title):
    browser = await playwright.chromium.launch(headless=False)  # Sichtbarer Browser
    page = await browser.new_page()
    await page.goto(url)
    
    title = await page.title()
    print(f"{url} → Title: {title}")  # Ausgabe im Terminal
    
    # ✅ Titel überprüfen
    assert expected_title in title, f"❌ Title mismatch: {title}"

    # 📸 Screenshot speichern
    filename = f"screenshots/{expected_title.replace(' ', '_')}.png"
    await page.screenshot(path=filename)
    print(f"✓ Screenshot gespeichert: {filename}")

    await browser.close()

# ✅ Das ist der eigentliche Test
@pytest.mark.asyncio
async def test_multiple_pages_parallel():
    async with async_playwright() as playwright:
        tasks = [
            check_title(playwright, url, expected_title)
            for url, expected_title in test_data
        ]
        await asyncio.gather(*tasks)  # Alle Tests parallel starten
