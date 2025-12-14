import pytest_asyncio
from playwright.async_api import async_playwright
from src.pages.login_page import LoginPage
import os


@pytest_asyncio.fixture
async def browser():
    # CI erkennt man über ENV-Variable
    is_ci = os.getenv("CI", "false").lower() == "true"

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=is_ci  # ✅ lokal: False | CI: True
        )
        yield browser
        await browser.close()


@pytest_asyncio.fixture
async def page(browser):
    context = await browser.new_context()
    page = await context.new_page()

    page.set_default_timeout(10_000)
    page.set_default_navigation_timeout(15_000)

    yield page
    await context.close()


@pytest_asyncio.fixture
async def login(page):
    login_page = LoginPage(page)
    await login_page.goto()
    return login_page
