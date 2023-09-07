import pytest
from get_air_travel_settings import get_air_travel_settings, validate_input_date


@pytest.mark.input_user
def test_get_settings_from_user_input(monkeypatch):
    mock_inputs = iter(["São Paulo", "Rio de Janeiro", "07 08 2023", "14 08 2023"])
    monkeypatch.setattr("builtins.input", lambda _: next(mock_inputs))

    from_where, to_where, departure_date, return_date = get_air_travel_settings()

    assert from_where == "São Paulo"
    assert to_where == "Rio de Janeiro"
    assert departure_date == {"dia": "7", "mes": "agosto", "ano": "2023"}
    print(departure_date)
    assert return_date == {"dia": "14", "mes": "agosto", "ano": "2023"}


@pytest.mark.input_user
def test_validate_if_input_date_is_in_correct_format():
    validaded_input_date = validate_input_date("7 08 2023")

    assert validaded_input_date == {"dia": "7", "mes": "agosto", "ano": "2023"}


@pytest.mark.skip(reason="Não tenho conhecimento ainda para fazer tal teste")
def test_input_validation(monkeypatch, capsys):
    mock_inputs = iter(["1", "Rio de Janeiro", "07 08 2023", "14 08 2023"])
    monkeypatch.setattr("builtins.input", lambda _: next(mock_inputs))

    from_where_validation_error_printed = capsys.readouterr()

    assert (
        from_where_validation_error_printed.out == "Por favor, insira um local válido!"
    )
