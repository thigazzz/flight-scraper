from typing import List
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import utils
import pyautogui
import time


class WebRobot:
    def __init__(self, driver: WebDriver):
        self.web_driver = driver

    def access_skyscanner_site(self):
        self.web_driver.get("https://www.kayak.com.br/")

    def search_air_travels(self):
        self.web_driver.find_element(
            By.CSS_SELECTOR, 'button[aria-label="Buscar"]'
        ).click()

    def extract_air_travels_informations(self):
        time.sleep(10)
        self.web_driver.switch_to.window(self.web_driver.window_handles[1])

        informations = []
        travel_cards = self.web_driver.find_elements(
            By.CSS_SELECTOR, 'div.resultsList div[class*="wrapper"] div[class*="inner"]'
        )
        for travel_card in travel_cards:
            price = travel_card.find_element(
                By.CSS_SELECTOR,
                'div[class*="price"] div[class*="price-text-container"] div[class*="price-text"]',
            ).text
            item_cards = travel_card.find_elements(
                By.CSS_SELECTOR, 'div[class*="main"] li[class*="item"]'
            )
            for item_card in item_cards:
                departure_time = item_card.find_element(
                    By.CSS_SELECTOR,
                    'div[class*="stacked"] + div > div span:first-child',
                ).text
                disembarkation_time = item_card.find_element(
                    By.CSS_SELECTOR,
                    'li[class*="item"] div[class*="stacked"] + div > div span:last-child',
                ).text
                informations.append(
                    {
                        "price": price,
                        "departure time": departure_time,
                        "disembarkation time": disembarkation_time,
                    }
                )
        return informations

    def insert_air_travel_settings(self, air_travel_settings: list):
        from_where, to_where, departure_date, return_date = air_travel_settings
        wait = WebDriverWait(self.web_driver, timeout=5)
        time.sleep(60)

        self.web_driver.find_element(
            By.CSS_SELECTOR, "input[aria-label='Campo de origem']"
        ).send_keys(from_where)
        wait.until(
            lambda d: EC.element_to_be_selected(
                self.web_driver.find_element(
                    By.CSS_SELECTOR, 'div[role="presentation"][tabindex="-1"]'
                )
            )
        )
        wait.until(
            lambda d: EC.element_to_be_selected(
                self.web_driver.find_element(
                    By.CSS_SELECTOR,
                    f'ul[role="listbox"] li[role="option"][aria-label*="{from_where}"]',
                )
            )
        )
        pyautogui.press("enter")

        self.web_driver.find_element(
            By.CSS_SELECTOR, "input[placeholder='Destino']"
        ).send_keys(to_where)
        wait.until(
            lambda d: EC.element_to_be_selected(
                self.web_driver.find_element(
                    By.CSS_SELECTOR, 'div[role="presentation"][tabindex="-1"]'
                )
            )
        )
        wait.until(
            lambda d: EC.element_to_be_selected(
                self.web_driver.find_element(
                    By.CSS_SELECTOR,
                    f'ul[role="listbox"] li[role="option"][aria-label*="{to_where}"]',
                )
            )
        )
        pyautogui.press("enter")

        self.web_driver.find_element(
            By.CSS_SELECTOR,
            "span[aria-label='Seleção da data de início no calendário']",
        ).click()
        self.insert_date(departure_date)

        self.web_driver.find_element(
            By.CSS_SELECTOR,
            "span[aria-label='Seleção da data de término no calendário']",
        ).click()
        self.insert_date(return_date)

    def insert_date(self, date: dict):
        while True:
            displayed_months_on_screen = self.get_months_displayed_on_screen()
            month = utils.convert_date_in_a_number(
                [
                    str(date["ano"]),
                    datetime.strptime(f"{date['mes']}", "%B").date().strftime("%m"),
                ]
            )

            if self.is_defined_month_displayed_on_screen(
                month, displayed_months_on_screen
            ):
                self.web_driver.find_element(
                    By.CSS_SELECTOR,
                    f"div[aria-label*='{date['dia']} de {date['mes']} de {date['ano']}']",
                ).click()
                break

    def get_months_displayed_on_screen(self):
        displayed_months = self.web_driver.find_elements(By.CLASS_NAME, "onx_-double")
        months = []
        for displayed_month in displayed_months:
            year_and_month = displayed_month.get_attribute("data-month").split("-")
            months.append(utils.convert_date_in_a_number(year_and_month))
        return months

    def is_defined_month_displayed_on_screen(
        self, month: int, months_displayed_on_screen: List[int]
    ) -> bool:
        if utils.is_month_earlier_than_the_first_one_shown_on_the_screen(
            month, months_displayed_on_screen[0]
        ):
            self.back_months_displayed_on_screen()
            return False
        elif utils.is_month_later_than_the_second_one_shown_on_the_screen(
            month, months_displayed_on_screen[1]
        ):
            self.advance_months_displayed_on_screen()
            return False
        return True

    def back_months_displayed_on_screen(self):
        self.web_driver.find_element(
            By.CSS_SELECTOR, 'button[aria-label="Mês anterior"]'
        ).click()

    def advance_months_displayed_on_screen(self):
        self.web_driver.find_element(
            By.CSS_SELECTOR, 'button[aria-label="Próximo mês"]'
        ).click()
