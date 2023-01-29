from time import sleep

from settings.UserSettings import MetaMaskId


class MetaMaskScript:
    homeUrl = f"chrome-extension://{MetaMaskId}/home.html"
    popupUrl = f"chrome-extension://{MetaMaskId}/popup.html"

    @staticmethod
    def initMetaMask(browser, mnemo, index):
        sleep(15)
        page = browser.pages[0]
        page.goto(MetaMaskScript.homeUrl)
        for i in range(0, 5):
            psdCount = page.locator('[id="password"][autocomplete="current-password"]').count()
            createCount = page.locator('[data-testid="first-time-flow__button"]').count()
            if psdCount > 0 or createCount > 0:
                break
            else:
                sleep(1)
        if psdCount > 0:
            page.fill('[id="password"][autocomplete="current-password"]', '12345678')
            page.click('[data-testid="unlock-submit"]')
            sleep(10)
        elif createCount > 0:
            page.click('[data-testid="first-time-flow__button"]')
            page.click('[data-testid="page-container-footer-next"]')
            page.click('[data-testid="import-wallet-button"]')
            for i in range(len(mnemo.split(' '))):
                page.fill(f'[id="import-srp__srp-word-{i}"]', mnemo.split(' ')[i])
            page.fill('[autocomplete="new-password"][id="password"]', '12345678')
            page.fill('[autocomplete="new-password"][id="confirm-password"]', '12345678')
            page.click('[id="create-new-vault__terms-checkbox"]')
            page.click('[class="button btn--rounded btn-primary create-new-vault__submit-button"]')
            page.click('[data-testid="EOF-complete-button"]')
        else:
            print(f"第{str(index)}个账号出现异常")
