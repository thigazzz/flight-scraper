import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from datetime import datetime


class WebRobot:
    def __init__(self, driver: WebDriver) -> None:
        self.web_driver = driver

    def access_skyscanner_site(self):
        self.web_driver.get("https://www.kayak.com.br/")
        # try:
        #     if self.web_driver.find_element(By.XPATH, "//*[text()='Are you a person or a robot?']"):
        #         time.sleep(3)
        #         self.__break_captcha()
        # except:
        #     pass

    def __break_captcha(self):
        self.web_driver.find_element(
            By.XPATH, "//*[text()='Are you a person or a robot?']"
        ).click()
        actions = ActionChains(self.web_driver)
        actions.send_keys(Keys.TAB)
        actions.key_down(Keys.ENTER)
        actions.perform()
        time.sleep(10)
        actions.key_up(Keys.ENTER)
        actions.perform()

    def insert_air_travel_settings(self, air_travel_settings: list):
        from_where, to_where, departure_date, return_date = air_travel_settings

        self.web_driver.find_element(
            By.CSS_SELECTOR, "input[aria-label='Campo de origem']"
        ).send_keys(from_where)
        self.web_driver.find_element(
            By.CSS_SELECTOR, "input[placeholder='Destino']"
        ).send_keys(to_where)

        self.web_driver.find_element(
            By.CSS_SELECTOR,
            "span[aria-label='Seleção da data de início no calendário']",
        ).click()

        while True:
            displayed_months = self.web_driver.find_elements(
                By.CLASS_NAME, "onx_-double"
            )
            months = []
            for displayed_month in displayed_months:
                year_and_month = displayed_month.get_attribute("data-month")
                year_and_month = year_and_month.split("-")

                months.append(int(f"{year_and_month[0]}{year_and_month[1]}"))

            init_month = int(
                datetime.strptime(
                    f"{departure_date['ano']}{departure_date['mes']}", "%Y%B"
                )
                .date()
                .strftime("%Y%m")
            )

            if init_month < months[0]:
                print(
                    "mes escolhido para inicio é menor e nao esta sendo mostrado na tela"
                )
                self.web_driver.find_element(
                    By.CSS_SELECTOR, 'button[aria-label="Mês anterior"]'
                ).click()
            elif init_month > months[1]:
                print(
                    "mes escolhido para inicio  é maior e nao esta sendo mostrado na tela"
                )
                self.web_driver.find_element(
                    By.CSS_SELECTOR, 'button[aria-label="Próximo mês"]'
                ).click()
            else:
                print(
                    f"div[aria-label*='{departure_date['dia']} de {departure_date['mes']} de {departure_date['ano']}']"
                )
                self.web_driver.find_element(
                    By.CSS_SELECTOR,
                    f"div[aria-label*='{departure_date['dia']} de {departure_date['mes']} de {departure_date['ano']}']",
                ).click()
                print("mes esta sendo mostrado na tela")
                break

        self.web_driver.find_element(
            By.CSS_SELECTOR,
            "span[aria-label='Seleção da data de término no calendário']",
        ).click()
        while True:
            displayed_months = self.web_driver.find_elements(
                By.CLASS_NAME, "onx_-double"
            )
            months = []
            for displayed_month in displayed_months:
                year_and_month = displayed_month.get_attribute("data-month")
                year_and_month = year_and_month.split("-")

                months.append(int(f"{year_and_month[0]}{year_and_month[1]}"))

            init_month = int(
                datetime.strptime(f"{return_date['ano']}{return_date['mes']}", "%Y%B")
                .date()
                .strftime("%Y%m")
            )

            if init_month < months[0]:
                print(
                    "mes escolhido para inicio é menor e nao esta sendo mostrado na tela"
                )
                self.web_driver.find_element(
                    By.CSS_SELECTOR, 'button[aria-label="Mês anterior"]'
                ).click()
            elif init_month > months[1]:
                print(
                    "mes escolhido para inicio  é maior e nao esta sendo mostrado na tela"
                )
                self.web_driver.find_element(
                    By.CSS_SELECTOR, 'button[aria-label="Próximo mês"]'
                ).click()
            else:
                print(
                    f"div[aria-label*='{return_date['dia']} de {return_date['mes']} de {return_date['ano']}']"
                )
                self.web_driver.find_element(
                    By.CSS_SELECTOR,
                    f"div[aria-label*='{return_date['dia']} de {return_date['mes']} de {return_date['ano']}']",
                ).click()
                print("mes esta sendo mostrado na tela")
                break


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
@pytest.mark.skip(reason="a")
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


# aria-label="quinta, 7 de setembro de 2023. preço médio. Selecionar como data de ida"
