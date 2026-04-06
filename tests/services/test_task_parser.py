import pytest

from garden_app.domain.types import Status
from garden_app.services.task_parser import (
    parse_area,
    parse_notes,
    parse_optional_text,
    parse_priority,
    parse_recommended_month,
    parse_recommended_month_stage,
    parse_status,
    parse_task_row,
    parse_task_type,
    parse_title,
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
        ("urgent", None),
        (None, None),
    ],
)
def test_parse_priority(value: str | None, expected: str | None) -> None:
    assert parse_priority(value) == expected


# Full test coverage for shared helper
@pytest.mark.parametrize(
    "value,expected",
    [
        ("Canal", "Canal"),
        (" Everywhere ", "Everywhere"),
        ("Some note", "Some note"),
        ("", None),
        ("   ", None),
        (None, None),
    ],
)
def test_parse_optional_text(value: str | None, expected: str | None) -> None:
    assert parse_optional_text(value) == expected


# One simple test per wrapper
def test_parse_area_uses_optional_text_parser() -> None:
    assert parse_area(" Canal ") == "Canal"


def test_parse_task_type_uses_optional_text_parser() -> None:
    assert parse_task_type(" Maintenance ") == "Maintenance"


def test_parse_notes_uses_optional_text_parser() -> None:
    assert parse_notes(" Some note ") == "Some note"


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("todo", Status.todo),
        ("doing", Status.doing),
        ("done", Status.done),
        ("won't do", Status.skip),
    ],
)
def test_parse_status(value: str, expected: Status) -> None:
    assert parse_status(value) == expected


@pytest.mark.parametrize("value", ["", None, "invalid", "false"])
def test_parse_status_raises_for_unknown_value(value: str) -> None:
    with pytest.raises(ValueError):
        parse_status(value)


@pytest.mark.parametrize(
    "value,expected",
    [
        ("Remove brambles", "Remove brambles"),
        (" Prune willows ", "Prune willows"),
    ],
)
def test_parse_title(value: str, expected: str) -> None:
    assert parse_title(value) == expected


@pytest.mark.parametrize(
    "value",
    [
        "",
        "   ",
        None,
    ],
)
def test_parse_title_invalid(value: str | None) -> None:
    with pytest.raises(ValueError):
        parse_title(value)


# TASK ROW
def test_parse_task_row_valid() -> None:
    row = {
        "Task": "Remove brambles",
        "Recommended time": "01.1 Early January",
        "Priority": "High",
        "Area": "Canal",
        "Type of task": "Maintenance",
        "Notes": "Some note",
        "Status": "todo",
    }

    result = parse_task_row(row)

    assert result is not None
    assert result.title == "Remove brambles"
    assert result.recommended_month == 1
    assert result.recommended_month_stage == "early"
    assert result.priority == "high"
    assert result.area == "Canal"
    assert result.task_type == "Maintenance"
    assert result.notes == "Some note"
    assert result.status == Status.todo


def test_parse_task_row_minimal_valid() -> None:
    row = {
        "Task": "Prune willows",
        "Recommended time": "05. May",
        "Status": "todo",
    }

    result = parse_task_row(row)

    assert result is not None
    assert result.title == "Prune willows"
    assert result.recommended_month == 5
    assert result.recommended_month_stage is None
    assert result.priority is None
    assert result.area is None
    assert result.task_type is None
    assert result.notes is None
    assert result.status == Status.todo


def test_parse_task_row_missing_recommended_time_empty() -> None:
    row = {
        "Task": "Remove brambles",
        "Recommended time": "",
    }

    assert parse_task_row(row) is None


def test_parse_task_row_missing_recommended_time_none() -> None:
    row = {
        "Task": "Remove brambles",
        "Recommended time": None,
    }

    assert parse_task_row(row) is None


def test_parse_task_row_missing_title_empty() -> None:
    row = {
        "Task": "",
        "Recommended time": "01. January",
    }

    assert parse_task_row(row) is None


def test_parse_task_row_missing_title_none() -> None:
    row = {
        "Task": None,
        "Recommended time": "01. January",
    }

    assert parse_task_row(row) is None


def test_parse_task_row_invalid_month() -> None:
    row = {
        "Task": "Remove brambles",
        "Recommended time": "Not a real month",
    }

    assert parse_task_row(row) is None


def test_parse_task_row_optional_fields_invalid() -> None:
    row = {
        "Task": "Remove brambles",
        "Recommended time": "01. January",
        "Status": "done",
        "Priority": "urgent",  # invalid → None
        "Area": "",
        "Type of task": None,
        "Notes": "   ",
    }

    result = parse_task_row(row)

    assert result is not None
    assert result.priority is None
    assert result.area is None
    assert result.task_type is None
    assert result.notes is None
