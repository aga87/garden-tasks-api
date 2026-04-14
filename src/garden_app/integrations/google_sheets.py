import json
from typing import Any

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build  # type: ignore[import-untyped]

from garden_app.config.env import ENV

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


def fetch_sheet_values() -> list[list[str]]:
    sheet_id = ENV.config.sheet_id
    sheet_range = ENV.config.sheet_range

    service_account_info = json.loads(ENV.secrets.google_service_account_json)
    if not isinstance(service_account_info, dict):
        raise ValueError("Invalid service account JSON format: expected a JSON object")

    credentials = Credentials.from_service_account_info(  # type: ignore[no-untyped-call]
        service_account_info,
        scopes=SCOPES,
    )

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
