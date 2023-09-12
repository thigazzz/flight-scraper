from typing import List
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.webdriver import WebDriver
from utils import (
    is_month_earlier_than_the_first_one_shown_on_the_screen,
    is_month_later_than_the_second_one_shown_on_the_screen,
)


class WebRobot:
    def __init__(self, driver: WebDriver):
        self.web_driver = driver

    def access_skyscanner_site(self):
        self.web_driver.get("https://www.kayak.com.br/")

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
        self.insert_day(departure_date)

        self.web_driver.find_element(
            By.CSS_SELECTOR,
            "span[aria-label='Seleção da data de término no calendário']",
        ).click()
        self.insert_day(return_date)

    def insert_day(self, date: dict):
        while True:
            # pego meses na tela e formato
            displayed_months = self.web_driver.find_elements(
                By.CLASS_NAME, "onx_-double"
            )
            months = []
            for displayed_month in displayed_months:
                year_and_month = displayed_month.get_attribute("data-month")
                year_and_month = year_and_month.split("-")

                months.append(int(f"{year_and_month[0]}{year_and_month[1]}"))

            choosen_month = int(
                datetime.strptime(f"{date['ano']}{date['mes']}", "%Y%B")
                .date()
                .strftime("%Y%m")
            )

            if self.is_defined_month_displayed_on_screen(choosen_month, months):
                self.web_driver.find_element(
                    By.CSS_SELECTOR,
                    f"div[aria-label*='{date['dia']} de {date['mes']} de {date['ano']}']",
                ).click()
                break

    def is_defined_month_displayed_on_screen(
        self, month: int, months_displayed_on_screen: List[int]
    ) -> bool:
        if is_month_earlier_than_the_first_one_shown_on_the_screen(
            month, months_displayed_on_screen[0]
        ):
            self.back_months_displayed_on_screen()
            return False
        elif is_month_later_than_the_second_one_shown_on_the_screen(
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
