# models/bus.py

from datetime import datetime

from models.seat import Seat

from utils.constants import SEAT_PATTERN
from utils.exceptions import InvalidSeatError


class Bus:
    """
    Represents a bus and its seats.
    """

    def __init__(
        self,
        bus_id: str,
        name: str,
        source: str,
        destination: str,
        departure_dt: str,
        arrival_dt: str,
        total_seats: int,
        fare: float,
        bus_type: str
    ):

        self.bus_id = bus_id
        self.name = name

        self.source = source
        self.destination = destination

        self.departure_dt = departure_dt
        self.arrival_dt = arrival_dt

        self.fare = fare

        self.bus_type = bus_type

        self.seats = {}

        for i in range(1, total_seats + 1):

            seat_type = SEAT_PATTERN[(i - 1) % 4]

            self.seats[i] = Seat(
                i,
                seat_type
            )

    # -------------------------------------------------
    # DISPLAY HELPERS
    # -------------------------------------------------

    @property
    def route(self):

        return (
            f"{self.source}"
            f" -> "
            f"{self.destination}"
        )

    @staticmethod
    def _format_datetime(dt_string):

        try:

            dt = datetime.strptime(
                dt_string,
                "%Y-%m-%d %H:%M"
            )

            return dt.strftime(
                "%d %b %H:%M"
            )

        except ValueError:

            return dt_string

    @property
    def departure_display(self):

        return self._format_datetime(
            self.departure_dt
        )

    @property
    def arrival_display(self):

        return self._format_datetime(
            self.arrival_dt
        )

    def has_departed(self):

        try:

            dep = datetime.strptime(
                self.departure_dt,
                "%Y-%m-%d %H:%M"
            )

            return dep < datetime.now()

        except ValueError:

            return False

    # -------------------------------------------------
    # SEAT HELPERS
    # -------------------------------------------------

    @property
    def total_seats(self):

        return len(self.seats)

    @property
    def available_seats(self):

        return [
            seat_no
            for seat_no, seat in self.seats.items()
            if not seat.is_reserved
        ]
    
    @property
    def available_seats_count(self):

        return len(self.available_seats)

    @property
    def reserved_seats(self):

        return [
            seat_no
            for seat_no, seat in self.seats.items()
            if seat.is_reserved
        ]
    


    def get_seat(
        self,
        seat_number: int
    ):

        if seat_number not in self.seats:

            raise InvalidSeatError(
                f"Seat {seat_number} "
                f"does not exist "
                f"on bus {self.bus_id}."
            )

        return self.seats[seat_number]

    # -------------------------------------------------
    # SERIALIZATION
    # -------------------------------------------------

    def to_dict(self):

        return {

            "bus_id": self.bus_id,
            "name": self.name,

            "source": self.source,
            "destination": self.destination,

            "departure_dt": self.departure_dt,
            "arrival_dt": self.arrival_dt,

            "fare": self.fare,
            "bus_type": self.bus_type,

            "seats": {
                str(seat_no): seat.to_dict()
                for seat_no, seat
                in self.seats.items()
            }
        }

    @classmethod
    def from_dict(
        cls,
        data
    ):

        bus = cls(
            data["bus_id"],
            data["name"],

            data["source"],
            data["destination"],

            data["departure_dt"],
            data["arrival_dt"],

            0,
            data["fare"],
            data["bus_type"]
        )

        bus.seats = {

            int(seat_no):
            Seat.from_dict(seat_data)

            for seat_no, seat_data
            in data["seats"].items()
        }

        return bus

    # -------------------------------------------------
    # SEAT LAYOUT DISPLAY
    # -------------------------------------------------

    def display_layout(self):

        cols = 4

        print(
            "\n"
            + "=" * 60
        )

        print(
            f"Bus ID      : {self.bus_id}"
        )

        print(
            f"Bus Name    : {self.name}"
        )

        print(
            f"Bus Type    : {self.bus_type}"
        )

        print(
            f"Route       : {self.route}"
        )

        print(
            f"Departure   : {self.departure_display}"
        )

        print(
            f"Arrival     : {self.arrival_display}"
        )

        print(
            f"Fare        : Rs.{self.fare:.2f}"
        )

        print(
            "=" * 60
        )

        print(
            "\n[##] Available"
        )

        print(
            "[XX] Reserved\n"
        )

        rows = (
            self.total_seats + cols - 1
        ) // cols

        for row in range(rows):

            row_text = (
                f"Row {row + 1:02d} : "
            )

            for col in range(cols):

                seat_no = (
                    row * cols
                    + col
                    + 1
                )

                if seat_no <= self.total_seats:

                    seat = self.seats[
                        seat_no
                    ]

                    if seat.is_reserved:

                        tag = "[XX]"

                    else:

                        tag = (
                            f"[{seat_no:02d}]"
                        )

                    row_text += (
                        f"{tag:<8}"
                    )

            print(row_text)

        print()