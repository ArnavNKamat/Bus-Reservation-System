# models/reservation.py

from models.user import User


class Reservation:
    """
    Represents a booking made by a passenger.
    """

    def __init__(
        self,
        booking_id: str,
        user: User,
        bus_id: str,
        seat_numbers: list[int],
        booking_time: str,
        total_fare: float
    ):
        self.booking_id = booking_id
        self.user = user
        self.bus_id = bus_id
        self.seat_numbers = seat_numbers
        self.booking_time = booking_time
        self.total_fare = total_fare

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
            "total_fare": self.total_fare
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Rebuild Reservation from JSON data.
        """

        return cls(
            data["booking_id"],
            User.from_dict(data["user"]),
            data["bus_id"],
            data["seat_numbers"],
            data["booking_time"],
            data["total_fare"]
        )

    def display(self, bus=None):
        """
        Pretty print reservation details.
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
        print(f"BOOKED ON  : {self.booking_time}")
        print(f"{'=' * 60}")

    def __str__(self):

        seats = ", ".join(
            map(str, self.seat_numbers)
        )

        return (
            f"{self.booking_id} | "
            f"Bus: {self.bus_id} | "
            f"Seats: {seats} | "
            f"Fare: Rs.{self.total_fare:.2f}"
        )
    
    def remove_seats(
        self,
        seats_to_remove
    ):

        self.seat_numbers = [

            seat

            for seat in self.seat_numbers

            if seat not in seats_to_remove
        ]