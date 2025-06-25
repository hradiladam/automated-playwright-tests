# ikea_page
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
        expect(self.page).to_have_url("https://www.ikea.com/cz/en/")
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
    
    # Wait for and verify the first (nearest) store has the expected ID attribute
    def verify_store(self, store_div, expected_id: str, expected_text: str):
        expect(store_div).to_have_attribute("id", expected_id, timeout=10000)
        print(f"DEBUG: Store ID matches: {expected_id}")

        title = store_div.locator("button > span > span > span.hnf-choice-item__title")
        expect(title).to_have_text(expected_text, timeout=5000)
        print(f"DEBUG: Store name matches: {expected_text}")
    
    # Click on the first store
    def select_store(self, store_div):
        button = store_div.get_by_role("button")
        button.click()
        print("DEBUG: Clicked store button")

    # Check that the selected store name appears in the header
    def verify_selected_store(self, expected_text: str):
        selected = self.page.locator("#hnf-header-storepicker > a > span.hnf-utilities__value")
        selected.wait_for(state="visible", timeout=10000)
        expect(selected).to_have_text(expected_text, timeout=10000)
        print(f"DEBUG: Verified selected store name in header: '{expected_text}'")