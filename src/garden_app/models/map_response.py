from typing import Any

from pydantic import BaseModel


class MapResponse(BaseModel):
    geojsons: dict[str, Any] | None
