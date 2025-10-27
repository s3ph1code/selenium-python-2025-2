from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote


@given("I am on IMDb home")
def step_impl(context):
    context.driver.get("https://www.imdb.com/")


@when('I search for movie "{movie}"')
def step_impl(context, movie):
    q = quote(movie)
    context.driver.get(f"https://www.imdb.com/find/?q={q}&s=tt")


@when("I open the first movie result")
def step_impl(context):
    wait = WebDriverWait(context.driver, 20)
    # Prefer explicit title links
    link = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href*="/title/tt"]'))
    )
    link.click()
    wait.until(EC.url_contains("/title/tt"))


@then('I should see the title contains "{expected}"')
def step_impl(context, expected):
    title = WebDriverWait(context.driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'h1, h1[data-testid="hero__pageTitle"]'))
    ).text
    assert expected.lower() in title.lower(), f"Title '{title}' does not contain '{expected}'"


@then("I should see a numeric rating")
def step_impl(context):
    import re, json
    wait = WebDriverWait(context.driver, 20)

    # Try several UI selectors
    selectors = [
        '[data-testid="hero-rating-bar__aggregate-rating__score"] span',
        '[data-testid="hero-rating-bar__aggregate-rating__score"]',
        'span[aria-label*="IMDb rating"]',
        'div[data-testid="hero-rating-bar__aggregate-rating__score"] span',
        'div.AggregateRatingButton__Rating-sc-1ll29m0-2',
        'span.sc-bde20123-1',
        'meta[itemprop="ratingValue"]'
    ]
    for sel in selectors:
        try:
            el = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, sel)))
            text = (el.get_attribute('content') or el.text or '').strip()
            if re.search(r"\d+(?:[.,]\d+)?", text):
                return
        except Exception:
            continue

    # Fallback: parse JSON-LD for aggregateRating
    scripts = context.driver.find_elements(By.CSS_SELECTOR, 'script[type="application/ld+json"]')
    for s in scripts:
        try:
            data = json.loads(s.get_attribute('innerText') or '{}')
        except Exception:
            continue
        objs = data if isinstance(data, list) else [data]
        for obj in objs:
            if not isinstance(obj, dict):
                continue
            agg = obj.get('aggregateRating')
            if isinstance(agg, dict) and agg.get('ratingValue'):
                return

    assert False, "No numeric rating found in UI or JSON-LD"
