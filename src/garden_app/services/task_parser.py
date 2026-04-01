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
