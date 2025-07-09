# pages/jysk_page.py

from playwright.sync_api import Page, expect

class JyskPage:
    def __init__(self, page: Page):
        self.page = page
    
    def goto_home(self):
        self.page.goto("https://www.jysk.cz/")
    
    def accept_cookies(self):
        try:
            btn = self.page.get_by_role("button", name="Nezbytně nutné")
            if btn.is_visible(timeout=5000):
                btn.click()
                print("\nDEBUG: Cookie button clicked")
        except:
            print("\nDEBUG: Cookie button not found or failed to click")
    
    # Selecting category of mattrasses
    def select_category_of_mattrasses(self):
        menu_btn = self.page.get_by_role("link", name="Menu")
        menu_btn.click()

        menu_bar = self.page.locator("#mega-menu-content > div > div.off-canvas-container.lowerModal-container")
        menu_bar.wait_for(state="visible", timeout=10000)
        expect(menu_bar).to_be_visible(timeout=10000)
        print("DEBUG: Menu displayed")

        mattrases_btn = self.page.get_by_role("link", name="Postele a matrace")
        mattrases_btn.click()
        
        show_all_btn = self.page.get_by_role("link", name="Zobrazit vše")
        show_all_btn.click()
        print("DEBUG: Page with mattrasses has been loaded")

    # Get the current URL
    def get_current_url(self):
        return self.page.url
    
    # Choosing quality
    def choosing_quality(self, quality):
        all_filters_btn = self.page.get_by_role("button", name="Všechny filtry")
        all_filters_btn.wait_for(state="visible")
        all_filters_btn.click()

        filters_bar = self.page.locator("div.off-canvas-content.off-canvas-content--sticky").filter(has_text="Filtry")
        filters_bar.wait_for(state="visible", timeout=25000)
        expect(filters_bar).to_be_visible(timeout=25000)
        print("DEBUG: Menu with filters for mattresses is diplayed")

        quality_btn = self.page.get_by_role("button", name="Kvalita", exact=True)
        quality_btn.click()

        quality_checkbox = self.page.get_by_role("checkbox", name=quality)
        quality_checkbox.check()
        print("DEBUG: Quality selected")

    # Display results
    def display_results(self):
        display_results_btn = self.page.get_by_role("button", name="Zobrazit výsledky vyhledávání:")
        display_results_btn.click()
        print("DEBUG: Results selected")
    
    # Return the locator for the selected filters pill container
    # Used to verify that the applied filter (e.g. quality) is visible on the UI 
    def get_selected_filters(self):
        return self.page.locator("div.w3-pills-container").nth(0)
    
    # Scroll to the bottom of the page to trigger lazy loading of more products
    def scroll_down(self):
        self.page.mouse.wheel(0, 15000)
        self.page.wait_for_timeout(10000)  # Lazy load wait

    # Return a list of all mattress product elements currently visible on the page
    def get_visible_mattress_products(self):
        product_locator = self.page.locator("div.product-teaser-body")
        total = product_locator.count()
        visible_products = []

        for i in range(total):
            product = product_locator.nth(i)
            if product.is_visible():
                visible_products.append(product)

        return visible_products

    # Extract the text from the quality sticker of a single visible product
    def get_sticker_text(self, product):
        sticker = product.locator("span.sticker-text")
        return sticker.text_content() or ""