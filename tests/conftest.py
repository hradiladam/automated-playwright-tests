# tests/conftest.py

import pytest

@pytest.fixture(scope="session")
def browser_launch(playwright, request):
    browser_list = request.config.getoption("browser")
    browser_name = browser_list[0] if isinstance(browser_list, list) else browser_list
    browser = getattr(playwright, browser_name).launch(headless=False, slow_mo=300)
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def context(browser_launch):
    context = browser_launch.new_context()
    yield context
    context.close()

@pytest.fixture(scope="function")
def page(context):
    page = context.new_page()
    yield page
    page.close()
