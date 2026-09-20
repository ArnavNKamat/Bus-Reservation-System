# services/bus_generator.py

import random

from datetime import datetime, timedelta

from models.bus import Bus

from utils.constants import (
    GOA_TOWNS,
    ALL_DESTINATIONS,
    BUS_OPERATORS,
    BUS_SUFFIXES,
    LONG_HAUL,
    MEDIUM_HAUL,
    FARE_LOCAL,
    FARE_MEDIUM,
    FARE_LONG,
    BUS_TYPES
)


class BusGenerator:

    DEP_HOURS = [
        5, 6, 7, 8, 9,
        10, 11,
        14, 16, 18,
        20, 21, 22, 23
    ]

    @staticmethod
    def _fare_for(destination):

        if destination in LONG_HAUL:
            low, high = FARE_LONG

        elif destination in MEDIUM_HAUL:
            low, high = FARE_MEDIUM

        else:
            low, high = FARE_LOCAL

        return round(
            random.randint(low, high) / 10
        ) * 10

    @staticmethod
    def _travel_hours(destination):

        if destination in LONG_HAUL:
            return random.randint(8, 16)

        elif destination in MEDIUM_HAUL:
            return random.randint(3, 7)

        return random.randint(1, 3)

    @staticmethod
    def _next_bus_number(existing_buses):

        if not existing_buses:
            return 1

        highest = 0

        for bus_id in existing_buses:

            try:
                number = int(
                    bus_id.replace("B", "")
                )

                highest = max(
                    highest,
                    number
                )

            except ValueError:
                pass

        return highest + 1

    @classmethod
    def generate(
        cls,
        existing_buses=None,
        buses_per_day=8
    ):

        if existing_buses is None:
            existing_buses = {}

        buses = {}

        counter = cls._next_bus_number(
            existing_buses
        )

        today = datetime.now()

        for day_offset in range(3):

            current_day = (
                today +
                timedelta(days=day_offset)
            )

            hours = random.sample(
                cls.DEP_HOURS,
                min(
                    buses_per_day,
                    len(cls.DEP_HOURS)
                )
            )

            for hour in hours:

                minute = random.choice(
                    [0, 15, 30, 45]
                )

                departure_dt = current_day.replace(
                    hour=hour,
                    minute=minute,
                    second=0,
                    microsecond=0
                )

                source = random.choice(
                    GOA_TOWNS
                )

                destination = random.choice(
                    [
                        d
                        for d in ALL_DESTINATIONS
                        if d != source
                    ]
                )

                travel_hours = cls._travel_hours(
                    destination
                )

                arrival_dt = (
                    departure_dt +
                    timedelta(
                        hours=travel_hours
                    )
                )

                operator = random.choice(
                    BUS_OPERATORS
                )

                suffix = random.choice(
                    BUS_SUFFIXES
                )

                name = (
                    f"{operator} "
                    f"{suffix}"
                )

                bus_type = random.choice(
                    BUS_TYPES
                )

                fare = cls._fare_for(
                    destination
                )

                total_seats = random.choice(
                    [
                        28,
                        32,
                        36,
                        40,
                        44
                    ]
                )

                bus_id = (
                    f"B{counter:04d}"
                )

                bus = Bus(
                    bus_id=bus_id,
                    name=name,
                    source=source,
                    destination=destination,
                    departure_dt=departure_dt.strftime(
                        "%Y-%m-%d %H:%M"
                    ),
                    arrival_dt=arrival_dt.strftime(
                        "%Y-%m-%d %H:%M"
                    ),
                    total_seats=total_seats,
                    fare=fare,
                    bus_type=bus_type
                )

                buses[bus_id] = bus

                counter += 1

        return buses