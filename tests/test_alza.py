# tests/test_alza.py

# NOTE:
# The test includes handling for CAPTCHA detection that occurs on webkit. 
# The test includes handling for Google sign-in popups that occurs on firefox and webkit.

import pytest
from playwright.sync_api import expect
from pages.alza_page import AlzaPage
from helpers.helper_captcha_skip import is_human_interaction_required



@pytest.fixture(autouse=True)
def setup_alza(page):
    alza = AlzaPage(page)
    alza.goto_home()
    
    if is_human_interaction_required(page):
        pytest.skip("Human verification required (e.g. CAPTCHA or Cloudflare)")

    alza.accept_cookies()
    return alza


# Test that checks that user is offered AlzaPlus subscribtion when in cart going through Payment and Delivery options
@pytest.mark.parametrize("item", [
    "Dell Alienware AW3423DW",
    "Marshall Monitor III",
    "BOSCH MUMS2EW40"
])
def test_alza_plus_offered_in_cart_eng(setup_alza, item):
    alza = setup_alza

    alza.switch_to_english()
    assert alza.get_current_url() == "https://www.alza.cz/EN/?setlang=en-GB"

    alza.search_and_add_to_cart(item)

    alza.go_to_cart()
    expect(alza.page).to_have_url("https://www.alza.cz/Order1.htm")

    alza.proceed_to_payment_and_delivery()
    alza.decline_additional_items_offer()

    expect(alza.get_alza_plus_banner()).to_be_visible()
    expect(alza.get_alza_plus_one_year_option()).to_be_visible()
    expect(alza.get_alza_plus_monthly_option()).to_be_visible()

    alza.empty_cart()

# pytest tests/test_alza.py --browser chromium -s
# pytest tests/test_alza.py --browser firefox -s
# pytest tests/test_alza.py --browser webkit -s