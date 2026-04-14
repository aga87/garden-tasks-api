import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class GardenSheetConfig:
    sheet_id: str
    sheet_range: str


@dataclass(frozen=True)
class Secrets:
    google_service_account_json: str


@dataclass(frozen=True)
class Env:
    config: GardenSheetConfig
    secrets: Secrets


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


ENV = Env(
    config=GardenSheetConfig(
        sheet_id=require_env("GARDEN_SHEET_ID"),
        sheet_range=require_env("GARDEN_SHEET_RANGE"),
    ),
    secrets=Secrets(
        google_service_account_json=require_env("GOOGLE_SERVICE_ACCOUNT_JSON"),
    ),
)
