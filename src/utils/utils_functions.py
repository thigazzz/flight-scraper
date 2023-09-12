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
