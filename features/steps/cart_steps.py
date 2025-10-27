from behave import given, when, then
import time
import sys
from pathlib import Path
import importlib

# Ensure project root on sys.path and import POM classes dynamically
_project_root = Path(__file__).resolve().parents[2]
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))
LoginPage = importlib.import_module('pages.login_page').LoginPage
InventoryPage = importlib.import_module('pages.inventory_page').InventoryPage


@given("I am logged in on the inventory page")
def step_impl(context):
    context.driver.get("https://www.saucedemo.com/")
    login_page = LoginPage(context.driver)
    login_page.login("standard_user", "secret_sauce")
    context.inventory_page = InventoryPage(context.driver)


@when('I add the product "{product_name}" to the cart')
def step_impl(context, product_name):
    context.inventory_page.add_product_to_cart(product_name)


@then("I should see 1 item in the cart")
def step_impl(context):
    time.sleep(1)
    cart_count = context.inventory_page.get_cart_count()
    assert cart_count == "1"
