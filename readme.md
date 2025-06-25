# E2E UI Tests with Playwright

This project contains end-to-end UI tests for three major Czech e-commerce websites:
- [Ikea.cz](https://www.ikea.com/cz/cs/)
- [Jysk.cz](https://www.jysk.cz/)
- [Alza.cz](https://www.alza.cz/)

Tests are written using [Playwright](https://playwright.dev/python/) and `pytest`.  
They run across **Chromium**, **Firefox**, and **WebKit**

## Directory Structure
-- conftest.py 
-- tests/
    -- test_alza.py # Tests for Alza.cz
    --test_ikea.py # Tests for IKEA.cz
    -- test_jysk.py # Tests for JYSK.cz
-- pages/
    -- alza_page.py # Page Object Model for Alza
    -- ikea_page.py # Page Object Model for IKEA
    --  jysk_page.py # Page Object Model for JYSK
-- helpers/
    -- helper_google_popup_decline.py # Handles Google sign-in popup
    -- helper_captcha_skip.py # Skips test if CAPTCHA appears

## Prerequisites

- Python 3.7+
- Playwright for Python
- pytest

### Installation

```bash
pip install pytest playwright
playwright install
```

## 🧪 Test Summary

### `test_alza.py`
- Switches site to **English**
- Searches for a product and **adds it to the cart**
- Proceeds through the **checkout process**
- Verifies that **Alza Plus** subscription options are displayed during **payment and delivery**

### `test_ikea.py`
- Switches the site to **English**
- Inputs a **postal code** to find the **nearest store**
- Verifies that the correct store is **selected and reflected in the header**

### `test_jysk.py`
- Navigates to the **mattress category**
- Applies a **quality filter** (`BASIC`, `PLUS`, or `GOLD`)
- Verifies that all **visible mattresses** match the selected **quality**
