from behave import given, when, then
from selenium.webdriver.common.by import By
import sys
from pathlib import Path
import importlib

# Ensure project root on sys.path and import POM classes dynamically
_project_root = Path(__file__).resolve().parents[2]
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))
LoginPage = importlib.import_module('pages.login_page').LoginPage
InventoryPage = importlib.import_module('pages.inventory_page').InventoryPage


@given('the user is on the login page')
def step_given_user_on_login_page(context):
    # Use the driver provided by features/environment.py
    context.driver.get("https://www.saucedemo.com/")
    context.login_page = LoginPage(context.driver)


@when('the user logs in with valid credentials')
def step_when_user_logs_in_valid(context):
    context.login_page.login("standard_user", "secret_sauce")


@when('the user logs in with invalid credentials')
def step_when_user_logs_in_invalid(context):
    context.login_page.login("invalid_user", "invalid_password")


@when('the user logs in with empty credentials')
def step_when_user_logs_in_empty(context):
    context.login_page.login("", "")


@then('the user should be redirected to the inventory page')
def step_then_inventory_page(context):
    inventory_page = InventoryPage(context.driver)
    assert inventory_page.is_inventory_page_displayed()


@then('an error message should be displayed')
def step_then_error_message(context):
    error_message = context.login_page.find_element((By.CSS_SELECTOR, '[data-test="error"]')).text
    assert "Epic sadface" in error_message
