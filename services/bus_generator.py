# services/bus_generator.py

from datetime import datetime, timedelta
from models.bus import Bus
from utils.constants import (
    SLEEPER_MULTIPLIER
)


# Fixed Schedule Route Template Definitions
FIXED_ROUTE_TEMPLATES = [
    # -------------------------------------------------------------
    # INTRA-GOA EXPRESS SHUTTLES (High Frequency)
    # -------------------------------------------------------------
    # Panaji <-> Margao
    {"source": "Panaji", "destination": "Margao", "operator": "Kadamba Transport (KTC)", "name": "Kadamba Express Shuttle", "dep_time": "06:30", "duration_mins": 50, "fare": 50, "bus_type": "Seater", "seats": 40},
    {"source": "Panaji", "destination": "Margao", "operator": "Zuari Link Lines", "name": "Zuari Non-Stop", "dep_time": "08:00", "duration_mins": 50, "fare": 50, "bus_type": "Seater", "seats": 40},
    {"source": "Panaji", "destination": "Margao", "operator": "Kadamba Transport (KTC)", "name": "Kadamba AC Shuttle", "dep_time": "09:30", "duration_mins": 45, "fare": 65, "bus_type": "Seater", "seats": 36},
    {"source": "Panaji", "destination": "Margao", "operator": "Gomantak Superfast", "name": "Gomantak Superfast", "dep_time": "11:00", "duration_mins": 50, "fare": 50, "bus_type": "Seater", "seats": 40},
    {"source": "Panaji", "destination": "Margao", "operator": "Kadamba Transport (KTC)", "name": "Kadamba Express Shuttle", "dep_time": "13:30", "duration_mins": 50, "fare": 50, "bus_type": "Seater", "seats": 40},
    {"source": "Panaji", "destination": "Margao", "operator": "Zuari Link Lines", "name": "Zuari Non-Stop", "dep_time": "15:00", "duration_mins": 50, "fare": 50, "bus_type": "Seater", "seats": 40},
    {"source": "Panaji", "destination": "Margao", "operator": "Kadamba Transport (KTC)", "name": "Kadamba AC Shuttle", "dep_time": "16:30", "duration_mins": 45, "fare": 65, "bus_type": "Seater", "seats": 36},
    {"source": "Panaji", "destination": "Margao", "operator": "Goa Express Shuttle", "name": "Goa Star Shuttle", "dep_time": "18:00", "duration_mins": 50, "fare": 50, "bus_type": "Seater", "seats": 40},
    {"source": "Panaji", "destination": "Margao", "operator": "Kadamba Transport (KTC)", "name": "Kadamba Express Shuttle", "dep_time": "19:30", "duration_mins": 50, "fare": 50, "bus_type": "Seater", "seats": 40},
    {"source": "Panaji", "destination": "Margao", "operator": "Zuari Link Lines", "name": "Zuari Late Liner", "dep_time": "21:00", "duration_mins": 50, "fare": 50, "bus_type": "Seater", "seats": 40},

    # Margao <-> Panaji
    {"source": "Margao", "destination": "Panaji", "operator": "Kadamba Transport (KTC)", "name": "Kadamba Express Shuttle", "dep_time": "06:45", "duration_mins": 50, "fare": 50, "bus_type": "Seater", "seats": 40},
    {"source": "Margao", "destination": "Panaji", "operator": "Mandovi Luxury Cruiser", "name": "Mandovi Non-Stop", "dep_time": "08:15", "duration_mins": 50, "fare": 50, "bus_type": "Seater", "seats": 40},
    {"source": "Margao", "destination": "Panaji", "operator": "Kadamba Transport (KTC)", "name": "Kadamba AC Shuttle", "dep_time": "09:45", "duration_mins": 45, "fare": 65, "bus_type": "Seater", "seats": 36},
    {"source": "Margao", "destination": "Panaji", "operator": "Goa Express Shuttle", "name": "Goa Star Shuttle", "dep_time": "11:15", "duration_mins": 50, "fare": 50, "bus_type": "Seater", "seats": 40},
    {"source": "Margao", "destination": "Panaji", "operator": "Kadamba Transport (KTC)", "name": "Kadamba Express Shuttle", "dep_time": "13:45", "duration_mins": 50, "fare": 50, "bus_type": "Seater", "seats": 40},
    {"source": "Margao", "destination": "Panaji", "operator": "Mandovi Luxury Cruiser", "name": "Mandovi Non-Stop", "dep_time": "15:15", "duration_mins": 50, "fare": 50, "bus_type": "Seater", "seats": 40},
    {"source": "Margao", "destination": "Panaji", "operator": "Kadamba Transport (KTC)", "name": "Kadamba AC Shuttle", "dep_time": "16:45", "duration_mins": 45, "fare": 65, "bus_type": "Seater", "seats": 36},
    {"source": "Margao", "destination": "Panaji", "operator": "Zuari Link Lines", "name": "Zuari Evening Express", "dep_time": "18:15", "duration_mins": 50, "fare": 50, "bus_type": "Seater", "seats": 40},
    {"source": "Margao", "destination": "Panaji", "operator": "Kadamba Transport (KTC)", "name": "Kadamba Express Shuttle", "dep_time": "19:45", "duration_mins": 50, "fare": 50, "bus_type": "Seater", "seats": 40},
    {"source": "Margao", "destination": "Panaji", "operator": "Goa Express Shuttle", "name": "Goa Night Shuttle", "dep_time": "21:15", "duration_mins": 50, "fare": 50, "bus_type": "Seater", "seats": 40},

    # Panaji <-> Mapusa
    {"source": "Panaji", "destination": "Mapusa", "operator": "Kadamba Transport (KTC)", "name": "Kadamba North Shuttle", "dep_time": "07:00", "duration_mins": 30, "fare": 40, "bus_type": "Seater", "seats": 40},
    {"source": "Panaji", "destination": "Mapusa", "operator": "Goa Express Shuttle", "name": "Goa City Link", "dep_time": "08:30", "duration_mins": 30, "fare": 40, "bus_type": "Seater", "seats": 40},
    {"source": "Panaji", "destination": "Mapusa", "operator": "Kadamba Transport (KTC)", "name": "Kadamba AC Express", "dep_time": "10:00", "duration_mins": 25, "fare": 55, "bus_type": "Seater", "seats": 36},
    {"source": "Panaji", "destination": "Mapusa", "operator": "Naik Tours & Travels", "name": "Naik Metro Line", "dep_time": "12:00", "duration_mins": 30, "fare": 40, "bus_type": "Seater", "seats": 40},
    {"source": "Panaji", "destination": "Mapusa", "operator": "Kadamba Transport (KTC)", "name": "Kadamba North Shuttle", "dep_time": "14:00", "duration_mins": 30, "fare": 40, "bus_type": "Seater", "seats": 40},
    {"source": "Panaji", "destination": "Mapusa", "operator": "Goa Express Shuttle", "name": "Goa City Link", "dep_time": "16:00", "duration_mins": 30, "fare": 40, "bus_type": "Seater", "seats": 40},
    {"source": "Panaji", "destination": "Mapusa", "operator": "Kadamba Transport (KTC)", "name": "Kadamba North Shuttle", "dep_time": "17:30", "duration_mins": 30, "fare": 40, "bus_type": "Seater", "seats": 40},
    {"source": "Panaji", "destination": "Mapusa", "operator": "Mandovi Luxury Cruiser", "name": "Mandovi Express", "dep_time": "19:00", "duration_mins": 30, "fare": 40, "bus_type": "Seater", "seats": 40},
    {"source": "Panaji", "destination": "Mapusa", "operator": "Goa Express Shuttle", "name": "Goa Night Line", "dep_time": "20:30", "duration_mins": 30, "fare": 40, "bus_type": "Seater", "seats": 40},

    # Mapusa <-> Panaji
    {"source": "Mapusa", "destination": "Panaji", "operator": "Kadamba Transport (KTC)", "name": "Kadamba Capital Shuttle", "dep_time": "07:30", "duration_mins": 30, "fare": 40, "bus_type": "Seater", "seats": 40},
    {"source": "Mapusa", "destination": "Panaji", "operator": "Goa Express Shuttle", "name": "Goa City Link", "dep_time": "09:00", "duration_mins": 30, "fare": 40, "bus_type": "Seater", "seats": 40},
    {"source": "Mapusa", "destination": "Panaji", "operator": "Kadamba Transport (KTC)", "name": "Kadamba AC Express", "dep_time": "10:30", "duration_mins": 25, "fare": 55, "bus_type": "Seater", "seats": 36},
    {"source": "Mapusa", "destination": "Panaji", "operator": "Naik Tours & Travels", "name": "Naik Metro Line", "dep_time": "12:30", "duration_mins": 30, "fare": 40, "bus_type": "Seater", "seats": 40},
    {"source": "Mapusa", "destination": "Panaji", "operator": "Kadamba Transport (KTC)", "name": "Kadamba Capital Shuttle", "dep_time": "14:30", "duration_mins": 30, "fare": 40, "bus_type": "Seater", "seats": 40},
    {"source": "Mapusa", "destination": "Panaji", "operator": "Goa Express Shuttle", "name": "Goa City Link", "dep_time": "16:30", "duration_mins": 30, "fare": 40, "bus_type": "Seater", "seats": 40},
    {"source": "Mapusa", "destination": "Panaji", "operator": "Kadamba Transport (KTC)", "name": "Kadamba Capital Shuttle", "dep_time": "18:00", "duration_mins": 30, "fare": 40, "bus_type": "Seater", "seats": 40},
    {"source": "Mapusa", "destination": "Panaji", "operator": "Mandovi Luxury Cruiser", "name": "Mandovi Express", "dep_time": "19:30", "duration_mins": 30, "fare": 40, "bus_type": "Seater", "seats": 40},
    {"source": "Mapusa", "destination": "Panaji", "operator": "Goa Express Shuttle", "name": "Goa Night Line", "dep_time": "21:00", "duration_mins": 30, "fare": 40, "bus_type": "Seater", "seats": 40},

    # Panaji <-> Vasco da Gama
    {"source": "Panaji", "destination": "Vasco da Gama", "operator": "Kadamba Transport (KTC)", "name": "Kadamba Port Shuttle", "dep_time": "07:15", "duration_mins": 45, "fare": 45, "bus_type": "Seater", "seats": 40},
    {"source": "Panaji", "destination": "Vasco da Gama", "operator": "Zuari Link Lines", "name": "Zuari Harbor Shuttle", "dep_time": "09:15", "duration_mins": 45, "fare": 45, "bus_type": "Seater", "seats": 40},
    {"source": "Panaji", "destination": "Vasco da Gama", "operator": "Kadamba Transport (KTC)", "name": "Kadamba AC Airport Link", "dep_time": "11:30", "duration_mins": 40, "fare": 60, "bus_type": "Seater", "seats": 36},
    {"source": "Panaji", "destination": "Vasco da Gama", "operator": "Goa Express Shuttle", "name": "Goa Port Link", "dep_time": "14:15", "duration_mins": 45, "fare": 45, "bus_type": "Seater", "seats": 40},
    {"source": "Panaji", "destination": "Vasco da Gama", "operator": "Kadamba Transport (KTC)", "name": "Kadamba Port Shuttle", "dep_time": "16:45", "duration_mins": 45, "fare": 45, "bus_type": "Seater", "seats": 40},
    {"source": "Panaji", "destination": "Vasco da Gama", "operator": "Zuari Link Lines", "name": "Zuari Harbor Shuttle", "dep_time": "18:45", "duration_mins": 45, "fare": 45, "bus_type": "Seater", "seats": 40},
    {"source": "Panaji", "destination": "Vasco da Gama", "operator": "Goa Express Shuttle", "name": "Goa Evening Express", "dep_time": "20:15", "duration_mins": 45, "fare": 45, "bus_type": "Seater", "seats": 40},

    # Vasco da Gama <-> Panaji
    {"source": "Vasco da Gama", "destination": "Panaji", "operator": "Kadamba Transport (KTC)", "name": "Kadamba Port Shuttle", "dep_time": "07:45", "duration_mins": 45, "fare": 45, "bus_type": "Seater", "seats": 40},
    {"source": "Vasco da Gama", "destination": "Panaji", "operator": "Zuari Link Lines", "name": "Zuari Harbor Shuttle", "dep_time": "09:45", "duration_mins": 45, "fare": 45, "bus_type": "Seater", "seats": 40},
    {"source": "Vasco da Gama", "destination": "Panaji", "operator": "Kadamba Transport (KTC)", "name": "Kadamba AC Airport Link", "dep_time": "12:00", "duration_mins": 40, "fare": 60, "bus_type": "Seater", "seats": 36},
    {"source": "Vasco da Gama", "destination": "Panaji", "operator": "Goa Express Shuttle", "name": "Goa Port Link", "dep_time": "14:45", "duration_mins": 45, "fare": 45, "bus_type": "Seater", "seats": 40},
    {"source": "Vasco da Gama", "destination": "Panaji", "operator": "Kadamba Transport (KTC)", "name": "Kadamba Port Shuttle", "dep_time": "17:15", "duration_mins": 45, "fare": 45, "bus_type": "Seater", "seats": 40},
    {"source": "Vasco da Gama", "destination": "Panaji", "operator": "Zuari Link Lines", "name": "Zuari Harbor Shuttle", "dep_time": "19:15", "duration_mins": 45, "fare": 45, "bus_type": "Seater", "seats": 40},
    {"source": "Vasco da Gama", "destination": "Panaji", "operator": "Goa Express Shuttle", "name": "Goa Evening Express", "dep_time": "20:45", "duration_mins": 45, "fare": 45, "bus_type": "Seater", "seats": 40},

    # Margao <-> Vasco da Gama
    {"source": "Margao", "destination": "Vasco da Gama", "operator": "Konkan Kanya Travels", "name": "Konkan Coast Rider", "dep_time": "07:00", "duration_mins": 40, "fare": 40, "bus_type": "Seater", "seats": 36},
    {"source": "Margao", "destination": "Vasco da Gama", "operator": "Kadamba Transport (KTC)", "name": "Kadamba South Shuttle", "dep_time": "09:00", "duration_mins": 40, "fare": 40, "bus_type": "Seater", "seats": 40},
    {"source": "Margao", "destination": "Vasco da Gama", "operator": "Konkan Kanya Travels", "name": "Konkan Coast Rider", "dep_time": "11:00", "duration_mins": 40, "fare": 40, "bus_type": "Seater", "seats": 36},
    {"source": "Margao", "destination": "Vasco da Gama", "operator": "Kadamba Transport (KTC)", "name": "Kadamba South Shuttle", "dep_time": "14:00", "duration_mins": 40, "fare": 40, "bus_type": "Seater", "seats": 40},
    {"source": "Margao", "destination": "Vasco da Gama", "operator": "Konkan Kanya Travels", "name": "Konkan Coast Rider", "dep_time": "16:00", "duration_mins": 40, "fare": 40, "bus_type": "Seater", "seats": 36},
    {"source": "Margao", "destination": "Vasco da Gama", "operator": "Kadamba Transport (KTC)", "name": "Kadamba South Shuttle", "dep_time": "18:30", "duration_mins": 40, "fare": 40, "bus_type": "Seater", "seats": 40},
    {"source": "Margao", "destination": "Vasco da Gama", "operator": "Goa Express Shuttle", "name": "Goa South Line", "dep_time": "20:00", "duration_mins": 40, "fare": 40, "bus_type": "Seater", "seats": 40},

    # Vasco da Gama <-> Margao
    {"source": "Vasco da Gama", "destination": "Margao", "operator": "Konkan Kanya Travels", "name": "Konkan Coast Rider", "dep_time": "08:00", "duration_mins": 40, "fare": 40, "bus_type": "Seater", "seats": 36},
    {"source": "Vasco da Gama", "destination": "Margao", "operator": "Kadamba Transport (KTC)", "name": "Kadamba South Shuttle", "dep_time": "10:00", "duration_mins": 40, "fare": 40, "bus_type": "Seater", "seats": 40},
    {"source": "Vasco da Gama", "destination": "Margao", "operator": "Konkan Kanya Travels", "name": "Konkan Coast Rider", "dep_time": "12:00", "duration_mins": 40, "fare": 40, "bus_type": "Seater", "seats": 36},
    {"source": "Vasco da Gama", "destination": "Margao", "operator": "Kadamba Transport (KTC)", "name": "Kadamba South Shuttle", "dep_time": "15:00", "duration_mins": 40, "fare": 40, "bus_type": "Seater", "seats": 40},
    {"source": "Vasco da Gama", "destination": "Margao", "operator": "Konkan Kanya Travels", "name": "Konkan Coast Rider", "dep_time": "17:00", "duration_mins": 40, "fare": 40, "bus_type": "Seater", "seats": 36},
    {"source": "Vasco da Gama", "destination": "Margao", "operator": "Kadamba Transport (KTC)", "name": "Kadamba South Shuttle", "dep_time": "19:30", "duration_mins": 40, "fare": 40, "bus_type": "Seater", "seats": 40},
    {"source": "Vasco da Gama", "destination": "Margao", "operator": "Goa Express Shuttle", "name": "Goa South Line", "dep_time": "21:00", "duration_mins": 40, "fare": 40, "bus_type": "Seater", "seats": 40},

    # Panaji <-> Ponda
    {"source": "Panaji", "destination": "Ponda", "operator": "Gomantak Superfast", "name": "Gomantak Antruz Line", "dep_time": "07:30", "duration_mins": 45, "fare": 45, "bus_type": "Seater", "seats": 40},
    {"source": "Panaji", "destination": "Ponda", "operator": "Kadamba Transport (KTC)", "name": "Kadamba Central Shuttle", "dep_time": "09:30", "duration_mins": 45, "fare": 45, "bus_type": "Seater", "seats": 40},
    {"source": "Panaji", "destination": "Ponda", "operator": "Gomantak Superfast", "name": "Gomantak Antruz Line", "dep_time": "12:30", "duration_mins": 45, "fare": 45, "bus_type": "Seater", "seats": 40},
    {"source": "Panaji", "destination": "Ponda", "operator": "Kadamba Transport (KTC)", "name": "Kadamba Central Shuttle", "dep_time": "15:30", "duration_mins": 45, "fare": 45, "bus_type": "Seater", "seats": 40},
    {"source": "Panaji", "destination": "Ponda", "operator": "Gomantak Superfast", "name": "Gomantak Antruz Line", "dep_time": "17:30", "duration_mins": 45, "fare": 45, "bus_type": "Seater", "seats": 40},
    {"source": "Panaji", "destination": "Ponda", "operator": "Kadamba Transport (KTC)", "name": "Kadamba Central Shuttle", "dep_time": "19:30", "duration_mins": 45, "fare": 45, "bus_type": "Seater", "seats": 40},

    # Ponda <-> Panaji
    {"source": "Ponda", "destination": "Panaji", "operator": "Gomantak Superfast", "name": "Gomantak Antruz Line", "dep_time": "08:30", "duration_mins": 45, "fare": 45, "bus_type": "Seater", "seats": 40},
    {"source": "Ponda", "destination": "Panaji", "operator": "Kadamba Transport (KTC)", "name": "Kadamba Central Shuttle", "dep_time": "10:30", "duration_mins": 45, "fare": 45, "bus_type": "Seater", "seats": 40},
    {"source": "Ponda", "destination": "Panaji", "operator": "Gomantak Superfast", "name": "Gomantak Antruz Line", "dep_time": "13:30", "duration_mins": 45, "fare": 45, "bus_type": "Seater", "seats": 40},
    {"source": "Ponda", "destination": "Panaji", "operator": "Kadamba Transport (KTC)", "name": "Kadamba Central Shuttle", "dep_time": "16:30", "duration_mins": 45, "fare": 45, "bus_type": "Seater", "seats": 40},
    {"source": "Ponda", "destination": "Panaji", "operator": "Gomantak Superfast", "name": "Gomantak Antruz Line", "dep_time": "18:30", "duration_mins": 45, "fare": 45, "bus_type": "Seater", "seats": 40},
    {"source": "Ponda", "destination": "Panaji", "operator": "Kadamba Transport (KTC)", "name": "Kadamba Central Shuttle", "dep_time": "20:30", "duration_mins": 45, "fare": 45, "bus_type": "Seater", "seats": 40},

    # -------------------------------------------------------------
    # COASTAL & VILLAGE CONNECTORS
    # -------------------------------------------------------------
    # Panaji <-> Arambol (via Morjim, Mandrem, Siolim)
    {"source": "Panaji", "destination": "Arambol", "operator": "Naik Tours & Travels", "name": "Naik Northern Coast Cruiser", "dep_time": "07:00", "duration_mins": 75, "fare": 70, "bus_type": "Seater", "seats": 36},
    {"source": "Panaji", "destination": "Arambol", "operator": "Sahyadri Coastal Express", "name": "Sahyadri Beach Express", "dep_time": "10:30", "duration_mins": 75, "fare": 70, "bus_type": "Seater", "seats": 36},
    {"source": "Panaji", "destination": "Arambol", "operator": "Naik Tours & Travels", "name": "Naik Northern Coast Cruiser", "dep_time": "14:30", "duration_mins": 75, "fare": 70, "bus_type": "Seater", "seats": 36},
    {"source": "Panaji", "destination": "Arambol", "operator": "Sahyadri Coastal Express", "name": "Sahyadri Beach Express", "dep_time": "18:00", "duration_mins": 75, "fare": 70, "bus_type": "Seater", "seats": 36},

    {"source": "Arambol", "destination": "Panaji", "operator": "Naik Tours & Travels", "name": "Naik Northern Coast Cruiser", "dep_time": "08:45", "duration_mins": 75, "fare": 70, "bus_type": "Seater", "seats": 36},
    {"source": "Arambol", "destination": "Panaji", "operator": "Sahyadri Coastal Express", "name": "Sahyadri Beach Express", "dep_time": "12:15", "duration_mins": 75, "fare": 70, "bus_type": "Seater", "seats": 36},
    {"source": "Arambol", "destination": "Panaji", "operator": "Naik Tours & Travels", "name": "Naik Northern Coast Cruiser", "dep_time": "16:15", "duration_mins": 75, "fare": 70, "bus_type": "Seater", "seats": 36},
    {"source": "Arambol", "destination": "Panaji", "operator": "Sahyadri Coastal Express", "name": "Sahyadri Beach Express", "dep_time": "19:45", "duration_mins": 75, "fare": 70, "bus_type": "Seater", "seats": 36},

    # Mapusa <-> Calangute (via Candolim, Baga)
    {"source": "Mapusa", "destination": "Calangute", "operator": "Goa Express Shuttle", "name": "Calangute Beach Shuttle", "dep_time": "07:30", "duration_mins": 25, "fare": 35, "bus_type": "Seater", "seats": 32},
    {"source": "Mapusa", "destination": "Calangute", "operator": "Goa Express Shuttle", "name": "Calangute Beach Shuttle", "dep_time": "09:30", "duration_mins": 25, "fare": 35, "bus_type": "Seater", "seats": 32},
    {"source": "Mapusa", "destination": "Calangute", "operator": "Goa Express Shuttle", "name": "Calangute Beach Shuttle", "dep_time": "11:30", "duration_mins": 25, "fare": 35, "bus_type": "Seater", "seats": 32},
    {"source": "Mapusa", "destination": "Calangute", "operator": "Goa Express Shuttle", "name": "Calangute Beach Shuttle", "dep_time": "13:30", "duration_mins": 25, "fare": 35, "bus_type": "Seater", "seats": 32},
    {"source": "Mapusa", "destination": "Calangute", "operator": "Goa Express Shuttle", "name": "Calangute Beach Shuttle", "dep_time": "15:30", "duration_mins": 25, "fare": 35, "bus_type": "Seater", "seats": 32},
    {"source": "Mapusa", "destination": "Calangute", "operator": "Goa Express Shuttle", "name": "Calangute Beach Shuttle", "dep_time": "17:30", "duration_mins": 25, "fare": 35, "bus_type": "Seater", "seats": 32},
    {"source": "Mapusa", "destination": "Calangute", "operator": "Goa Express Shuttle", "name": "Calangute Beach Shuttle", "dep_time": "19:30", "duration_mins": 25, "fare": 35, "bus_type": "Seater", "seats": 32},

    {"source": "Calangute", "destination": "Mapusa", "operator": "Goa Express Shuttle", "name": "Calangute Beach Shuttle", "dep_time": "08:15", "duration_mins": 25, "fare": 35, "bus_type": "Seater", "seats": 32},
    {"source": "Calangute", "destination": "Mapusa", "operator": "Goa Express Shuttle", "name": "Calangute Beach Shuttle", "dep_time": "10:15", "duration_mins": 25, "fare": 35, "bus_type": "Seater", "seats": 32},
    {"source": "Calangute", "destination": "Mapusa", "operator": "Goa Express Shuttle", "name": "Calangute Beach Shuttle", "dep_time": "12:15", "duration_mins": 25, "fare": 35, "bus_type": "Seater", "seats": 32},
    {"source": "Calangute", "destination": "Mapusa", "operator": "Goa Express Shuttle", "name": "Calangute Beach Shuttle", "dep_time": "14:15", "duration_mins": 25, "fare": 35, "bus_type": "Seater", "seats": 32},
    {"source": "Calangute", "destination": "Mapusa", "operator": "Goa Express Shuttle", "name": "Calangute Beach Shuttle", "dep_time": "16:15", "duration_mins": 25, "fare": 35, "bus_type": "Seater", "seats": 32},
    {"source": "Calangute", "destination": "Mapusa", "operator": "Goa Express Shuttle", "name": "Calangute Beach Shuttle", "dep_time": "18:15", "duration_mins": 25, "fare": 35, "bus_type": "Seater", "seats": 32},
    {"source": "Calangute", "destination": "Mapusa", "operator": "Goa Express Shuttle", "name": "Calangute Beach Shuttle", "dep_time": "20:15", "duration_mins": 25, "fare": 35, "bus_type": "Seater", "seats": 32},

    # Panaji <-> Anjuna & Vagator
    {"source": "Panaji", "destination": "Anjuna", "operator": "Mandovi Luxury Cruiser", "name": "Mandovi Sunset Express", "dep_time": "08:00", "duration_mins": 45, "fare": 60, "bus_type": "Seater", "seats": 32},
    {"source": "Panaji", "destination": "Anjuna", "operator": "Mandovi Luxury Cruiser", "name": "Mandovi Sunset Express", "dep_time": "11:00", "duration_mins": 45, "fare": 60, "bus_type": "Seater", "seats": 32},
    {"source": "Panaji", "destination": "Anjuna", "operator": "Mandovi Luxury Cruiser", "name": "Mandovi Sunset Express", "dep_time": "15:00", "duration_mins": 45, "fare": 60, "bus_type": "Seater", "seats": 32},
    {"source": "Panaji", "destination": "Anjuna", "operator": "Mandovi Luxury Cruiser", "name": "Mandovi Sunset Express", "dep_time": "18:30", "duration_mins": 45, "fare": 60, "bus_type": "Seater", "seats": 32},

    # Margao <-> Palolem & Canacona (via Cuncolim, Agonda, Chaudi)
    {"source": "Margao", "destination": "Palolem", "operator": "Kadamba Transport (KTC)", "name": "Kadamba South Beach Link", "dep_time": "07:15", "duration_mins": 65, "fare": 65, "bus_type": "Seater", "seats": 36},
    {"source": "Margao", "destination": "Palolem", "operator": "Konkan Kanya Travels", "name": "Konkan Canacona Flyer", "dep_time": "10:15", "duration_mins": 65, "fare": 65, "bus_type": "Seater", "seats": 36},
    {"source": "Margao", "destination": "Palolem", "operator": "Kadamba Transport (KTC)", "name": "Kadamba South Beach Link", "dep_time": "13:45", "duration_mins": 65, "fare": 65, "bus_type": "Seater", "seats": 36},
    {"source": "Margao", "destination": "Palolem", "operator": "Konkan Kanya Travels", "name": "Konkan Canacona Flyer", "dep_time": "17:15", "duration_mins": 65, "fare": 65, "bus_type": "Seater", "seats": 36},

    {"source": "Palolem", "destination": "Margao", "operator": "Kadamba Transport (KTC)", "name": "Kadamba South Beach Link", "dep_time": "08:45", "duration_mins": 65, "fare": 65, "bus_type": "Seater", "seats": 36},
    {"source": "Palolem", "destination": "Margao", "operator": "Konkan Kanya Travels", "name": "Konkan Canacona Flyer", "dep_time": "11:45", "duration_mins": 65, "fare": 65, "bus_type": "Seater", "seats": 36},
    {"source": "Palolem", "destination": "Margao", "operator": "Kadamba Transport (KTC)", "name": "Kadamba South Beach Link", "dep_time": "15:15", "duration_mins": 65, "fare": 65, "bus_type": "Seater", "seats": 36},
    {"source": "Palolem", "destination": "Margao", "operator": "Konkan Kanya Travels", "name": "Konkan Canacona Flyer", "dep_time": "18:45", "duration_mins": 65, "fare": 65, "bus_type": "Seater", "seats": 36},

    # Margao <-> Colva & Benaulim (via Majorda, Varca, Cavelossim)
    {"source": "Margao", "destination": "Colva", "operator": "Goa Express Shuttle", "name": "Colva Beach Shuttle", "dep_time": "07:00", "duration_mins": 20, "fare": 30, "bus_type": "Seater", "seats": 32},
    {"source": "Margao", "destination": "Colva", "operator": "Goa Express Shuttle", "name": "Colva Beach Shuttle", "dep_time": "09:00", "duration_mins": 20, "fare": 30, "bus_type": "Seater", "seats": 32},
    {"source": "Margao", "destination": "Colva", "operator": "Goa Express Shuttle", "name": "Colva Beach Shuttle", "dep_time": "11:00", "duration_mins": 20, "fare": 30, "bus_type": "Seater", "seats": 32},
    {"source": "Margao", "destination": "Colva", "operator": "Goa Express Shuttle", "name": "Colva Beach Shuttle", "dep_time": "14:00", "duration_mins": 20, "fare": 30, "bus_type": "Seater", "seats": 32},
    {"source": "Margao", "destination": "Colva", "operator": "Goa Express Shuttle", "name": "Colva Beach Shuttle", "dep_time": "16:30", "duration_mins": 20, "fare": 30, "bus_type": "Seater", "seats": 32},
    {"source": "Margao", "destination": "Colva", "operator": "Goa Express Shuttle", "name": "Colva Beach Shuttle", "dep_time": "18:30", "duration_mins": 20, "fare": 30, "bus_type": "Seater", "seats": 32},

    # Panaji <-> Valpoi & Sanquelim (via Old Goa, Marcel, Bicholim, Honda)
    {"source": "Panaji", "destination": "Valpoi", "operator": "Kadamba Transport (KTC)", "name": "Kadamba Sattari Link", "dep_time": "07:30", "duration_mins": 60, "fare": 65, "bus_type": "Seater", "seats": 36},
    {"source": "Panaji", "destination": "Valpoi", "operator": "Kadamba Transport (KTC)", "name": "Kadamba Sattari Link", "dep_time": "11:30", "duration_mins": 60, "fare": 65, "bus_type": "Seater", "seats": 36},
    {"source": "Panaji", "destination": "Valpoi", "operator": "Kadamba Transport (KTC)", "name": "Kadamba Sattari Link", "dep_time": "15:30", "duration_mins": 60, "fare": 65, "bus_type": "Seater", "seats": 36},
    {"source": "Panaji", "destination": "Valpoi", "operator": "Kadamba Transport (KTC)", "name": "Kadamba Sattari Link", "dep_time": "19:00", "duration_mins": 60, "fare": 65, "bus_type": "Seater", "seats": 36},

    # Margao <-> Curchorem & Sanguem (via Quepem, Rivona, Sanvordem)
    {"source": "Margao", "destination": "Curchorem", "operator": "Kadamba Transport (KTC)", "name": "Kadamba Mining Belt Express", "dep_time": "07:45", "duration_mins": 50, "fare": 55, "bus_type": "Seater", "seats": 36},
    {"source": "Margao", "destination": "Curchorem", "operator": "Kadamba Transport (KTC)", "name": "Kadamba Mining Belt Express", "dep_time": "11:45", "duration_mins": 50, "fare": 55, "bus_type": "Seater", "seats": 36},
    {"source": "Margao", "destination": "Curchorem", "operator": "Kadamba Transport (KTC)", "name": "Kadamba Mining Belt Express", "dep_time": "15:45", "duration_mins": 50, "fare": 55, "bus_type": "Seater", "seats": 36},
    {"source": "Margao", "destination": "Curchorem", "operator": "Kadamba Transport (KTC)", "name": "Kadamba Mining Belt Express", "dep_time": "18:45", "duration_mins": 50, "fare": 55, "bus_type": "Seater", "seats": 36},

    # -------------------------------------------------------------
    # OUTSTATION INTERSTATE ROUTES (Luxury Seater & Sleeper)
    # -------------------------------------------------------------
    # Panaji -> Mumbai
    {"source": "Panaji", "destination": "Mumbai", "operator": "Paulo Travels", "name": "Paulo Luxury Multi-Axle", "dep_time": "18:00", "duration_mins": 780, "fare": 950, "bus_type": "Seater", "seats": 40},
    {"source": "Panaji", "destination": "Mumbai", "operator": "IntrCity SmartBus", "name": "IntrCity AC Sleeper", "dep_time": "19:30", "duration_mins": 750, "fare": 1350, "bus_type": "Sleeper", "seats": 32},
    {"source": "Panaji", "destination": "Mumbai", "operator": "Kadamba Transport (KTC)", "name": "Kadamba Volvo AC Sleeper", "dep_time": "21:00", "duration_mins": 720, "fare": 1450, "bus_type": "Sleeper", "seats": 30},

    # Margao -> Mumbai
    {"source": "Margao", "destination": "Mumbai", "operator": "VRL Travels", "name": "VRL I-Shift Multi-Axle", "dep_time": "17:30", "duration_mins": 810, "fare": 980, "bus_type": "Seater", "seats": 40},
    {"source": "Margao", "destination": "Mumbai", "operator": "Paulo Travels", "name": "Paulo Super Deluxe Sleeper", "dep_time": "19:00", "duration_mins": 780, "fare": 1400, "bus_type": "Sleeper", "seats": 32},
    {"source": "Margao", "destination": "Mumbai", "operator": "Seabird Tourists", "name": "Seabird AC Volvo Sleeper", "dep_time": "20:30", "duration_mins": 750, "fare": 1500, "bus_type": "Sleeper", "seats": 30},

    # Panaji -> Pune
    {"source": "Panaji", "destination": "Pune", "operator": "Paulo Travels", "name": "Paulo Deccan Express", "dep_time": "19:00", "duration_mins": 600, "fare": 850, "bus_type": "Seater", "seats": 40},
    {"source": "Panaji", "destination": "Pune", "operator": "IntrCity SmartBus", "name": "IntrCity AC Sleeper", "dep_time": "20:45", "duration_mins": 570, "fare": 1250, "bus_type": "Sleeper", "seats": 32},
    {"source": "Panaji", "destination": "Pune", "operator": "Kadamba Transport (KTC)", "name": "Kadamba Garuda AC", "dep_time": "22:00", "duration_mins": 540, "fare": 1300, "bus_type": "Sleeper", "seats": 30},

    # Margao -> Pune
    {"source": "Margao", "destination": "Pune", "operator": "VRL Travels", "name": "VRL Deccan Express", "dep_time": "18:30", "duration_mins": 630, "fare": 880, "bus_type": "Seater", "seats": 40},
    {"source": "Margao", "destination": "Pune", "operator": "Paulo Travels", "name": "Paulo AC Sleeper", "dep_time": "20:15", "duration_mins": 600, "fare": 1300, "bus_type": "Sleeper", "seats": 32},

    # Panaji -> Bangalore
    {"source": "Panaji", "destination": "Bangalore", "operator": "VRL Travels", "name": "VRL Multi-Axle AC Sleeper", "dep_time": "17:00", "duration_mins": 780, "fare": 1450, "bus_type": "Sleeper", "seats": 32},
    {"source": "Panaji", "destination": "Bangalore", "operator": "Seabird Tourists", "name": "Seabird Silicon Cruiser", "dep_time": "19:15", "duration_mins": 750, "fare": 1050, "bus_type": "Seater", "seats": 40},
    {"source": "Panaji", "destination": "Bangalore", "operator": "Kadamba Transport (KTC)", "name": "Kadamba Rajahamsa AC Sleeper", "dep_time": "21:30", "duration_mins": 720, "fare": 1550, "bus_type": "Sleeper", "seats": 30},

    # Margao -> Bangalore
    {"source": "Margao", "destination": "Bangalore", "operator": "Seabird Tourists", "name": "Seabird AC Volvo Sleeper", "dep_time": "16:30", "duration_mins": 810, "fare": 1500, "bus_type": "Sleeper", "seats": 32},
    {"source": "Margao", "destination": "Bangalore", "operator": "VRL Travels", "name": "VRL Express Seater", "dep_time": "18:45", "duration_mins": 780, "fare": 1050, "bus_type": "Seater", "seats": 40},
    {"source": "Margao", "destination": "Bangalore", "operator": "Kadamba Transport (KTC)", "name": "Kadamba Rajahamsa AC Sleeper", "dep_time": "21:00", "duration_mins": 750, "fare": 1550, "bus_type": "Sleeper", "seats": 30},

    # Panaji -> Hyderabad
    {"source": "Panaji", "destination": "Hyderabad", "operator": "Paulo Travels", "name": "Paulo Pearl City Sleeper", "dep_time": "16:00", "duration_mins": 900, "fare": 1600, "bus_type": "Sleeper", "seats": 32},
    {"source": "Panaji", "destination": "Hyderabad", "operator": "VRL Travels", "name": "VRL Multi-Axle AC Sleeper", "dep_time": "18:00", "duration_mins": 870, "fare": 1750, "bus_type": "Sleeper", "seats": 30},

    # Margao -> Mangalore & Udupi
    {"source": "Margao", "destination": "Mangalore", "operator": "Kadamba Transport (KTC)", "name": "Kadamba Coastal Superfast", "dep_time": "07:00", "duration_mins": 360, "fare": 450, "bus_type": "Seater", "seats": 40},
    {"source": "Margao", "destination": "Mangalore", "operator": "Seabird Tourists", "name": "Seabird Coastal Express", "dep_time": "14:00", "duration_mins": 360, "fare": 480, "bus_type": "Seater", "seats": 36},
    {"source": "Margao", "destination": "Mangalore", "operator": "VRL Travels", "name": "VRL Coastal AC Sleeper", "dep_time": "21:00", "duration_mins": 330, "fare": 750, "bus_type": "Sleeper", "seats": 32},

    # Panaji -> Belgaum & Kolhapur
    {"source": "Panaji", "destination": "Belgaum", "operator": "Kadamba Transport (KTC)", "name": "Kadamba Ghat Express", "dep_time": "06:30", "duration_mins": 210, "fare": 350, "bus_type": "Seater", "seats": 40},
    {"source": "Panaji", "destination": "Belgaum", "operator": "Naik Tours & Travels", "name": "Naik Sahyadri Shuttle", "dep_time": "10:30", "duration_mins": 210, "fare": 350, "bus_type": "Seater", "seats": 40},
    {"source": "Panaji", "destination": "Kolhapur", "operator": "Kadamba Transport (KTC)", "name": "Kadamba Mahalaxmi Line", "dep_time": "15:00", "duration_mins": 300, "fare": 450, "bus_type": "Seater", "seats": 40},
    {"source": "Panaji", "destination": "Kolhapur", "operator": "Paulo Travels", "name": "Paulo Kolhapur Cruiser", "dep_time": "18:30", "duration_mins": 300, "fare": 500, "bus_type": "Seater", "seats": 36},

    # Margao -> Hubli & Dharwad
    {"source": "Margao", "destination": "Hubli", "operator": "Kadamba Transport (KTC)", "name": "Kadamba Deccan Express", "dep_time": "07:30", "duration_mins": 270, "fare": 380, "bus_type": "Seater", "seats": 40},
    {"source": "Margao", "destination": "Hubli", "operator": "VRL Travels", "name": "VRL Hubli Non-Stop", "dep_time": "13:30", "duration_mins": 270, "fare": 400, "bus_type": "Seater", "seats": 40},
    {"source": "Margao", "destination": "Hubli", "operator": "Seabird Tourists", "name": "Seabird AC Sleeper", "dep_time": "19:30", "duration_mins": 240, "fare": 600, "bus_type": "Sleeper", "seats": 32}
]


class BusGenerator:
    """
    Generates structured, realistic fixed bus timetables for 3 consecutive days
    (Today, Tomorrow, Day After Tomorrow).
    """

    @staticmethod
    def _next_bus_number(existing_buses):
        if not existing_buses:
            return 1

        highest = 0
        for bus_id in existing_buses:
            try:
                number = int(bus_id.replace("B", ""))
                highest = max(highest, number)
            except ValueError:
                pass
        return highest + 1

    @classmethod
    def generate(
        cls,
        existing_buses=None,
        days_window=3
    ):
        """
        Generate fixed schedule buses for `days_window` days (Today, Today+1, Today+2).
        """
        if existing_buses is None:
            existing_buses = {}

        buses = {}
        counter = cls._next_bus_number(existing_buses)
        today = datetime.now()

        for day_offset in range(days_window):
            current_day = today + timedelta(days=day_offset)
            date_str = current_day.strftime("%Y-%m-%d")

            for template in FIXED_ROUTE_TEMPLATES:
                hour_str, min_str = template["dep_time"].split(":")
                hour = int(hour_str)
                minute = int(min_str)

                dep_dt = current_day.replace(
                    hour=hour,
                    minute=minute,
                    second=0,
                    microsecond=0
                )

                arr_dt = dep_dt + timedelta(minutes=template["duration_mins"])

                bus_id = f"B{counter:04d}"
                counter += 1

                bus = Bus(
                    bus_id=bus_id,
                    name=template["name"],
                    source=template["source"],
                    destination=template["destination"],
                    departure_dt=dep_dt.strftime("%Y-%m-%d %H:%M"),
                    arrival_dt=arr_dt.strftime("%Y-%m-%d %H:%M"),
                    total_seats=template["seats"],
                    fare=float(template["fare"]),
                    bus_type=template["bus_type"]
                )

                buses[bus_id] = bus

        return buses