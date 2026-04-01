import pytest

from garden_app.services.task_parser import parse_recommended_month


@pytest.mark.parametrize(
    "value,expected",
    [
        ("01. January", 1),
        ("01.1 Early January", 1),
        ("01.2 Late January", 1),
        ("1.1 Early January", 1),
        ("05. May", 5),
        ("05. Early May", 5),
        ("09.2 Late September", 9),
    ],
)
def test_parse_recommended_month(value: str, expected: int) -> None:
    assert parse_recommended_month(value) == expected


@pytest.mark.parametrize(
    "value",
    [
        "",
        "Not a real month",
        "13. Something",
    ],
)
def test_parse_recommended_month_invalid(value: str) -> None:
    with pytest.raises(ValueError):
        parse_recommended_month(value)
