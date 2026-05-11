from typing import Any

import google.auth
from googleapiclient.discovery import build  # type: ignore[import-untyped]

from garden_app.config.env import ENV

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


def fetch_sheet_values() -> list[list[str]]:
    sheet_id = ENV.config.sheet_id
    sheet_range = ENV.config.sheet_range

    credentials, _ = google.auth.default(scopes=SCOPES)

    service = build("sheets", "v4", credentials=credentials)

    result: dict[str, Any] = (
        service.spreadsheets()
        .values()
        .get(
            spreadsheetId=sheet_id,
            range=sheet_range,
        )
        .execute()
    )

    values = result.get("values", [])

    if not isinstance(values, list):
        raise ValueError("Invalid response format: 'values' is not a list")

    return values
