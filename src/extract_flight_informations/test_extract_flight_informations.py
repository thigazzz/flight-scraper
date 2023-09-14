import pytest
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from extract_flight_informations import WebRobot
from utils import format_date, get_today_date, get_date_after_a_week_from_today


def generate_mock_air_travel_settings():
    from_where = "São Paulo"
    to_where = "Rio de Janeiro"
    departure_date = format_date(get_today_date(), "%d %B %Y").split(" ")
    return_date = format_date(get_date_after_a_week_from_today(), "%d %B %Y").split(" ")
    print(departure_date, return_date)
    return [
        from_where,
        to_where,
        {"dia": departure_date[0], "mes": departure_date[1], "ano": departure_date[2]},
        {"dia": return_date[0], "mes": return_date[1], "ano": return_date[2]},
    ]


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
    mock_air_travel_settings = generate_mock_air_travel_settings()

    web_robot.access_skyscanner_site()
    web_robot.insert_air_travel_settings(mock_air_travel_settings)

    assert (
        f'{format_date(get_today_date(), "%d/%-m")}'
        in web_robot.web_driver.find_element(
            By.CSS_SELECTOR,
            'span[aria-label="Seleção da data de início no calendário"] span:nth-child(2)',
        ).text
    )
    assert (
        f'{format_date(get_date_after_a_week_from_today(), "%d/%-m")}'
        in web_robot.web_driver.find_element(
            By.CSS_SELECTOR,
            'span[aria-label="Seleção da data de término no calendário"] span:nth-child(2)',
        ).text
    )
