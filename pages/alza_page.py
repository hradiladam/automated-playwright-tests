# pages/alza_page.py

from playwright.sync_api import Page, expect, TimeoutError
from helpers.helper_google_popup_decline import dismiss_google_popup_if_present

class AlzaPage:
    def __init__(self, page: Page):
        self.page = page

    def goto_home(self):
        self.page.goto("https://www.alza.cz/")
    
    def accept_cookies(self):
        try:
            btn = self.page.get_by_role("link", name="Rozumím")
            if btn.is_visible(timeout=5000):
                btn.click()
                print("\nDEBUG: Cookie button clicked")
        except:
            print("\nDEBUG: Cookie button not found or failed to click")

    # ---Switch to Eng---
    def switch_to_english(self):
        lang_btn = self.page.get_by_test_id("headerLanguageSwitcher").get_by_role("img", name="CZ")
        lang_btn.wait_for(state="visible", timeout=10000)
        lang_btn.click()
        print("DEBUG: Clicked language button")

        lang_tab = self.page.get_by_text("Alza.cz - Jazyk / LanguageČeš")
        lang_tab.wait_for(state="visible")
        print("DEBUG: Language panel visible")

        eng_btn = self.page.get_by_role("button", name="English English")
        eng_btn.click()

        confirm_lang_btn = self.page.get_by_role("button", name="Potvrdit / Confirm")
        confirm_lang_btn.click()
        print("DEBUG: Selected English language")
        
        self.page.wait_for_load_state("load")

    def get_current_url(self):
        return self.page.url        
    
    # --- Search for item and add it to cart---
    def search_and_add_to_cart(self, item:str):
        searchbox = self.page.get_by_role("combobox", name="What are you looking for? E.g")
        searchbox_btn = self.page.get_by_test_id("button-search")

        searchbox.wait_for(state="visible", timeout=5000)
        searchbox.click()
        searchbox.fill(item)

        searchbox_btn.click()

        buy_btn = self.page.locator("a.btnk1").first
        buy_btn.click()
        print("DEBUG: Item added to the cart")

        dismiss_google_popup_if_present(self.page) # Remove google account sign-in popup

    # Return the locator for the cart icon button in the header
    def get_basket_button(self):
        return self.page.get_by_title("Go to Shopping Cart")

    # Check that item was added to cart, go to the cart and check that order page opens
    def go_to_cart(self):
        dismiss_google_popup_if_present(self.page)
        self.get_basket_button().click()
        dismiss_google_popup_if_present(self.page)
    
     # Progress to payment and delviery page
    def proceed_to_payment_and_delivery(self):
        continue_btn = self.page.get_by_role("link", name="Continue", exact=True)
        continue_btn.wait_for(state="visible")
        continue_btn.click()

        dismiss_google_popup_if_present(self.page)

    # Decline additional item offer if appears
    def decline_additional_items_offer(self):
        try:
            offer_tab = self.page.get_by_text("Do not forget these important things May come in handy This issue can be solved")
            offer_tab.wait_for(state="visible", timeout=5000)  # wait max 5 seconds
            print("DEBUG: Add items panel visible")

            decline_btn = self.page.get_by_text("Do not add anything")
            decline_btn.click()
            print("DEBUG: Declined additional items offer")

        except TimeoutError:
            print("DEBUG: Add items panel did not appear, continuing without declining")
        
        dismiss_google_popup_if_present(self.page)
    
    # Return the locator for the Alza Plus banner on the payment & delivery page
    def get_alza_plus_banner(self):
        return self.page.get_by_text("FREE shipping on everything with AlzaPlus+Activate AlzaPlus+ and get FREE")
    
    # Return the locator for the 1-year Alza Plus membership subscription option
    def get_alza_plus_one_year_option(self):
        return self.page.get_by_test_id("apSubsType1")

    # Return the locator for the monthly Alza Plus subscription option
    def get_alza_plus_monthly_option(self):
        return self.page.get_by_test_id("apSubsType2")

    # Cleanup of the cart
    def empty_cart(self):
        back_btn = self.page.get_by_role("link", name="Back")
        back_btn.click()

        empty_cart_label = self.page.get_by_text("Empty cart")
        empty_cart_label.wait_for(state="visible", timeout=5000)
        empty_cart_label.click()

        flush_button = self.page.get_by_test_id("basketItems_flushButton")
        flush_button.wait_for(state="visible", timeout=5000)
        flush_button.click()

        confirm_button = self.page.get_by_role("button", name="Empty cart")
        confirm_button.wait_for(state="visible", timeout=5000)
        confirm_button.click()