from selenium.common import StaleElementReferenceException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pages.base_page import BasePage



class StatsPage(BasePage):
    STATS_LINK = (By.CSS_SELECTOR, "a[href='/stats']")
    REFRESH_BTN = (By.CSS_SELECTOR, "button[aria-label='Обновить сейчас']")
    STOP_BTN = (By.CSS_SELECTOR, "button[aria-label='Отключить автообновление']")
    START_BTN = (By.CSS_SELECTOR, "button[aria-label='Включить автообновление']")
    TIMER_VALUE = (By.CSS_SELECTOR, "span[class*='_timeValue_']")
    DISABLED_TEXT = (By.XPATH, "//*[contains(text(), 'Автообновление выключено')]")

    def navigate_to_stats_page(self, base_url: str):
        """
        Открывает главную страницу и переходит в раздел статистики.
        """
        self.driver.get(base_url)
        self.wait_page_loaded()
        self.click(self.STATS_LINK)
        # Ждём, когда загрузится страница статистики (появление индикатора таймера)
        self.wait.until(lambda d: self.is_element_visible(self.TIMER_VALUE))

    def click_refresh(self):
        self.click(self.REFRESH_BTN)

    def click_stop(self):
        self.click(self.STOP_BTN)

    def click_start(self):
        self.click(self.START_BTN)


    def get_timer_value(self) -> str:
        """Прямое получение цифр таймера"""
        try:
            element = self.wait.until(EC.visibility_of_element_located(self.TIMER_VALUE))
            return element.text.strip()
        except (StaleElementReferenceException, TimeoutException):
            return ""


    def wait_timer_decreases(self, old_value: str):
        """Ждет, пока цифры на таймере изменятся (уменьшатся)"""
        self.wait.until(
            lambda d: self.get_timer_value() != old_value and self.get_timer_value() != "",
            message=f"Таймер застыл на значении {old_value}"
        )


    def wait_for_timer_reset(self):
        """Ждет, пока таймер сбросится до 5:00"""
        self.wait.until(
            lambda d: self.get_timer_value() in ("5:00", "05:00"),
            message=f"Таймер не сбросился до 5:00. Текущее значение: {self.get_timer_value()}"
        )

    def is_timer_displayed(self) -> bool:
        """Проверяет, видны ли цифры таймера на странице"""
        try:
            # Используем короткое ожидание, чтобы тест не тупил 10 секунд
            return self.driver.find_element(*self.TIMER_VALUE).is_displayed()
        except:
            return False

    def is_disabled_message_displayed(self) -> bool:
        """Проверяет, появилось ли сообщение об отключении"""
        try:
            return self.driver.find_element(*self.DISABLED_TEXT).is_displayed()
        except:
            return False