# test_alza

# NOTE:
# The test includes handling for CAPTCHA detection that occurs on webkit. 
# The test includes handling for Google sign-in popups that occurs on firefox and webkit.

import pytest
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
    alza.search_and_add_to_cart(item)
    alza.go_to_cart()
    alza.proceed_to_payment_and_delivery()
    alza.decline_additional_items_offer()
    alza.check_alza_plus_offers()
    alza.empty_cart()

# pytest tests/test_alza.py --browser chromium -s
# pytest tests/test_alza.py --browser firefox -s
# pytest tests/test_alza.py --browser webkit -s