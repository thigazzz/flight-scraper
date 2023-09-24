from typing import List
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import utils
import pyautogui
import time


class Robot:
    def __init__(self, driver: WebDriver, timeout: int = 5):
        self.web_driver = driver
        self.wait = WebDriverWait(self.web_driver, timeout=5)

    def access_site(self, url: str):
        self.web_driver.get(url)

    def find_element(self, selector: str, by: str = "CSS_SELECTOR"):
        by_type = getattr(By, by.upper())
        return self.web_driver.find_element(by_type, selector)

    def click_element(self, selector: str, by: str = "CSS_SELECTOR") -> None:
        self.find_element(selector=selector, by=by).click()

    def get_text(self, selector: str, by: str = "CSS_SELECTOR") -> str:
        return self.find_element(selector=selector, by=by).text

    def wait_element(self, waiter: str, selector: str, by: str = "CSS_SELECTOR"):
        waiter = getattr(EC, waiter)
        self.wait.until(lambda d: waiter(self.find_element(selector=selector, by=by)))


class WebRobot(Robot):
    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def access_skyscanner_site(self):
        self.access_site("https://www.kayak.com.br/")

    def search_air_travels(self):
        self.click_element('button[aria-label="Buscar"]')

    def extract_air_travels_informations(self):
        time.sleep(15)
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

        self.insert_destination(from_where, "input[aria-label='Campo de origem']")
        self.insert_destination(to_where, "input[placeholder='Destino']")

        self.click_element("span[aria-label='Seleção da data de início no calendário']")
        self.insert_date(departure_date)
        self.click_element(
            "span[aria-label='Seleção da data de término no calendário']"
        )
        self.insert_date(return_date)

    def insert_destination(self, destination: str, selector: str):
        self.web_driver.find_element(By.CSS_SELECTOR, selector).send_keys(destination)
        self.wait_destination_dropbox_appears(destination)
        pyautogui.press("enter")

    def wait_destination_dropbox_appears(self, destination: str):
        self.wait_element(
            "element_to_be_selected", 'div[role="presentation"][tabindex="-1"]'
        )
        self.wait_element(
            "element_to_be_selected",
            f'ul[role="listbox"] li[role="option"][aria-label*="{destination}"]',
        )

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
                self.click_element(
                    f"div[aria-label*='{date['dia']} de {date['mes']} de {date['ano']}']"
                )
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
        self.click_element('button[aria-label="Mês anterior"]')

    def advance_months_displayed_on_screen(self):
        self.click_element('button[aria-label="Próximo mês"]')
