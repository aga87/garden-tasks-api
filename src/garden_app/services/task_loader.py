import logging

from garden_app.integrations.google_sheets import fetch_sheet_values
from garden_app.models.task import Task
from garden_app.services.task_parser import parse_task_row

logger = logging.getLogger(__name__)


def map_sheet_rows(rows: list[list[str]]) -> list[dict[str, str | None]]:
    if not rows:
        return []

    header = rows[2]
    data_rows = rows[3:]

    mapped_rows: list[dict[str, str | None]] = []

    for row in data_rows:
        row_dict = {
            column_name: row[index] if index < len(row) else None
            for index, column_name in enumerate(header)
        }
        mapped_rows.append(row_dict)

    return mapped_rows


def load_tasks_from_sheet() -> list[Task]:
    rows = fetch_sheet_values()
    logger.info("Fetched %d rows from Google Sheet", len(rows))

    row_dicts = map_sheet_rows(rows)

    tasks: list[Task] = []
    skipped = 0

    for row_dict in row_dicts:
        task = parse_task_row(row_dict)

        if task is not None:
            tasks.append(task)
        else:
            skipped += 1

    logger.info(
        "Parsed %d tasks (skipped %d rows)",
        len(tasks),
        skipped,
    )

    return tasks
