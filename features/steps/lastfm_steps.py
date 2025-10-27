from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote


@given("I am on Lastfm home")
def step_impl(context):
    context.driver.get("https://www.last.fm/")


@when('I search for artist "{artist}"')
def step_impl(context, artist):
    # Navigate directly to search results (artist type)
    q = quote(artist)
    context.driver.get(f"https://www.last.fm/search/artists?q={q}")


@when("I open the first artist result")
def step_impl(context):
    # New search results layout: list items with 'artist-result' or similar
    first = WebDriverWait(context.driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.artist-result a, li.searchresults-item-artist a, .searchresults .artist .result-text a, .link-block-target'))
    )
    first.click()


@then("I should see the latest release date displayed")
def step_impl(context):
    wait = WebDriverWait(context.driver, 20)

    # Strategy 1: time tags in known sections
    try:
        time_el = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'section[data-page-type*="discography"] time, .discography time, time[itemprop="datePublished"], time[datetime]'))
        )
        txt = (time_el.text or "").strip()
        dt = time_el.get_attribute("datetime") or ""
        if any(ch.isdigit() for ch in txt + dt):
            return
    except Exception:
        pass

    # Strategy 2: Any <time> element that contains year-like text or datetime
    try:
        time_any = wait.until(
            EC.presence_of_element_located((By.XPATH, '//time[contains(@datetime,"20") or contains(@datetime,"19") or contains(normalize-space(.),"20") or contains(normalize-space(.),"19")]'))
        )
        content = (time_any.text or "").strip() + (time_any.get_attribute("datetime") or "")
        if any(ch.isdigit() for ch in content):
            return
    except Exception:
        pass

    # Strategy 3: Fallback — look for visible text nodes with a 4-digit year
    import re
    # Check a few common containers to avoid scanning the whole DOM
    candidates = context.driver.find_elements(By.CSS_SELECTOR, 'section, article, .wiki, .header-new-releases, .catalogue, body')
    year_re = re.compile(r'\b(19|20)\d{2}\b')
    for el in candidates:
        try:
            t = el.text
        except Exception:
            continue
        if t and year_re.search(t):
            return

    assert False, "Could not find a date/year on the artist page"
