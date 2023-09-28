from get_air_travel_settings import get_air_travel_settings
from extract_flight_informations import WebRobot, Robot
from save_informations_in_excel import ExcelRobot
from selenium import webdriver
import time

air_travel_settings = get_air_travel_settings()
driver = webdriver.Edge()
driver.implicitly_wait(10)
driver.maximize_window()
web_robot = WebRobot(driver)
web_robot.access_skyscanner_site()
web_robot.insert_air_travel_settings(air_travel_settings)
web_robot.click_element('button[aria-label="Buscar"]')
informations = web_robot.extract_air_travels_informations()
excel_robot = ExcelRobot()
excel_robot.insert_informations_in_excel(informations)
excel_robot.save_excel()
