from playwright.async_api import Page

class InventoryPage:
    def __init__(self, page: Page):
        self.page = page

    async def add_first_product_to_cart(self):
        await self.page.click(".inventory_item button")

    async def is_first_product_in_cart(self) -> bool:
        button_text = await self.page.inner_text(".inventory_item button")
        return button_text.lower() == "remove"