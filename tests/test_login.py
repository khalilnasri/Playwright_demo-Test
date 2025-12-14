import pytest

@pytest.mark.asyncio
async def test_login_successful(login):
    """ISTQB Test Case 1: Erfolgreicher Login mit korrekten Anmeldedaten"""
    try:
        await login.login()
        await login.assert_logged_in()
        screenshot_path = await login.take_screenshot("test_login_successful")
        print(f"✓ Screenshot gespeichert: {screenshot_path}")
    except Exception as e:
        screenshot_path = await login.take_screenshot("test_login_successful_FAILED")
        print(f"✗ Test fehlgeschlagen. Screenshot gespeichert: {screenshot_path}")
        raise

@pytest.mark.asyncio
async def test_login_wrong_credentials(login):
    """ISTQB Test Case 2: Login mit falschen Anmeldedaten - erwartet Fehlermeldung"""
    try:
        await login.login_with_wrong_credentials(user="wrong_user", pwd="wrong_password")
        await login.assert_error_message("Username and password do not match any user in this service")
        screenshot_path = await login.take_screenshot("test_login_wrong_credentials")
        print(f"✓ Screenshot gespeichert: {screenshot_path}")
    except Exception as e:
        screenshot_path = await login.take_screenshot("test_login_wrong_credentials_FAILED")
        print(f"✗ Test fehlgeschlagen. Screenshot gespeichert: {screenshot_path}")
        raise

@pytest.mark.asyncio
async def test_login_password_missing(login):
    """ISTQB Test Case 3: Login ohne Passwort - erwartet Fehlermeldung"""
    try:
        await login.login_without_password(user="standard_user")
        await login.assert_error_message("Password is required")
        screenshot_path = await login.take_screenshot("test_login_password_missing")
        print(f"✓ Screenshot gespeichert: {screenshot_path}")
    except Exception as e:
        screenshot_path = await login.take_screenshot("test_login_password_missing_FAILED")
        print(f"✗ Test fehlgeschlagen. Screenshot gespeichert: {screenshot_path}")
        raise

@pytest.mark.asyncio
async def test_login_username_missing(login):
    """ISTQB Test Case 4: Login ohne Username - erwartet Fehlermeldung"""
    try:
        await login.login_without_username(pwd="secret_sauce")
        await login.assert_error_message("Username is required")
        screenshot_path = await login.take_screenshot("test_login_username_missing")
        print(f"✓ Screenshot gespeichert: {screenshot_path}")
    except Exception as e:
        screenshot_path = await login.take_screenshot("test_login_username_missing_FAILED")
        print(f"✗ Test fehlgeschlagen. Screenshot gespeichert: {screenshot_path}")
        raise
