async def test_add_to_cart(login, page):
    print("STEP 1: start")

    print("STEP 2: login")
    await login.login("standard_user", "secret_sauce")

    print("STEP 3: inventory visible")
    await page.wait_for_selector(".inventory_list", timeout=10_000)

    print("STEP 4: wait add-to-cart button")
    await page.wait_for_selector(
        "#add-to-cart-sauce-labs-backpack",
        timeout=10_000
    )

    print("STEP 5: click add-to-cart")
    await page.click("#add-to-cart-sauce-labs-backpack")

    print("STEP 6: cart badge")
    await page.wait_for_selector(".shopping_cart_badge", timeout=10_000)

    print("STEP 7: done")