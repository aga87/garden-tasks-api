from pydantic import BaseModel

from garden_app.domain.types import NamedJSONs


class MapResponse(BaseModel):
    geojsons: NamedJSONs
