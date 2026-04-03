import requests

from garden_app.config.env import ENV

BASE_URL = "https://sheets.googleapis.com/v4/spreadsheets"


def fetch_sheet_values() -> list[list[str]]:
    sheet_id = ENV.config.sheet_id
    sheet_range = ENV.config.sheet_range
    api_key = ENV.secrets.google_sheets_api_key

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
