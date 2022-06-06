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

            # self.browser = webdriver.Chrome(ChromeDriverManager().install())
            # chrome_options = webdriver.ChromeOptions()
            # chrome_options.add_argument('--no-sandbox')
            # chrome_options.add_argument('--headless')
            # chrome_options.add_argument('--disable-gpu')
            # self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        except:
            pass

    def get_browser(self):
        return self.browser
