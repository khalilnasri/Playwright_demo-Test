import os
import pytest
import pytest_asyncio
from playwright.async_api import async_playwright
from src.pages.login_page import LoginPage

from src.config import BASE_URL

@pytest_asyncio.fixture(scope="session")
async def browser():
    """Browser-Fixture: Startet einen Browser für die gesamte Test-Session"""

    is_ci = os.getenv("CI", "false").lower() == "true"
    headless_mode = is_ci or os.getenv("HEADLESS", "true").lower() == "true"

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=headless_mode)
        yield browser
        try:
            await browser.close()
        except Exception:
            pass
        
@pytest_asyncio.fixture
async def page(browser):
    """Page fixture - erstellt eine neue Seite für jeden Test"""
    context = await browser.new_context()
    page = await context.new_page()
    yield page
    # Cleanup: Schließe Context (schließt automatisch alle Pages)
    try:
        await context.close()
    except Exception:
        pass

@pytest_asyncio.fixture
async def login(page):
    """Login fixture - navigiert zur Login-Seite"""
    login_page = LoginPage(page)
    await login_page.goto()
    return login_page
