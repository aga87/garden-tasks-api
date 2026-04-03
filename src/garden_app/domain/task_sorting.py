from garden_app.domain.time import (
    get_current_month,
    get_next_month,
    get_previous_month,
)
from garden_app.models.task import Task


def sort_tasks(tasks: list[Task]) -> list[Task]:
    current_month = get_current_month()
    previous_month = get_previous_month(current_month)
    next_month = get_next_month(current_month)

    month_order = {
        previous_month: 0,
        current_month: 1,
        next_month: 2,
    }

    done_order = {
        False: 0,
        True: 1,
    }

    stage_order = {
        "early": 0,
        None: 1,
        "late": 2,
    }

    priority_order = {
        "high": 0,
        "medium": 1,
        "low": 2,
    }

    return sorted(
        tasks,
        key=lambda t: (
            month_order.get(t.recommended_month, 99),
            done_order.get(t.done, 99),
            stage_order.get(t.recommended_month_stage, 99),
            priority_order.get(t.priority, 99) if t.priority is not None else 99,
        ),
    )
