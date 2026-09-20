# models/reservation.py

from datetime import datetime
from models.user import User


class Reservation:
    """
    Represents a booking made by a passenger with payment metadata and E-Ticket support.
    """

    def __init__(
        self,
        booking_id: str,
        user: User,
        bus_id: str,
        seat_numbers: list[int],
        booking_time: str,
        total_fare: float,
        payment_mode: str = "UPI / Card",
        payment_status: str = "Confirmed (Paid)",
        transaction_id: str = ""
    ):
        self.booking_id = booking_id
        self.user = user
        self.bus_id = bus_id
        self.seat_numbers = seat_numbers
        self.booking_time = booking_time
        self.total_fare = total_fare
        self.payment_mode = payment_mode
        self.payment_status = payment_status
        self.transaction_id = transaction_id or f"TXN-{booking_id.replace('BKG-', '').replace('PRE', '')}"

    @property
    def booking_time_display(self):
        """Display booking time formatted with 12-hour AM/PM."""
        try:
            dt = datetime.strptime(self.booking_time, "%Y-%m-%d %H:%M:%S")
            return dt.strftime("%d %b %Y, %I:%M %p")
        except ValueError:
            return self.booking_time

    def to_dict(self) -> dict:
        """
        Convert reservation into JSON-compatible dictionary.
        """
        return {
            "booking_id": self.booking_id,
            "user": self.user.to_dict(),
            "bus_id": self.bus_id,
            "seat_numbers": self.seat_numbers,
            "booking_time": self.booking_time,
            "booking_time_display": self.booking_time_display,
            "total_fare": self.total_fare,
            "payment_mode": self.payment_mode,
            "payment_status": self.payment_status,
            "transaction_id": self.transaction_id
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Rebuild Reservation from JSON data.
        """
        return cls(
            booking_id=data["booking_id"],
            user=User.from_dict(data["user"]),
            bus_id=data["bus_id"],
            seat_numbers=data["seat_numbers"],
            booking_time=data["booking_time"],
            total_fare=data["total_fare"],
            payment_mode=data.get("payment_mode", "UPI / Card"),
            payment_status=data.get("payment_status", "Confirmed (Paid)"),
            transaction_id=data.get("transaction_id", "")
        )

    def display(self, bus=None):
        """
        Pretty print reservation details in terminal CLI.
        """
        route = "N/A"
        departure = "N/A"

        if bus:
            route = bus.route
            departure = bus.departure_display

        print(f"\n{'=' * 60}")
        print(f"BOOKING ID : {self.booking_id}")
        print(f"PASSENGER  : {self.user}")
        print(f"BUS ID     : {self.bus_id}")
        print(f"ROUTE      : {route}")
        print(f"DEPARTURE  : {departure}")
        print(f"SEATS      : {', '.join(map(str, self.seat_numbers))}")
        print(f"TOTAL FARE : Rs.{self.total_fare:.2f}")
        print(f"PAYMENT    : {self.payment_mode} | {self.payment_status}")
        print(f"BOOKED ON  : {self.booking_time_display}")
        print(f"{'=' * 60}")

    def __str__(self):
        seats = ", ".join(map(str, self.seat_numbers))
        return (
            f"{self.booking_id} | "
            f"Bus: {self.bus_id} | "
            f"Seats: {seats} | "
            f"Fare: Rs.{self.total_fare:.2f}"
        )

    def remove_seats(self, seats_to_remove):
        self.seat_numbers = [
            seat for seat in self.seat_numbers
            if seat not in seats_to_remove
        ]