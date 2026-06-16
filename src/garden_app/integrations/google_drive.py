"""Interact with Google Drive files through Google Drive API."""

import io
import json
from pathlib import Path
from typing import Any, TypedDict, cast

import google.auth
from googleapiclient.discovery import Resource, build  # type: ignore[import-untyped]
from googleapiclient.http import MediaIoBaseDownload  # type: ignore[import-untyped]

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]


class DriveFile(TypedDict):
    id: str
    name: str

class NamedJSONs(TypedDict):
    json_name: str
    json: Any


def authenticate_google_drive() -> Resource:
    """Authenticate into Google Drive.

    :return: object for interacting with Google Drive
    """
    credentials, _ = google.auth.default(scopes=SCOPES)
    service = build("drive", "v3", credentials=credentials)

    return service


def fetch_entries(
    service: Resource, extension: str = "json"
) -> list[DriveFile]:
    """Fetch metadata of Google Drive files with the given extension."""
    results = (
        service.files()
        .list(fields="files(id,name)", q=f"fileExtension = '{extension}'")
        .execute()
    )

    return cast(list[DriveFile], results.get("files", []))


def get_json_contents(
    service: Resource, entries: list[DriveFile]
) -> NamedJSONs:
    """Get contents of JSON files stored on Google Drive."""
    jsons = {}

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

    return cast(NamedJSONs, jsons)
