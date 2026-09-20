# utils/constants.py

# -------------------------------------------------
# GOA TOWNS (sources of buses)
# -------------------------------------------------

GOA_TOWNS = [
    "Panaji",
    "Margao",
    "Vasco da Gama",
    "Mapusa",
    "Ponda",
    "Bicholim",
    "Curchorem",
    "Canacona",
    "Calangute",
    "Valpoi",
    "Pernem",
    "Quepem",
    "Sanquelim",
    "Sanguem",
    "Mormugao",
    "Cortalim",
    "Cuncolim",
    "Fatorda",
    "Colva",
    "Arambol"
]


# -------------------------------------------------
# OUTSTATION DESTINATIONS
# -------------------------------------------------

OUTSTATION_CITIES = [
    "Mumbai",
    "Pune",
    "Bangalore",
    "Hyderabad",
    "Chennai",
    "Mangalore",
    "Hubli",
    "Belgaum",
    "Kolhapur",
    "Nashik",
    "Aurangabad",
    "Solapur",
    "Mysore",
    "Udupi",
    "Dharwad"
]


ALL_DESTINATIONS = GOA_TOWNS + OUTSTATION_CITIES


# -------------------------------------------------
# BUS OPERATORS
# -------------------------------------------------

BUS_OPERATORS = [
    "Kadamba",
    "Konkan",
    "Deccan",
    "Coastal",
    "Sahyadri",
    "Mandovi",
    "Zuari",
    "Gomantak",
    "Salcete",
    "Bardez"
]


BUS_SUFFIXES = [
    "Express",
    "Cruiser",
    "Deluxe",
    "Travels",
    "Liner",
    "Shuttle",
    "Runner",
    "Swift",
    "Link",
    "Star"
]


# -------------------------------------------------
# DESTINATION CATEGORIES
# -------------------------------------------------

LONG_HAUL = {
    "Mumbai",
    "Pune",
    "Bangalore",
    "Hyderabad",
    "Chennai",
    "Nashik",
    "Aurangabad",
    "Solapur"
}


MEDIUM_HAUL = {
    "Mangalore",
    "Hubli",
    "Belgaum",
    "Kolhapur",
    "Mysore",
    "Udupi",
    "Dharwad"
}


# -------------------------------------------------
# FARE RANGES
# -------------------------------------------------

FARE_LOCAL = (30, 90)

FARE_MEDIUM = (350, 700)

FARE_LONG = (650, 1400)


# -------------------------------------------------
# BUS TYPES
# -------------------------------------------------

BUS_TYPES = [
    "Seater",
    "Sleeper"
]


# Sleeper fare multiplier
SLEEPER_MULTIPLIER = 1.6


# -------------------------------------------------
# SEAT TYPES
# -------------------------------------------------

SEAT_PATTERN = [
    "window",
    "aisle",
    "window",
    "aisle"
]