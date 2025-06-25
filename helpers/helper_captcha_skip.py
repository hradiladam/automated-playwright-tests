# helper_captcha_skip.py
def is_human_interaction_required(page):
    # Common phrases and selectors for human verification
    human_check_phrases = [
        "potvrďte, že jste člověk",
        "potvrďte, že nejste robot",
        "jste z masa a kostí",
        "ověřte, že jste člověk",
        "ověření člověka",
        "human verification",
        "verify you are human",
        "please stand by",
        "checking your browser",
        "press and hold",
        "complete the security check"
    ]

    # Check for text-based indicators
    for phrase in human_check_phrases:
        try:
            if page.get_by_text(phrase, exact=False).is_visible(timeout=1000):
                return True
        except:
            continue

    # Check for known CAPTCHA-related elements
    try:
        if page.locator('iframe[src*="recaptcha"]').is_visible(timeout=1000):
            return True
        if page.locator('iframe[src*="hcaptcha"]').is_visible(timeout=1000):
            return True
        if page.locator('div.g-recaptcha').is_visible(timeout=1000):
            return True
        if page.locator('div.h-captcha').is_visible(timeout=1000):
            return True
        if page.locator('div[id*="captcha"]').is_visible(timeout=1000):
            return True
        if page.locator('input[name="captcha"]').is_visible(timeout=1000):
            return True
    except:
        pass

    return False
