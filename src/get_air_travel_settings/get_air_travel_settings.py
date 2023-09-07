from datetime import datetime, date
import locale

locale.setlocale(locale.LC_TIME, "pt_BR.utf8")


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


def validate_input_string(input: str):
    if input.replace(" ", "").isalpha() == False:
        raise ValueError("Por favor, insira um local válido!")
    return input


def format_input_date(date_object: str):
    return {
        "dia": str(date_object.day),
        "mes": str(date_object.strftime("%B")),
        "ano": str(date_object.year),
    }


def validate_input_date(input: str):
    try:
        date_convertted = datetime.strptime(input, "%d %m %Y").date()
    except:
        raise ValueError(
            "Insira uma data válida, da seguinte maneira: 01 01 2001 (dia, mes, ano)"
        )
    if isinstance(date_convertted, date) == False:
        raise ValueError("Por favor, insira uma data válida!")
    return format_input_date(date_convertted)
