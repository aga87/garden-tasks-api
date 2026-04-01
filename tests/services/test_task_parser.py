import pytest

from garden_app.services.task_parser import (
    parse_area,
    parse_priority,
    parse_recommended_month,
    parse_recommended_month_stage,
)


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


@pytest.mark.parametrize(
    "value,expected",
    [
        ("01.1 Early January", "early"),
        ("01.2 Late January", "late"),
        ("03.1 Early March", "early"),
        ("03.2 Late March", "late"),
        ("01. January", None),
        ("05. May", None),
        ("09.2 September", None),
        ("", None),
        ("Not a real month", None),
    ],
)
def test_parse_recommended_month_stage(value: str, expected: str | None) -> None:
    assert parse_recommended_month_stage(value) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        ("Low", "low"),
        ("Medium", "medium"),
        ("High", "high"),
        ("low", "low"),
        (" medium ", "medium"),
        ("", None),
        (None, None),
    ],
)
def test_parse_priority(value: str | None, expected: str | None) -> None:
    assert parse_priority(value) == expected


@pytest.mark.parametrize(
    "value",
    [
        "Urgent",
        "Very High",
    ],
)
def test_parse_priority_invalid(value: str) -> None:
    with pytest.raises(ValueError):
        parse_priority(value)


@pytest.mark.parametrize(
    "value,expected",
    [
        ("Canal", "Canal"),
        (" Everywhere ", "Everywhere"),
        ("", None),
        ("   ", None),
        (None, None),
    ],
)
def test_parse_area(value: str | None, expected: str | None) -> None:
    assert parse_area(value) == expected
