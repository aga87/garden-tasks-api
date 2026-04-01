MONTHS = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12,
}


def parse_recommended_month(text: str) -> int:
    lower_text = text.lower()

    month_name = next((name for name in MONTHS if name in lower_text), None)
    if month_name is None:
        raise ValueError(f"Could not find month name in: {text!r}")

    return MONTHS[month_name]


def parse_recommended_month_stage(text: str) -> str | None:
    lower_text = text.lower()

    if "early" in lower_text:
        return "early"

    if "late" in lower_text:
        return "late"

    return None


def parse_priority(value: str | None) -> str | None:
    if value is None:
        return None

    text = value.strip()
    if not text:
        return None

    lower = text.lower()

    if lower not in {"low", "medium", "high"}:
        raise ValueError(f"Invalid priority: {value!r}")

    return lower


def parse_optional_text(value: str | None) -> str | None:
    if value is None:
        return None

    text = value.strip()
    return text or None


def parse_area(value: str | None) -> str | None:
    return parse_optional_text(value)


def parse_task_type(value: str | None) -> str | None:
    return parse_optional_text(value)


def parse_notes(value: str | None) -> str | None:
    return parse_optional_text(value)
