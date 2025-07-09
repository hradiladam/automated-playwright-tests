# tests/test_ikea.py

import pytest
from playwright.sync_api import expect
from pages.ikea_page import IkeaPage
from helpers.helper_captcha_skip import is_human_interaction_required


@pytest.fixture(autouse=True)
def setup_ikea(page):
    ikea = IkeaPage(page)
    ikea.goto_home()
    
    if is_human_interaction_required(page):
        pytest.skip("Human verification required (e.g. CAPTCHA or Cloudflare)")

    ikea.accept_cookies()
    return ikea


# Test that switches the site to English
# Verifies that the nearest store is correctly selected based on a user-provided postal code
# Checks all 4 store options avalilable in Czechia
@pytest.mark.parametrize("postal_code, expected_id, expected_text", [
    ("25262", "choice-178", "Praha – Zličín"),
    ("61400", "choice-278", "Brno"),
    ("19800", "choice-408", "Praha – Černý Most"),
    ("75131", "choice-309", "Ostrava"),
])
def test_ikea_find_nearest_store_eng(setup_ikea, postal_code, expected_id, expected_text):
    ikea = setup_ikea
    ikea.switch_to_english()

    # Verify that the language switched (test-level check)
    expect(ikea.page).to_have_url("https://www.ikea.com/cz/en/")

    ikea.search_store(postal_code)

    store = ikea.get_first_store()
    ikea.wait_for_store_id(store, expected_id)

    title = ikea.get_store_title(store)
    expect(title).to_have_text(expected_text, timeout=5000)

    ikea.select_store(store)

    selected = ikea.get_selected_store_text()
    expect(selected).to_have_text(expected_text, timeout=10000)


# pytest tests/test_ikea.py --browser chromium -s
# pytest tests/test_ikea.py --browser firefox -s
# pytest tests/test_ikea.py --browser webkit -s
