URL = "http://maps.google.com/maps?q={lat},{lon}"


def location_url_gmaps(lat, lon):
    return URL.format(lat=lat, lon=lon)
