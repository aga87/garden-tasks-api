from zoneinfo import ZoneInfo

from garden_app.domain.time import get_current_month, get_next_month
from garden_app.domain.types import Location, Status
from garden_app.models.task import Task

APP_TIMEZONE = ZoneInfo("Europe/Amsterdam")

current = get_current_month()


HOME_TASK_TYPES = {"organization", "sowing at home"}


def filter_tasks_by_location(
    tasks: list[Task],
    location: Location | None,
) -> list[Task]:
    if location is None:
        return tasks

    def matches(task: Task) -> bool:
        if task.task_type is None:
            return True  # appears in both

        task_type = task.task_type.strip().lower()

        is_home = task_type in HOME_TASK_TYPES

        if location == Location.home:
            return is_home

        if location == Location.garden:
            return not is_home

        return True

    return [task for task in tasks if matches(task)]


def filter_tasks_by_status(tasks: list[Task]) -> list[Task]:
    return [task for task in tasks if task.status in {Status.todo, Status.doing}]


def filter_tasks_by_visible_months(tasks: list[Task]) -> list[Task]:
    current_month = get_current_month()
    next_month = get_next_month(current_month)

    return [
        task
        for task in tasks
        if (
            # include all past months from January up to current month,
            # plus the current month and the next month
            1 <= task.recommended_month <= current_month
            or task.recommended_month == next_month
        )
    ]
