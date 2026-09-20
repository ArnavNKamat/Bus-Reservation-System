# models/seat.py

from models.user import User

from utils.exceptions import (
    SeatNotAvailableError,
    ReservationNotFoundError
)


class Seat:
    """
    Represents one seat on a bus.
    """

    def __init__(
        self,
        seat_number: int,
        seat_type: str = "general"
    ):
        self.seat_number = seat_number
        self.seat_type = seat_type

        self.is_reserved = False

        self.passenger = None
        self.booking_id = ""

    def reserve(
        self,
        user: User,
        booking_id: str
    ):
        """
        Reserve this seat.
        """

        if self.is_reserved:
            raise SeatNotAvailableError(
                f"Seat {self.seat_number} is already reserved."
            )

        self.is_reserved = True
        self.passenger = user
        self.booking_id = booking_id

    def cancel(self):
        """
        Cancel reservation on this seat.
        """

        if not self.is_reserved:
            raise ReservationNotFoundError(
                f"Seat {self.seat_number} has no reservation."
            )

        self.is_reserved = False
        self.passenger = None
        self.booking_id = ""

    def to_dict(self) -> dict:
        """
        Convert seat to JSON-compatible dictionary.
        """

        return {
            "seat_number": self.seat_number,
            "seat_type": self.seat_type,
            "is_reserved": self.is_reserved,
            "passenger": (
                self.passenger.to_dict()
                if self.passenger
                else None
            ),
            "booking_id": self.booking_id
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Rebuild Seat from JSON data.
        """

        seat = cls(
            data["seat_number"],
            data["seat_type"]
        )

        seat.is_reserved = data["is_reserved"]

        if data["passenger"]:
            seat.passenger = User.from_dict(
                data["passenger"]
            )

        seat.booking_id = data["booking_id"]

        return seat

    def __str__(self):

        status = (
            "Reserved"
            if self.is_reserved
            else "Available"
        )

        return (
            f"Seat {self.seat_number} "
            f"({self.seat_type}) - "
            f"{status}"
        )