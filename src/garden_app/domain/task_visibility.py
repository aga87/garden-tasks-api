from datetime import datetime
from zoneinfo import ZoneInfo

from garden_app.models.task import Task

APP_TIMEZONE = ZoneInfo("Europe/Amsterdam")


def get_current_month(timezone: ZoneInfo = APP_TIMEZONE) -> int:
    return datetime.now(timezone).month


def get_month_window(current_month: int) -> set[int]:
    previous_month = 12 if current_month == 1 else current_month - 1
    next_month = 1 if current_month == 12 else current_month + 1
    return {previous_month, current_month, next_month}


def filter_tasks_for_current_window(tasks: list[Task]) -> list[Task]:
    current_month = get_current_month()
    visible_months = get_month_window(current_month)

    return [task for task in tasks if task.recommended_month in visible_months]
