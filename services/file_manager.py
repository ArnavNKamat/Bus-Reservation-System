# services/file_manager.py

import json
import os

from datetime import datetime

from models.bus import Bus
from models.reservation import Reservation


class FileManager:

    DATA_FOLDER = "data"

    def __init__(self):

        os.makedirs(
            self.DATA_FOLDER,
            exist_ok=True
        )

    # ------------------------------
    # Date helpers
    # ------------------------------

    @staticmethod
    def today():

        return datetime.now().strftime(
            "%Y-%m-%d"
        )

    def buses_file(
        self,
        date_string=None
    ):

        if date_string is None:
            date_string = self.today()

        return os.path.join(
            self.DATA_FOLDER,
            f"buses_{date_string}.json"
        )

    def reservations_file(
        self,
        date_string=None
    ):

        if date_string is None:
            date_string = self.today()

        return os.path.join(
            self.DATA_FOLDER,
            f"reservations_{date_string}.json"
        )

    # ------------------------------
    # Bus storage
    # ------------------------------

    def load_buses(
        self,
        date_string=None
    ):

        filename = self.buses_file(
            date_string
        )

        try:

            with open(
                filename,
                "r"
            ) as f:

                data = json.load(f)

            return {
                bus_id:
                Bus.from_dict(info)

                for bus_id,
                info in data.items()
            }

        except FileNotFoundError:

            return {}

        except (
            json.JSONDecodeError,
            KeyError
        ):

            return {}

    def save_buses(
        self,
        buses,
        date_string=None
    ):

        filename = self.buses_file(
            date_string
        )

        with open(
            filename,
            "w"
        ) as f:

            json.dump(
                {
                    bus_id:
                    bus.to_dict()

                    for bus_id,
                    bus in buses.items()
                },
                f,
                indent=2
            )

    # ------------------------------
    # Reservation storage
    # ------------------------------

    def load_reservations(
        self,
        date_string=None
    ):

        filename = self.reservations_file(
            date_string
        )

        try:

            with open(
                filename,
                "r"
            ) as f:

                data = json.load(f)

            return {
                booking_id:
                Reservation.from_dict(info)

                for booking_id,
                info in data.items()
            }

        except FileNotFoundError:

            return {}

        except (
            json.JSONDecodeError,
            KeyError
        ):

            return {}

    def save_reservations(
        self,
        reservations,
        date_string=None
    ):

        filename = self.reservations_file(
            date_string
        )

        with open(
            filename,
            "w"
        ) as f:

            json.dump(
                {
                    booking_id:
                    reservation.to_dict()

                    for booking_id,
                    reservation in reservations.items()
                },
                f,
                indent=2
            )

    # ------------------------------
    # Utility
    # ------------------------------

    def file_exists_today(self):

        return os.path.exists(
            self.buses_file()
        )
    
    def available_bus_dates(self):

        dates = []

        for filename in os.listdir(
            self.DATA_FOLDER
        ):

            if (
                filename.startswith(
                    "buses_"
                )
                and
                filename.endswith(
                    ".json"
                )
            ):

                date_part = (
                    filename
                    .replace(
                        "buses_",
                        ""
                    )
                    .replace(
                        ".json",
                        ""
                    )
                )

                dates.append(
                    date_part
                )

        dates.sort()

        return dates
    
    def latest_bus_date(self):

        dates = (
            self.available_bus_dates()
        )

        if not dates:

            return None

        return dates[-1]