import math

def maidenhead_latlon_to_locator(lat, lon):
    """
    Wandelt gegebene Koordinaten (Breite, Länge) in ein 6-stelliges Maidenhead Grid um.
    :param lat: Breitengrad (float), z. B. 48.137154
    :param lon: Längengrad (float), z. B. 11.576124
    :return: Maidenhead-Locator (z. B. 'JN58TD')
    """

    if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
        raise ValueError("Koordinaten außerhalb des gültigen Bereichs.")

    # Shift Koordinaten in positives System
    lat += 90.0
    lon += 180.0

    # 1. Field
    A = ord('A')
    field_lon = chr(A + int(lon // 20))
    field_lat = chr(A + int(lat // 10))

    # 2. Square
    square_lon = str(int((lon % 20) // 2))
    square_lat = str(int(lat % 10))

    # 3. Subsquare
    subsquare_lon = chr(A + int(((lon % 2) * 12)))
    subsquare_lat = chr(A + int(((lat % 1) * 24)))

    return field_lon + field_lat + square_lon + square_lat + subsquare_lon + subsquare_lat


def maidenhead_locator_to_latlon(locator):
    """
    Wandelt einen 6-stelligen Maidenhead-Locator in die Koordinaten des Zentrumspunkts um.
    :param locator: 6-stelliger Maidenhead-Locator (z. B. 'JN58TD')
    :return: (latitude, longitude) in Dezimalgrad
    """
    if len(locator) != 6:
        raise ValueError("Locator muss genau 6 Zeichen lang sein.")

    locator = locator.upper()

    # Field (1. und 2. Zeichen)
    lon_field = (ord(locator[0]) - ord('A')) * 20.0
    lat_field = (ord(locator[1]) - ord('A')) * 10.0

    # Square (3. und 4. Zeichen)
    lon_square = int(locator[2]) * 2.0
    lat_square = int(locator[3]) * 1.0

    # Subsquare (5. und 6. Zeichen)
    lon_sub = (ord(locator[4]) - ord('A')) * (2.0 / 24.0)
    lat_sub = (ord(locator[5]) - ord('A')) * (1.0 / 24.0)

    # Gesamtposition des linken unteren Eckpunkts
    lon = lon_field + lon_square + lon_sub - 180.0
    lat = lat_field + lat_square + lat_sub - 90.0

    # Mittelpunkt des Subsquare hinzufügen
    lon += (2.0 / 24.0) / 2.0  # 5 Minuten → halbe Länge
    lat += (1.0 / 24.0) / 2.0  # 2.5 Minuten → halbe Breite

    return lat, lon

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Berechnet die Luftlinien-Entfernung zwischen zwei Punkten auf der Erde
    anhand der Haversine-Formel.
    
    :param lat1: Breitengrad Punkt 1 (in Dezimalgrad)
    :param lon1: Längengrad Punkt 1 (in Dezimalgrad)
    :param lat2: Breitengrad Punkt 2 (in Dezimalgrad)
    :param lon2: Längengrad Punkt 2 (in Dezimalgrad)
    :return: Entfernung in Kilometern (float)
    """

    # Erdradius (mittlerer Radius in km)
    R = 6371.0

    # Koordinaten in Bogenmaß umrechnen
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    # Haversine-Formel
    a = math.sin(delta_phi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Entfernung berechnen
    distance = R * c

    return distance
