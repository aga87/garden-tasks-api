import garden_app.integrations.google_drive as gdrive
from garden_app.integrations.google_drive import NamedJSONs


def fetch_map_geojson_layers() -> NamedJSONs:
    service = gdrive.authenticate_google_drive()
    entries = gdrive.fetch_entries(service, extension="geojson")
    geojsons = gdrive.get_json_contents(service, entries)

    return geojsons
