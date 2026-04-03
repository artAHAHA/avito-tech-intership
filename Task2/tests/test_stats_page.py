import time
import pytest
from pages.stats_page import StatsPage


@pytest.fixture
def stats_page(driver):
    base_url = "https://cerulean-praline-8e5aa6.netlify.app/"
    page = StatsPage(driver)
    page.navigate_to_stats_page(base_url)
    return page


class TestStatsPage:

    def test_refresh_button_resets_timer_to_5_minutes(self, stats_page):
        initial = stats_page.get_timer_value()
        if initial in ("5:00", "05:00"):
            stats_page.wait_timer_decreases(initial)

        time.sleep(2)
        stats_page.click_refresh()

        stats_page.wait_for_timer_reset()

        final_value = stats_page.get_timer_value()
        assert final_value in ("5:00", "05:00", "4:59", "04:59"), \
            f"Таймер должен был сброситься, но получили {final_value}"

    def test_stop_timer_button_stops_countdown(self, stats_page):
        if not stats_page.is_timer_displayed():
            stats_page.click_start()
            stats_page.wait.until(lambda d: stats_page.is_timer_displayed())

        stats_page.click_stop()

        stats_page.wait.until(
            lambda d: not stats_page.is_timer_displayed(),
            message="Цифры таймера не исчезли после остановки"
        )

        assert stats_page.is_disabled_message_displayed(), \
            "Надпись 'Автообновление выключено' не появилась!"

    def test_start_timer_button_resumes_countdown(self, stats_page):
        if stats_page.is_timer_displayed():
            stats_page.click_stop()

        stats_page.wait.until(lambda d: stats_page.is_disabled_message_displayed())

        stats_page.click_start()

        stats_page.wait.until(
            lambda d: stats_page.is_timer_displayed(),
            message="Таймер не появился снова после нажатия кнопки запуска"
        )

        initial_val = stats_page.get_timer_value()
        time.sleep(2)
        assert stats_page.get_timer_value() != initial_val, "Таймер появился, но цифры не меняются"