from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage

class ThemeSwitchPage(BasePage):
    THEME_TOGGLE = (By.CSS_SELECTOR, "button._themeToggle_127us_1")

    def click_theme_toggle(self):
        """Клик по кнопке переключения темы"""
        self.click(self.THEME_TOGGLE)

    def get_theme_toggle_aria_label(self) -> str:
        """Возвращает aria-label кнопки (например, 'Switch to dark theme' или 'Switch to light theme')"""
        element = self.find_element(self.THEME_TOGGLE)
        return element.get_attribute("aria-label")

    def get_theme_toggle_text(self) -> str:
        """Возвращает текст кнопки ('Темная' или 'Светлая')"""
        return self.get_text(self.THEME_TOGGLE)  # берёт текст из span._label_127us_35

    def get_body_background_color(self) -> str:
        """Возвращает CSS background-color элемента body (для проверки смены темы)"""
        body = self.driver.find_element(By.TAG_NAME, "body")
        return body.value_of_css_property("background-color")

    def wait_for_theme_change(self, old_aria_label: str, timeout: int = 5):
        """Ожидает, пока aria-label кнопки не изменится"""
        WebDriverWait(self.driver, timeout, poll_frequency=0.2).until(
            lambda d: self.get_theme_toggle_aria_label() != old_aria_label,
            message="Тема не переключилась: aria-label не изменился"
        )