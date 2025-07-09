# pages/ikea_page.py
from playwright.sync_api import Page, expect

class IkeaPage:
    def __init__(self, page: Page):
        self.page = page

    def goto_home(self):
        self.page.goto("https://www.ikea.com/cz/cs/")

    def accept_cookies(self):
        try:
            btn = self.page.get_by_role("button", name="Přijmout vše")
            if btn.is_visible(timeout=5000):
                btn.click()
                print("\nDEBUG: Cookie button clicked")
        except:
            print("\nDEBUG: Cookie button not found or failed to click")
    
    def switch_to_english(self):
        # --- Change language to English ---
        language_btn = self.page.get_by_role("button", name="Změna jazyka nebo země, aktuá")
        language_btn.click()
        print("DEBUG: Clicked language button")

        # Wait for the language panel to show
        self.page.locator("div.hnf-sheets__content-wrapper").wait_for(state="visible")
        print("DEBUG: Language panel visible")

        # Click on English
        english_button = self.page.get_by_role("button", name="English")
        english_button.click()
        print("DEBUG: Selected English language")

        # Wait for the English site to load
        self.page.wait_for_load_state("load")
        print("DEBUG: Switched to English site")
    
    # --- Choose store by postal code ---
    def search_store(self, postal_code: str):
        select_store_button = self.page.get_by_role("button", name="Select store")
        select_store_button.click()
        print("DEBUG: Clicked 'Select store' button")

        # Type the postal code
        input_field = self.page.get_by_role("searchbox", name="Search by location")
        input_field.fill(postal_code)
        input_field.press("Enter")
        print(f"DEBUG: Entered postal code: {postal_code}")

    # Get the first item 
    def get_first_store(self):
        return self.page.locator("div.hnf-store-picker__storelist > ul > li > div").first
    
    # Wait until the given store element has the expected ID attribute
    # This confirms that the correct store item has been rendered based on search results
    def wait_for_store_id(self, store_div, expected_id: str):
        expect(store_div).to_have_attribute("id", expected_id, timeout=10000)
        print(f"DEBUG: Store ID matches: {expected_id}")

    # Return the locator for the store's title element inside a store card
    # Used in the test to check that the correct store name is shown to the user
    def get_store_title(self, store_div):
        return store_div.locator("button > span > span > span.hnf-choice-item__title")
    
    # Click on the first store
    def select_store(self, store_div):
        button = store_div.get_by_role("button")
        button.click()
        print("DEBUG: Clicked store button")

    # Check that the selected store name appears in the header
    def get_selected_store_text(self):
        locator = self.page.locator("#hnf-header-storepicker > a > span.hnf-utilities__value")
        locator.wait_for(state="visible", timeout=10000)
        return locator