import os
from typing import Dict
from openpyxl import load_workbook, Workbook
import pytest
from faker import Faker

fake = Faker()


class ExcelRobot:
    excel_file_path = os.path.abspath("data/air-travels.xlsx")

    def __init__(self) -> None:
        self.create_blank_excel_file()
        self.excel = self.get_excel()

    def create_blank_excel_file(self):
        if self.is_file_excel_exists() == False:
            Workbook().save(self.excel_file_path)

    def is_file_excel_exists(self) -> bool:
        return os.path.isfile(self.excel_file_path)

    def get_excel(self):
        return load_workbook(self.excel_file_path)

    def get_actual_sheet(self):
        return self.excel.active

    def insert_informations_in_excel(self, informations: Dict):
        index = 0
        for row in self.iterate_rows_of_length_informations(informations):
            self.insert_in_cell(row[0], informations[index]["price"])
            self.insert_in_cell(row[1], informations[index]["departure time"])
            self.insert_in_cell(row[2], informations[index]["disembarkation time"])
            index += 1

    def iterate_rows_of_length_informations(self, data):
        sheet = self.get_actual_sheet()
        return sheet.iter_rows(
            min_row=2, min_col=1, max_row=len(data) + 1, max_col=len(data[0])
        )

    def insert_in_cell(self, row, data):
        row.value = data

    def save_excel(self):
        self.excel.save(self.excel_file_path)


@pytest.fixture
def excel_open_and_delete():
    ExcelRobot()
    yield
    os.remove(os.path.abspath("data/air-travels.xlsx"))


def make_mock_extracted_informations():
    mock_extracted_informations = []
    for _ in list(range(5)):
        mock_extracted_informations.append(
            {
                "price": fake.pricetag(),
                "departure time": fake.date(),
                "disembarkation time": fake.date(),
            },
        )
    return mock_extracted_informations


@pytest.mark.excel_process
def test_insert_extracted_informations_in_excel_file(excel_open_and_delete):
    mock_extracted_informations = make_mock_extracted_informations()

    excel_robot = ExcelRobot()
    excel_robot.insert_informations_in_excel(mock_extracted_informations)
    excel_robot.save_excel()

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
