# E2E UI Tests with Playwright

This project contains end-to-end UI tests for three major Czech e-commerce websites:
- [Ikea.cz](https://www.ikea.com/cz/cs/)
- [Jysk.cz](https://www.jysk.cz/)
- [Alza.cz](https://www.alza.cz/)

Tests are written using [Playwright](https://playwright.dev/python/) and `pytest`.  
They run across **Chromium**, **Firefox**, and **WebKit**

## Directory Structure
conftest.py
tests/
├── test_alza.py          
├── test_ikea.py          
└── test_jysk.py         
pages/
├── alza_page.py
├── ikea_page.py          
└── jysk_page.py          
helpers/
├── helper_google_popup_decline.py   
└── helper_captcha_skip.py           

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
