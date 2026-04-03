import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.fixture
def mobile_driver():
    options = webdriver.ChromeOptions()
    mobile_emulation = {"deviceName": "iPhone 12 Pro"}
    options.add_experimental_option("mobileEmulation", mobile_emulation)

    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()