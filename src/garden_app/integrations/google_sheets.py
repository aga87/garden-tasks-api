import os

import requests

BASE_URL = "https://sheets.googleapis.com/v4/spreadsheets"


def fetch_sheet_values() -> list[list[str]]:
    sheet_id = os.environ["GARDEN_SHEET_ID"]
    sheet_range = os.environ["GARDEN_SHEET_RANGE"]
    api_key = os.environ["GOOGLE_SHEETS_API_KEY"]

    url = f"{BASE_URL}/{sheet_id}/values/{sheet_range}"

    response = requests.get(
        url,
        params={"key": api_key},
        timeout=10,
    )
    response.raise_for_status()

    data = response.json()
    values = data.get("values", [])

    if not isinstance(values, list):
        raise ValueError("Invalid response format: 'values' is not a list")

    return values
