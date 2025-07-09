# tests/test_jysk.py

import pytest
from playwright.sync_api import expect
from pages.jysk_page import JyskPage
from helpers.helper_captcha_skip import is_human_interaction_required


@pytest.fixture(autouse=True)
def setup_jysk(page):
    jysk = JyskPage(page)
    jysk.goto_home()

    if is_human_interaction_required(page):
        pytest.skip("Human verification required (e.g. CAPTCHA or Cloudflare)")
    
    jysk.accept_cookies()
    return jysk
      

# Test that checks that filtering by quality works and displayed items are items of selected quality
#  - tested with mattresses
@pytest.mark.parametrize("quality", [
    "BASIC",
    "PLUS",
    "GOLD",
])
def test_quality_filter(quality, setup_jysk):
    jysk = setup_jysk

    jysk.select_category_of_mattrasses()
    assert "/loznice/matrace" in jysk.get_current_url()

    jysk.choosing_quality(quality)
    jysk.display_results()

    selected_filters = jysk.get_selected_filters()
    expect(selected_filters).to_contain_text(quality)

    jysk.scroll_down()

    visible_products = jysk.get_visible_mattress_products()
    print(f"DEBUG: {len(visible_products)} mattresses visible after applying filter: {quality}")

    for product in visible_products:
        sticker_text = jysk.get_sticker_text(product)
        if sticker_text:
            try:
                expect(product.locator("span.sticker-text")).to_have_text(quality, ignore_case=True)
            except AssertionError:
                print(f"❌ Mismatch: '{sticker_text}' does not match '{quality}'")
                raise


# pytest tests/test_jysk.py --browser chromium -s
# pytest tests/test_jysk.py --browser firefox -s
# pytest tests/test_jysk.py --browser webkit -s