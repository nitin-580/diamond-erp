import math

FACTORY_LAT = 12.9716
FACTORY_LNG = 77.5946
RADIUS = 100  # meters


def is_inside_geofence(lat, lng):
    R = 6371000

    phi1 = math.radians(lat)
    phi2 = math.radians(FACTORY_LAT)

    dphi = math.radians(FACTORY_LAT - lat)
    dlambda = math.radians(FACTORY_LNG - lng)

    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    distance = R * c

    return distance <= RADIUS