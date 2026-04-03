import pytest
from pages.theme_switch import ThemeSwitchPage

@pytest.fixture
def theme_page(mobile_driver):
    base_url = "https://cerulean-praline-8e5aa6.netlify.app"
    page = ThemeSwitchPage(mobile_driver)
    mobile_driver.get(base_url)
    page.wait_page_loaded()
    return page

class TestThemeSwitch:

    def test_theme_switches_from_light_to_dark_and_back(self, theme_page):
        """
        Проверяет, что при клике на кнопку тема переключается (светлая -> тёмная -> светлая).
        Критерий: изменение aria-label кнопки.
        """

        old_label = theme_page.get_theme_toggle_aria_label()

        theme_page.click_theme_toggle()

        theme_page.wait_for_theme_change(old_label)
        new_label = theme_page.get_theme_toggle_aria_label()
        assert new_label != old_label, "Тема не переключилась после первого клика"

        theme_page.click_theme_toggle()
        theme_page.wait_for_theme_change(new_label)
        final_label = theme_page.get_theme_toggle_aria_label()
        assert final_label == old_label, "Тема не вернулась в исходное состояние"

