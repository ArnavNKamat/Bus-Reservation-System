# utils/constants.py

# -------------------------------------------------
# GOA TOWNS & VILLAGES (North & South Goa Coverage)
# -------------------------------------------------

GOA_TOWNS = [
    # North Goa Major Hubs
    "Panaji",
    "Mapusa",
    "Porvorim",
    "Ponda",
    "Bicholim",
    "Sanquelim",
    "Valpoi",
    "Pernem",

    # North Goa Coastal & Tourist Villages
    "Calangute",
    "Candolim",
    "Baga",
    "Anjuna",
    "Vagator",
    "Arambol",
    "Morjim",
    "Mandrem",
    "Siolim",
    "Assagao",
    "Kerim",

    # North Goa Hinterland & Riverine Villages
    "Aldona",
    "Colvale",
    "Tivim",
    "Moira",
    "Marcel",
    "Old Goa",
    "Ribandar",
    "Britona",
    "Honda",
    "Usgao",

    # South Goa Major Hubs
    "Margao",
    "Vasco da Gama",
    "Cortalim",
    "Cuncolim",
    "Curchorem",
    "Canacona",
    "Quepem",
    "Sanguem",
    "Mormugao",

    # South Goa Coastal & Beach Villages
    "Colva",
    "Benaulim",
    "Majorda",
    "Betalbatim",
    "Varca",
    "Cavelossim",
    "Palolem",
    "Agonda",
    "Patnem",
    "Chaudi",
    "Bogmalo",

    # South Goa Hinterland Villages
    "Fatorda",
    "Navelim",
    "Nuvem",
    "Chinchinim",
    "Balli",
    "Rivona",
    "Sanvordem",
    "Shiroda",
    "Borim",
    "Curtorim",
    "Raia",
    "Loutolim",
    "Verna",
    "Chicalim",
    "Dabolim"
]

# Ensure uniqueness while preserving order
GOA_TOWNS = list(dict.fromkeys(GOA_TOWNS))


# -------------------------------------------------
# OUTSTATION DESTINATIONS
# -------------------------------------------------

OUTSTATION_CITIES = [
    # Maharashtra
    "Mumbai",
    "Pune",
    "Kolhapur",
    "Belgaum",
    "Nashik",
    "Solapur",
    "Ratnagiri",
    "Sawantwadi",
    "Kankavli",

    # Karnataka
    "Bangalore",
    "Mangalore",
    "Hubli",
    "Dharwad",
    "Mysore",
    "Udupi",
    "Karwar",
    "Gokarna",

    # Telangana & Tamil Nadu
    "Hyderabad",
    "Chennai"
]

OUTSTATION_CITIES = list(dict.fromkeys(OUTSTATION_CITIES))

ALL_DESTINATIONS = GOA_TOWNS + OUTSTATION_CITIES


# -------------------------------------------------
# BUS OPERATORS
# -------------------------------------------------

BUS_OPERATORS = [
    "Kadamba Transport (KTC)",
    "Paulo Travels",
    "Naik Tours & Travels",
    "Goa Express Shuttle",
    "Konkan Kanya Travels",
    "Mandovi Luxury Cruiser",
    "Zuari Link Lines",
    "Gomantak Superfast",
    "VRL Travels",
    "Seabird Tourists",
    "IntrCity SmartBus",
    "Sahyadri Coastal Express"
]


# -------------------------------------------------
# DESTINATION CATEGORIES & FARES
# -------------------------------------------------

LONG_HAUL = {
    "Mumbai",
    "Pune",
    "Bangalore",
    "Hyderabad",
    "Chennai",
    "Nashik",
    "Solapur"
}

MEDIUM_HAUL = {
    "Mangalore",
    "Hubli",
    "Belgaum",
    "Kolhapur",
    "Mysore",
    "Udupi",
    "Dharwad",
    "Ratnagiri",
    "Karwar",
    "Gokarna",
    "Sawantwadi",
    "Kankavli"
}

FARE_LOCAL = (40, 120)
FARE_MEDIUM = (350, 750)
FARE_LONG = (800, 1600)

BUS_TYPES = [
    "Seater",
    "Sleeper"
]

SLEEPER_MULTIPLIER = 1.5

SEAT_PATTERN = [
    "window",
    "aisle",
    "window",
    "aisle"
]