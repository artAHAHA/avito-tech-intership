import time

import pytest
from pages.main_page import MainPage

BASE_URL = "https://cerulean-praline-8e5aa6.netlify.app/"

class TestMainPage:

    def test_price_filter(self, driver):
        driver.get(BASE_URL)
        main_page = MainPage(driver)
        main_page.set_price_range("5000", "15000")
        prices = main_page.get_all_prices()
        if not prices:
            pytest.skip("Нет объявлений в диапазоне 5000-15000")
        for price in prices:
            assert 5000 <= price <= 15000, f"Цена {price} вне диапазона"

    def test_sort_by_price_desc(self, driver):
        driver.get(BASE_URL)
        main_page = MainPage(driver)
        main_page.sort_by_price_desc()
        prices = main_page.get_all_prices()
        if len(prices) < 2:
            pytest.skip("Недостаточно объявлений для проверки сортировки")
        assert prices == sorted(prices, reverse=True), f"Цены не отсортированы: {prices}"

    def test_sort_by_price_asc(self, driver):
        driver.get(BASE_URL)
        main_page = MainPage(driver)
        main_page.sort_by_price_asc()
        prices = main_page.get_all_prices()
        if len(prices) < 2:
            pytest.skip("Недостаточно объявлений для проверки сортировки")
        assert prices == sorted(prices), f"Цены не отсортированы: {prices}"

    def test_category_filter(self, driver):
        driver.get(BASE_URL)
        main_page = MainPage(driver)
        category = "Электроника"
        main_page.filter_by_category(category)
        time.sleep(1)
        categories = main_page.get_all_categories()
        if not categories:
            pytest.skip(f"Нет объявлений в категории {category}")
        for cat in categories:
            assert cat == category, f"Категория {cat} не соответствует {category}"

    def test_urgent_toggle(self, driver):
        driver.get(BASE_URL)
        main_page = MainPage(driver)
        main_page.toggle_urgent(True)
        urgent_count = main_page.get_urgent_items_count()
        all_items = len(main_page.driver.find_elements(*main_page.ITEM_PRICES))
        if all_items == 0:
            pytest.skip("Нет объявлений после включения тогла")
        assert all_items == urgent_count, "Есть объявления без срочной пометки"