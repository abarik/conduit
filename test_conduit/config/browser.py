from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


class Browser:
    def __init__(self):
        try:
            browser_options = Options()
            browser_options.headless = True
            self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=browser_options)
            self.browser.implicitly_wait(10)
            self.browser.maximize_window()
        except:
            pass

    def get_browser(self):
        return self.browser
