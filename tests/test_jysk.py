# test_jysk

import pytest
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
    jysk.choosing_quality(quality)
    jysk.display_results()
    jysk.check_filters(quality)
    jysk.scroll_down()
    jysk.count_visible_mattrases(quality)



# pytest tests/test_jysk.py --browser chromium -s
# pytest tests/test_jysk.py --browser firefox -s
# pytest tests/test_jysk.py --browser webkit -s