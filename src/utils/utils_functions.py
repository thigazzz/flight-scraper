def is_chosen_month_is_previous_first_shown_on_screen(
    choosen_month: int, first_month_on_screen: int
) -> bool:
    if choosen_month < first_month_on_screen:
        return True
    return False


def is_month_chosen_is_posteior_to_second_shown_on_screen(
    choosen_month: int, second_month_on_screen: int
) -> bool:
    if choosen_month > second_month_on_screen:
        return True
    return False
