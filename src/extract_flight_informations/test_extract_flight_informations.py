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


@pytest.mark.skip(reason="a")
@pytest.mark.web_process
def test_access_site(web_robot: WebRobot):
    web_robot.access_skyscanner_site()
    assert (
        web_robot.web_driver.find_element(By.CLASS_NAME, "logo-image").is_displayed()
        == True
    )


@pytest.mark.skip(reason="a")
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


@pytest.mark.web_process
def test_extract_air_travel_main_informations_from_site(web_robot: WebRobot):
    mock_air_travel_settings = generate_mock_air_travel_settings()

    web_robot.access_skyscanner_site()
    web_robot.insert_air_travel_settings(mock_air_travel_settings)
    web_robot.search_air_travels()
    informations_extracted = web_robot.extract_air_travels_informations()

    index = 0
    travel_cards = web_robot.web_driver.find_elements(
        By.CSS_SELECTOR, 'div.resultsList div[class*="wrapper"] div[class*="inner"]'
    )
    for travel_card in travel_cards:
        item_cards = travel_card.find_elements(
            By.CSS_SELECTOR, 'div[class*="main"] li[class*="item"]'
        )
        for item_card in item_cards:
            assert (
                travel_card.find_element(
                    By.CSS_SELECTOR,
                    'div[class*="price"] div[class*="price-text-container"] div[class*="price-text"]',
                ).text
                == informations_extracted[index]["price"]
            )
            assert (
                item_card.find_element(
                    By.CSS_SELECTOR,
                    'div[class*="stacked"] + div > div span:first-child',
                ).text
                == informations_extracted[index]["departure time"]
            )
            assert (
                item_card.find_element(
                    By.CSS_SELECTOR,
                    'li[class*="item"] div[class*="stacked"] + div > div span:last-child',
                ).text
                == informations_extracted[index]["disembarkation time"]
            )
            index += 1
