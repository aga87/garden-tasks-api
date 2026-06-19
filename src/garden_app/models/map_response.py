from pydantic import BaseModel

from garden_app.integrations.google_drive import NamedJSONs


class MapResponse(BaseModel):
    geojsons: NamedJSONs
