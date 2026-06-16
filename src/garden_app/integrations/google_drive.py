"""Interact with Google Drive files through Google Drive API."""

import io
import json
from pathlib import Path
from typing import Any, cast

import google.auth
from googleapiclient.discovery import Resource, build  # type: ignore[import-untyped]
from googleapiclient.http import MediaIoBaseDownload  # type: ignore[import-untyped]

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]


def authenticate_google_drive() -> Resource:
    """Authenticate into Google Drive.

    :return: object for interacting with Google Drive
    """
    credentials, _ = google.auth.default(scopes=SCOPES)
    service = build("drive", "v3", credentials=credentials)

    return service


def fetch_entries(
    service: Resource, extension: str = "json"
) -> list[dict[str, str]] | None:
    """Fetch metadata of files with specific extension from Google Drive using its API.

    Can read all the files that are available to the account.

    :return: ID and name pairs of entries (files)
    """
    results = (
        service.files()
        .list(fields="files(id,name)", q=f"fileExtension = '{extension}'")
        .execute()
    )

    entries = cast(list[dict[str, str]], results.get("files", []))

    if not entries:
        return None

    return entries


def get_json_contents(
    service: Resource, entries: list[dict[str, str]] | None
) -> dict[str, Any] | None:
    """Get contents of JSON files stored on Google Drive.

    Works also for GeoJSONs.

    :return: dictionary of json_name: json
    """
    jsons = {}

    if entries is None:
        return None

    for entry in entries:
        request = service.files().get_media(fileId=entry["id"])
        memory_buffer = io.BytesIO()
        downloader = MediaIoBaseDownload(memory_buffer, request)

        done = False
        while not done:
            _, done = downloader.next_chunk()

        json_text = memory_buffer.getvalue().decode("utf-8")
        json_content = json.loads(json_text)
        key = Path(entry["name"]).stem

        jsons[key] = json_content

    return jsons
