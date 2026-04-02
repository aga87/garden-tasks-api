import logging

from garden_app.domain_types import Priority, RecommendedMonthStage
from garden_app.models.task import Task

logger = logging.getLogger(__name__)

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


def parse_recommended_month_stage(text: str) -> RecommendedMonthStage | None:
    lower_text = text.lower()

    if "early" in lower_text:
        return "early"

    if "late" in lower_text:
        return "late"

    return None


def parse_priority(value: str | None) -> Priority | None:
    if value is None:
        return None

    text = value.strip()
    if not text:
        return None

    lower = text.lower()

    if lower == "low":
        return "low"
    if lower == "medium":
        return "medium"
    if lower == "high":
        return "high"

    return None


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


def parse_done(value: str | None) -> bool:
    if value is None:
        return False

    text = value.strip().lower()

    return text in {"true", "1", "yes"}


def parse_title(value: str | None) -> str:
    if value is None:
        raise ValueError("Task title is missing")

    text = value.strip()
    if not text:
        raise ValueError("Task title is empty")

    return text


def parse_task_row(row: dict[str, str | None]) -> Task | None:
    try:
        title = parse_title(row.get("Task"))

        recommended_time = row.get("Recommended time")
        if not recommended_time or not recommended_time.strip():
            logger.warning("Skipping row: missing recommended time | row=%s", row)
            return None

        return Task(
            title=title,
            recommended_month=parse_recommended_month(recommended_time),
            recommended_month_stage=parse_recommended_month_stage(recommended_time),
            priority=parse_priority(row.get("Priority")),
            area=parse_area(row.get("Area")),
            task_type=parse_task_type(row.get("Type of task")),
            notes=parse_notes(row.get("Notes")),
            done=parse_done(row.get("Done")),
        )

    except ValueError as e:
        logger.warning("Skipping row due to parsing error: %s | row=%s", e, row)
        return None
