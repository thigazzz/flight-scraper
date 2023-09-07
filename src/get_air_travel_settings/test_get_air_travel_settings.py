from datetime import datetime, date
import pytest


def validate_input_string(input: str):
    if input.replace(" ", "").isalpha() == False:
        raise ValueError("Por favor, insira um local válido!")
    return input


def format_input_date(input: str):
    return input.replace(" ", "/")


def validate_input_date(input: str):
    try:
        date_convertted = datetime.strptime(input, "%d %m %Y").date()
    except:
        raise ValueError(
            "Insira uma data válida, da seguinte maneira: 01 01 2001 (dia, mes, ano)"
        )
    if isinstance(date_convertted, date) == False:
        raise ValueError("Por favor, insira uma data válida!")
    return format_input_date(input)


def get_air_travel_settings():
    while True:
        try:
            destination_from_where = validate_input_string(
                input("Insira o local de onde voce vai sair: ")
            )
            destination_from_to = validate_input_string(
                input("Insira o local para onde voce vai")
            )
            departure_date = validate_input_date(input("Insira a data de ida desejada"))
            return_date = validate_input_date(input("Insira a data de volta desejada"))

            return [
                destination_from_where,
                destination_from_to,
                departure_date,
                return_date,
            ]
        except ValueError as error:
            print(error)


def test_get_settings_from_user_input(monkeypatch):
    mock_inputs = iter(["São Paulo", "Rio de Janeiro", "07 08 2023", "14 08 2023"])
    monkeypatch.setattr("builtins.input", lambda _: next(mock_inputs))

    from_where, to_where, departure_date, return_date = get_air_travel_settings()

    assert from_where == "São Paulo"
    assert to_where == "Rio de Janeiro"
    assert departure_date == "07/08/2023"
    assert return_date == "14/08/2023"


def test_validate_if_input_date_is_in_correct_format():
    validaded_input_date = validate_input_date("10 10 2023")

    assert validaded_input_date == "10/10/2023"


@pytest.mark.skip(reason="Não tenho conhecimento ainda para fazer tal teste")
def test_input_validation(monkeypatch, capsys):
    mock_inputs = iter(["1", "Rio de Janeiro", "07 08 2023", "14 08 2023"])
    monkeypatch.setattr("builtins.input", lambda _: next(mock_inputs))

    from_where_validation_error_printed = capsys.readouterr()

    assert (
        from_where_validation_error_printed.out == "Por favor, insira um local válido!"
    )
