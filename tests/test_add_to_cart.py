import pytest
from src.pages.login_page import LoginPage
from src.pages.inventory_page import InventoryPage

@pytest.mark.asyncio
async def test_add_to_cart(login, page):
    login_page = login
    await login_page.goto()
    await login_page.login()
    await login_page.assert_logged_in()

    inventory = InventoryPage(page)
    await inventory.add_first_product_to_cart()
    assert await inventory.is_first_product_in_cart(), "Product was not added to cart"
