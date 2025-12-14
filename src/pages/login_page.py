import os
from playwright.async_api import Page, TimeoutError as PlaywrightTimeoutError
from src.config import BASE_URL, USERNAME, PASSWORD

class LoginPage:
    def __init__(self, page: Page):
        self.page = page

    async def goto(self):
        await self.page.goto(
        BASE_URL,
        wait_until="domcontentloaded",
        timeout=15_000
    )

    async def login(self, user=USERNAME, pwd=PASSWORD):
        await self.page.fill("#user-name", user)
        await self.page.fill("#password", pwd)
        await self.page.click("#login-button")
        # Warte kurz auf die Navigation (nicht zu lange, damit der Test nicht hängt)
        await self.page.wait_for_load_state("domcontentloaded", timeout=5000)

    async def login_without_password(self, user=USERNAME):
        """Login nur mit Username, ohne Passwort"""
        await self.page.fill("#user-name", user)
        await self.page.click("#login-button")
        await self.page.wait_for_load_state("domcontentloaded", timeout=5000)

    async def login_without_username(self, pwd=PASSWORD):
        """Login nur mit Passwort, ohne Username"""
        await self.page.fill("#password", pwd)
        await self.page.click("#login-button")
        await self.page.wait_for_load_state("domcontentloaded", timeout=5000)

    async def login_with_wrong_credentials(self, user="wrong_user", pwd="wrong_pass"):
        """Login mit falschen Anmeldedaten"""
        await self.page.fill("#user-name", user)
        await self.page.fill("#password", pwd)
        await self.page.click("#login-button")
        await self.page.wait_for_load_state("domcontentloaded", timeout=5000)

    async def assert_logged_in(self):
        # Prüfe ob das Inventory-Element vorhanden ist
        # Verwende ein Timeout, aber fange es ab, falls es fehlschlägt
        try:
            await self.page.wait_for_selector(".inventory_list", timeout=10000)
        except PlaywrightTimeoutError:
            # Prüfe die URL als Fallback
            current_url = self.page.url
            if "inventory" not in current_url.lower():
                raise AssertionError(f"Login fehlgeschlagen. Aktuelle URL: {current_url}. Element '.inventory_list' nicht gefunden.")

    async def assert_error_message(self, expected_message):
        """Prüft ob eine Fehlermeldung angezeigt wird"""
        # Sauce Demo verwendet h3[data-test="error"] für Fehlermeldungen
        error_selector = 'h3[data-test="error"]'
        try:
            await self.page.wait_for_selector(error_selector, timeout=5000)
            error_text = await self.page.text_content(error_selector)
            assert expected_message.lower() in error_text.lower(), f"Erwartete Fehlermeldung '{expected_message}' nicht gefunden. Gefunden: '{error_text}'"
        except PlaywrightTimeoutError:
            raise AssertionError(f"Fehlermeldung nicht gefunden. Erwartet: '{expected_message}'")

    async def take_screenshot(self, test_name):
        """Erstellt einen Screenshot mit Testnamen"""
        screenshots_dir = "screenshots"
        os.makedirs(screenshots_dir, exist_ok=True)
        screenshot_path = os.path.join(screenshots_dir, f"{test_name}.png")
        await self.page.screenshot(path=screenshot_path, full_page=True)
        return screenshot_path
