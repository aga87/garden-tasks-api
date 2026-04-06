from garden_app.domain.types import Status
from garden_app.models.task import Task


def sort_tasks(tasks: list[Task]) -> list[Task]:
    status_order = {
        Status.doing: 0,
        Status.todo: 1,
        Status.done: 2,
        Status.skip: 3,
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
            t.recommended_month,  # natural chronological order
            status_order.get(t.status, 99),
            stage_order.get(t.recommended_month_stage, 99),
            priority_order.get(t.priority, 99) if t.priority is not None else 99,
        ),
    )
