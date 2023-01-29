from playwright import sync_api


class BrowserSettings:

    @staticmethod
    def get_browser(port):
        playwright = sync_api.sync_playwright().start()
        browser = playwright.chromium.connect_over_cdp(f"http://127.0.0.1:{str(port)}")
        context = browser.contexts[0]
        return context
