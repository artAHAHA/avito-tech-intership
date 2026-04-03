import re
import time
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class MainPage(BasePage):
    PRICE_FROM = (By.CSS_SELECTOR, "input[placeholder='От']")
    PRICE_TO = (By.CSS_SELECTOR, "input[placeholder='До']")
    PAGINATION_INFO = (By.XPATH, "//*[contains(text(), 'объявлений')]")
    SORT_SELECT = (By.XPATH, "//select[.//option[@value='price']]")
    SORT_TYPE_SELECT = (By.XPATH, "//select[.//option[@value='asc']]")
    CATEGORY_SELECT = (By.XPATH, "//select[.//option[text()='Все категории']]")
    URGENT_TOGGLE_INPUT = (By.XPATH, "//label[contains(., 'Только срочные')]//input[@type='checkbox']")
    URGENT_TOGGLE_LABEL = (By.XPATH, "//label[contains(., 'Только срочные')]")
    ITEM_PRICES = (By.XPATH, "//div[contains(@class, '_card__price_')]")
    ITEM_CATEGORIES = (By.XPATH, "//div[contains(@class, '_card__category_')]")
    URGENT_BADGES = (By.XPATH, "//span[contains(@class, '_card__priority_')]")

    def set_price_range(self, price_from: str, price_to: str):
        self.input_text(self.PRICE_FROM, price_from)
        self.find_element(self.PRICE_FROM).send_keys(Keys.TAB)

        self.input_text(self.PRICE_TO, price_to)
        self.find_element(self.PRICE_TO).send_keys(Keys.ENTER)

        time.sleep(1)

    def sort_by_price_desc(self):
        old_first = self.get_first_item_price()
        self.click(self.SORT_SELECT)
        price_option = (By.XPATH, "//option[@value='price']")
        self.click(price_option)
        time.sleep(1)
        self.click(self.SORT_TYPE_SELECT)
        sort_option = (By.XPATH, "//option[@value='desc']")
        self.click(sort_option)
        time.sleep(1)
        self.wait_for_first_item_change(old_first)

    def sort_by_price_asc(self):
        old_first = self.get_first_item_price()
        self.click(self.SORT_SELECT)
        price_option = (By.XPATH, "//option[@value='price']")
        self.click(price_option)
        time.sleep(1)
        self.click(self.SORT_TYPE_SELECT)
        sort_option = (By.XPATH, "//option[@value='asc']")
        self.click(sort_option)
        time.sleep(1)
        self.wait_for_first_item_change(old_first)

    def filter_by_category(self, category_text: str):
        self.scroll_to_element(self.CATEGORY_SELECT)
        self.click(self.CATEGORY_SELECT)
        category_option = (By.XPATH, f"//option[text()='{category_text}']")
        self.click(category_option)

    def toggle_urgent(self, enable: bool = True):
        checkbox = self.find_element(self.URGENT_TOGGLE_INPUT)

        is_checked = checkbox.is_selected()

        if enable and not is_checked:
            self.click(self.URGENT_TOGGLE_LABEL)

        elif not enable and is_checked:
            self.click(self.URGENT_TOGGLE_LABEL)

    def get_all_prices(self) -> list[int]:
        self.wait.until(EC.presence_of_all_elements_located(self.ITEM_PRICES))

        price_elements = self.driver.find_elements(*self.ITEM_PRICES)
        prices = []
        for elem in price_elements:
            raw = elem.text.replace('₽', '').replace(' ', '').replace('\xa0', '').strip()
            if raw.isdigit():
                prices.append(int(raw))
        return prices

    def get_all_categories(self) -> list[str]:
        categories = self.driver.find_elements(*self.ITEM_CATEGORIES)
        return [c.text for c in categories]

    def get_urgent_items_count(self) -> int:
        return len(self.driver.find_elements(*self.URGENT_BADGES))

    # Дополнительные методы для сортировки
    def get_first_item_price(self) -> str:
        prices = self.driver.find_elements(*self.ITEM_PRICES)
        return prices[0].text if prices else ""

    def wait_for_first_item_change(self, old_text: str):
        self.wait.until(lambda d: self.get_first_item_price() != old_text)