from zoneinfo import ZoneInfo

from garden_app.domain.time import get_current_month, get_month_window
from garden_app.models.task import Task

APP_TIMEZONE = ZoneInfo("Europe/Amsterdam")

current = get_current_month()
prev, curr, next_ = get_month_window(current)


def filter_tasks_for_current_window(tasks: list[Task]) -> list[Task]:
    current_month = get_current_month()
    visible_months = get_month_window(current_month)

    return [task for task in tasks if task.recommended_month in visible_months]
