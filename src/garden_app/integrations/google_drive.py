#!/usr/bin/env python3
"""Interact with Google Drive files through Google Drive API."""
from pathlib import Path
import io
import json

import google.auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

def authenticate_google_drive():
    """Authenticate into Google Drive.
    
    :return: object for interacting with Google Drive
    """
    credentials, _ = google.auth.default(scopes=SCOPES)
    service = build("drive", "v3", credentials=credentials)
    
    return service

def fetch_entries(service, extension="json") -> list[dict[str, str]] | None:
    """Fetch metadata of files with specific extension from Google Drive using its API.
    
    Can read all the files that are available to the account.
    
    :return: ID and name pairs of entries (files)
    """
    results = (
        service.files()
        .list(fields="files(id,name)",
              q=f"fileExtension = '{extension}'")
        .execute()
    )
    
    entries = results.get("files", [])
    
    if not entries:
        print("No files found.")
        return
    
    # List available Google Drive files.
    # print("Files:")
    # for item in items:
    #     print(item)
    
    return entries

def get_json_contents(service, entries):
    """Get contents of JSON files stored on Google Drive.
    
    Works also for GeoJSONs.
        
    :return: dictionary of json_name: json
    """
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
    
    return jsons
