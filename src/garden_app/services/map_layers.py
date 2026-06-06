import garden_app.integrations.google_drive as gdrive

def fetch_map_geojson_layers():
    service = gdrive.authenticate_google_drive()
    entries = gdrive.fetch_entries(service, extension="geojson")
    geojsons = gdrive.get_json_contents(service, entries)
    
    return geojsons
