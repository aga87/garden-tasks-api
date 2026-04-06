from datetime import datetime
from zoneinfo import ZoneInfo

APP_TIMEZONE = ZoneInfo("Europe/Amsterdam")


def get_current_month(timezone: ZoneInfo = APP_TIMEZONE) -> int:
    return datetime.now(timezone).month


def get_previous_month(month: int) -> int:
    return 12 if month == 1 else month - 1


def get_next_month(month: int) -> int:
    return 1 if month == 12 else month + 1
