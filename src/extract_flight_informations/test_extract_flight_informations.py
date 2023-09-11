import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from extract_flight_informations import WebRobot


@pytest.fixture
def driver():
    driver = webdriver.Edge()
    driver.implicitly_wait(10)
    driver.maximize_window()
    return driver


@pytest.fixture
def web_robot(driver):
    web_robot = WebRobot(driver)
    return web_robot


@pytest.mark.web_process
def test_access_the_skyscanner_site(web_robot: WebRobot):
    web_robot.access_skyscanner_site()
    assert (
        web_robot.web_driver.find_element(By.CLASS_NAME, "logo-image").is_displayed()
        == True
    )


@pytest.mark.web_process
def test_insert_user_air_travel_settings_in_search_inputs(web_robot: WebRobot):
    mock_air_travel_settings = [
        "São Paulo",
        "Rio de Janeiro",
        {"dia": "15", "mes": "setembro", "ano": "2023"},
        {"dia": "18", "mes": "setembro", "ano": "2023"},
    ]

    web_robot.access_skyscanner_site()
    web_robot.insert_air_travel_settings(mock_air_travel_settings)

    assert (
        "15/9"
        in web_robot.web_driver.find_element(
            By.CSS_SELECTOR,
            'span[aria-label="Seleção da data de início no calendário"] span:nth-child(2)',
        ).text
    )
    assert (
        "18/9"
        in web_robot.web_driver.find_element(
            By.CSS_SELECTOR,
            'span[aria-label="Seleção da data de término no calendário"] span:nth-child(2)',
        ).text
    )
