import os
import pytest
from typing import Dict
from openpyxl import load_workbook, Workbook
import time


class ExcelRobot:
    def __init__(self) -> None:
        self.open_excel_blank_file()

    def open_excel_blank_file(self):
        if os.path.isfile(os.path.abspath("data/air-travels.xlsx")) == False:
            worksheet = Workbook()
            worksheet.save(os.path.abspath("data/air-travels.xlsx"))

    def insert_informations_in_excel(self, informations: Dict):
        excel_file = load_workbook(os.path.abspath("data/air-travels.xlsx"))
        sheet = excel_file.active
        index = 0
        for row in sheet.iter_rows(min_row=2, min_col=1, max_row=6, max_col=3):
            row[0].value = informations[index]["price"]
            row[1].value = informations[index]["departure time"]
            row[2].value = informations[index]["disembarkation time"]
            index += 1
        excel_file.save("data/air-travels.xlsx")


@pytest.fixture
def excel_open_and_delete():
    ExcelRobot()
    yield
    os.remove(os.path.abspath("data/air-travels.xlsx"))


@pytest.mark.excel_process
def test_insert_extracted_informations_in_excel_file(excel_open_and_delete):
    mock_extracted_informations = [
        {
            "price": "R$ 100,00",
            "departure time": "07/10/2023",
            "disembarkation time": "14/10/2023",
        },
        {
            "price": "R$ 150,00",
            "departure time": "07/10/2023",
            "disembarkation time": "14/10/2023",
        },
        {
            "price": "R$ 100,00",
            "departure time": "07/10/2023",
            "disembarkation time": "14/10/2023",
        },
        {
            "price": "R$ 200,00",
            "departure time": "07/10/2023",
            "disembarkation time": "14/10/2023",
        },
        {
            "price": "R$ 1200,00",
            "departure time": "07/10/2023",
            "disembarkation time": "14/10/2023",
        },
    ]

    excel_robot = ExcelRobot()
    excel_robot.insert_informations_in_excel(mock_extracted_informations)
    excel_file = load_workbook(os.path.abspath("data/air-travels.xlsx"))
    sheet = excel_file.active

    index = 0
    for row in sheet.iter_rows(min_row=2, min_col=1, max_row=6, max_col=3):
        assert row[0].value == mock_extracted_informations[index]["price"]
        assert row[1].value == mock_extracted_informations[index]["departure time"]
        assert row[2].value == mock_extracted_informations[index]["disembarkation time"]
        index += 1


@pytest.mark.excel_process
def test_create_blank_excel_file(excel_open_and_delete):
    mock_excel_file_path = os.path.abspath("data/air-travels.xlsx")
    assert os.path.isfile(mock_excel_file_path) == True


@pytest.mark.excel_process
def test_not_create_new_excel_file_if_exists_one():
    ExcelRobot()
    mock_excel_file_path = os.path.abspath("data/air-travels.xlsx")
    excel_date_creation = os.stat(mock_excel_file_path)
    ExcelRobot()
    assert excel_date_creation.st_mtime == os.stat(mock_excel_file_path).st_mtime
    os.remove(os.path.abspath("data/air-travels.xlsx"))
