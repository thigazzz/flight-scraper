from typing import List
from datetime import datetime, timedelta


def is_month_earlier_than_the_first_one_shown_on_the_screen(
    month: int, first_month_on_screen: int
) -> bool:
    if month < first_month_on_screen:
        return True
    return False


def is_month_later_than_the_second_one_shown_on_the_screen(
    choosen_month: int, second_month_on_screen: int
) -> bool:
    if choosen_month > second_month_on_screen:
        return True
    return False


def join_year_and_month_in_string(date: List):
    return f"{date[0]}{date[1]}"


def convert_date_in_a_number(date: List):
    return int(join_year_and_month_in_string(date))


def get_today_date() -> str:
    return datetime.today()


def get_date_after_a_week_from_today() -> str:
    return datetime.now() + timedelta(days=7)


def format_date(date: datetime, formatter) -> str:
    return date.strftime(formatter)
