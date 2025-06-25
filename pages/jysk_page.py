# jysk_page

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

        expect(self.page).to_have_url("https://jysk.cz/loznice/matrace")
        print("DEBUG: Page with mattrasses has been loaded")
    
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
        diplay_results_btn = self.page.get_by_role("button", name="Zobrazit výsledky vyhledávání:")
        diplay_results_btn.click()
        print("DEBUG: Results selected")
    
    # Check that filters are registered
    def check_filters(self, quality):
        selected_filters = self.page.locator("div.w3-pills-container").nth(0)
        expect(selected_filters).to_contain_text(quality)
        print("DEBUG: Selected filters have been registered correctly")
    
    # Scroll to the bottom to ensure all products are loaded (lazy loading)
    def scroll_down(self):
        self.page.mouse.wheel(0, 15000)
        self.page.wait_for_timeout(10000)  # Give time for lazy content to load/render
    
    # Count visible mattresses displayed on page after using "quality" in the filter
    # &
    # Individually check each visible product's sticker text matches quality (case-insensitive)
    def count_visible_mattrases(self, quality):
        product_locator = self.page.locator("div.product-teaser-body")
        total_products = product_locator.count()
        visible_count = sum(product_locator.nth(i).is_visible() for i in range(total_products))
        print(f"DEBUG: There are {visible_count} displayed mattresses after applying the quality filter: {quality}")

        for i in range(total_products):
            product = product_locator.nth(i)
            if product.is_visible():
                sticker = product.locator("span.sticker-text")
                sticker_text = sticker.text_content()
                # Only check if sticker text is not empty
                if sticker_text:
                    expect(sticker).to_have_text(quality, ignore_case=True)

        print(f"DEBUG: All displayed products' quality stickers match selected quality of: {quality}")