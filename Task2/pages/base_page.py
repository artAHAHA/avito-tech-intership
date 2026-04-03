import time

from selenium.webdriver import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10, poll_frequency=0.5)

    def find_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator):
        return self.wait.until(EC.visibility_of_all_elements_located(locator))

    def click(self, locator):
        element = self.scroll_to_element(locator)
        element.click()

    def input_text(self, locator, text):
        element = self.scroll_to_element(locator)
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.BACKSPACE)
        element.send_keys(text)


    def get_text(self, locator):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        return element.text

    def wait_page_loaded(self):
        self.wait.until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    def is_element_visible(self, locator):
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    def scroll_to_element(self, locator):
        element = self.wait.until(EC.presence_of_element_located(locator))

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
            element
        )

        time.sleep(0.3)

        self.wait.until(EC.visibility_of_element_located(locator))
        return element
