# services/reservation_system.py

from datetime import datetime

from models.user import User
from models.reservation import Reservation

from services.file_manager import FileManager
from services.bus_generator import BusGenerator

from utils.exceptions import (
    BusNotFoundError,
    ReservationNotFoundError,
    SeatNotAvailableError,
    InvalidSeatError
)


class ReservationSystem:

    def __init__(self):

        self.fm = FileManager()

        self.buses = self.fm.load_buses()

        self.reservations = (
            self.fm.load_reservations()
        )

        self._seed_buses_if_needed()

    # -------------------------------------------------
    # Startup
    # -------------------------------------------------

    def _seed_buses_if_needed(self):

        if self.buses:
            return

        print(
            "\nGenerating bus schedule..."
        )

        self.buses = (
            BusGenerator.generate()
        )

        self._create_demo_bookings()

        self.fm.save_buses(
            self.buses
        )

        self.fm.save_reservations(
            self.reservations
        )

        print(
            f"{len(self.buses)} buses generated."
        )

    # -------------------------------------------------
    # Booking IDs
    # -------------------------------------------------

    def _new_booking_id(self):

        timestamp = (
            datetime.now().strftime(
                "%Y%m%d%H%M%S"
            )
        )

        return (
            f"BKG-{timestamp}"
        )

    # -------------------------------------------------
    # Helpers
    # -------------------------------------------------

    def _get_bus(
        self,
        bus_id
    ):

        if bus_id not in self.buses:

            raise BusNotFoundError(
                f"Bus '{bus_id}' not found."
            )

        return self.buses[bus_id]

    def _get_reservation(
        self,
        booking_id
    ):

        if booking_id not in self.reservations:

            raise ReservationNotFoundError(
                f"Booking '{booking_id}' not found."
            )

        return self.reservations[
            booking_id
        ]

    @staticmethod
    def _input(prompt):

        return input(
            prompt
        ).strip()
    
    # -------------------------------------------------
    # Bus Visibility
    # -------------------------------------------------

    def visible_buses(self):
        """
        Return only buses whose departure
        time is still in the future.
        """

        now = datetime.now()

        visible = {}

        for bus_id, bus in self.buses.items():

            departure = datetime.strptime(
                bus.departure_dt,
                "%Y-%m-%d %H:%M"
            )

            if departure > now:
                visible[bus_id] = bus

        return visible

    # -------------------------------------------------
    # Bus Listing
    # -------------------------------------------------

    def list_buses(self):

        buses = self.visible_buses()

        if not buses:

            print("\nNo buses available.")
            return

        print("\n" + "=" * 90)
        print(
            f"{'ID':<8}"
            f"{'TYPE':<10}"
            f"{'ROUTE':<30}"
            f"{'DEPARTURE':<20}"
            f"{'FARE':<10}"
        )
        print("=" * 90)

        for bus in buses.values():

            print(
                f"{bus.bus_id:<8}"
                f"{bus.bus_type:<10}"
                f"{bus.route:<30}"
                f"{bus.departure_display:<20}"
                f"Rs.{bus.fare:<10.0f}"
            )

        print("=" * 90)

    # -------------------------------------------------
    # Bus Search
    # -------------------------------------------------

    def find_bus(self):

        bus_id = self._input(
            "\nEnter Bus ID: "
        )

        try:

            bus = self._get_bus(
                bus_id
            )

            print("\n" + "=" * 60)
            print(f"Bus ID      : {bus.bus_id}")
            print(f"Name        : {bus.name}")
            print(f"Type        : {bus.bus_type}")
            print(f"Route       : {bus.route}")
            print(f"Departure   : {bus.departure_display}")
            print(f"Arrival     : {bus.arrival_display}")
            print(f"Fare        : Rs.{bus.fare:.2f}")
            print(
                f"Seats       : "
                f"{bus.available_seats_count}/"
                f"{bus.total_seats}"
            )
            print("=" * 60)

        except BusNotFoundError as e:

            print("\n", e)

    # -------------------------------------------------
    # Seat Layout
    # -------------------------------------------------

    def view_seat_layout(self):

        bus_id = self._input(
            "\nEnter Bus ID: "
        )

        try:

            bus = self._get_bus(
                bus_id
            )

            print(
                f"\nSeat Layout for "
                f"{bus.bus_id}"
            )

            bus.display_layout()

        except BusNotFoundError as e:

            print("\n", e)

    # -------------------------------------------------
    # Booking
    # -------------------------------------------------

    def book_seats(self):

        try:

            bus_id = self._input(
                "\nEnter Bus ID: "
            )

            bus = self._get_bus(
                bus_id
            )

            print(
                f"\nSelected Bus: "
                f"{bus.route}"
            )

            bus.display_layout()

            name = self._input(
                "\nPassenger Name: "
            )

            phone = self._input(
                "Phone Number: "
            )

            email = self._input(
                "Email: "
            )

            seats_text = self._input(
                "Seat Numbers (comma separated): "
            )

            seat_numbers = [

                int(seat.strip())

                for seat in seats_text.split(",")
            ]

            for seat_no in seat_numbers:

                seat = bus.get_seat(
                    seat_no
                )

                if seat.is_reserved:

                    raise SeatNotAvailableError(
                        f"Seat {seat_no} "
                        f"is already reserved."
                    )

            booking_id = (
                self._new_booking_id()
            )

            user = User(
                name,
                phone,
                email
            )

            for seat_no in seat_numbers:

                bus.get_seat(
                    seat_no
                ).reserve(
                    user,
                    booking_id
                )

            total_fare = (
                len(seat_numbers)
                * bus.fare
            )

            reservation = Reservation(
                booking_id=booking_id,
                user=user,
                bus_id=bus.bus_id,
                seat_numbers=seat_numbers,
                booking_time=datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                total_fare=total_fare
            )

            self.reservations[
                booking_id
            ] = reservation

            self.fm.save_buses(
                self.buses
            )

            self.fm.save_reservations(
                self.reservations
            )

            print("\nBooking Successful!")

            reservation.display(
                bus
            )

        except (
            BusNotFoundError,
            InvalidSeatError,
            SeatNotAvailableError,
            ValueError
        ) as e:

            print(
                f"\nError: {e}"
            )

    # -------------------------------------------------
    # View Reservation
    # -------------------------------------------------

    def view_reservation(self):

        try:

            booking_id = self._input(
                "\nEnter Booking ID: "
            )

            reservation = (
                self._get_reservation(
                    booking_id
                )
            )

            bus = self._get_bus(
                reservation.bus_id
            )

            reservation.display(
                bus
            )

        except (
            ReservationNotFoundError,
            BusNotFoundError
        ) as e:

            print(
                f"\nError: {e}"
            )

    # -------------------------------------------------
    # Partial Cancellation
    # -------------------------------------------------

    def cancel_seats(self):

        try:

            booking_id = self._input(
                "\nEnter Booking ID: "
            )

            reservation = (
                self._get_reservation(
                    booking_id
                )
            )

            bus = self._get_bus(
                reservation.bus_id
            )

            print(
                f"\nBooked Seats: "
                f"{reservation.seat_numbers}"
            )

            seats_text = self._input(
                "Seats to cancel "
                "(comma separated): "
            )

            seats_to_cancel = [

                int(seat.strip())

                for seat in seats_text.split(",")
            ]

            for seat_no in seats_to_cancel:

                if seat_no not in (
                    reservation.seat_numbers
                ):

                    raise ValueError(
                        f"Seat {seat_no} "
                        f"is not part of "
                        f"this booking."
                    )

            for seat_no in seats_to_cancel:

                bus.get_seat(
                    seat_no
                ).cancel()

            reservation.remove_seats(
                seats_to_cancel
            )

            reservation.total_fare = (
                len(
                    reservation.seat_numbers
                )
                * bus.fare
            )

            if not reservation.seat_numbers:

                del self.reservations[
                    booking_id
                ]

                print(
                    "\nAll seats cancelled."
                )

                print(
                    "Reservation removed."
                )

            else:

                print(
                    "\nCancellation successful."
                )

                print(
                    "Remaining seats:",
                    reservation.seat_numbers
                )

                print(
                    f"Updated Fare: "
                    f"Rs."
                    f"{reservation.total_fare:.2f}"
                )

            self.fm.save_buses(
                self.buses
            )

            self.fm.save_reservations(
                self.reservations
            )

        except (
            ReservationNotFoundError,
            BusNotFoundError,
            ValueError
        ) as e:

            print(
                f"\nError: {e}"
            )

    # -------------------------------------------------
    # List All Reservations
    # -------------------------------------------------

    def list_reservations(self):

        if not self.reservations:

            print("\nNo reservations found.")

            return

        print("\n" + "=" * 100)

        print(
            f"{'BOOKING ID':<22}"
            f"{'PASSENGER':<20}"
            f"{'BUS ID':<10}"
            f"{'SEATS':<20}"
            f"{'FARE':<12}"
        )

        print("=" * 100)

        for reservation in self.reservations.values():

            seats = ", ".join(
                map(
                    str,
                    reservation.seat_numbers
                )
            )

            print(
                f"{reservation.booking_id:<22}"
                f"{reservation.user.name:<20}"
                f"{reservation.bus_id:<10}"
                f"{seats:<20}"
                f"Rs.{reservation.total_fare:<10.2f}"
            )

        print("=" * 100)

        print(
            f"\nTotal Reservations: "
            f"{len(self.reservations)}"
        )

    # -------------------------------------------------
    # Search By Phone Number
    # -------------------------------------------------

    def search_by_phone(self):

        phone = self._input(
            "\nEnter Phone Number: "
        )

        matches = []

        for reservation in (
            self.reservations.values()
        ):

            if (
                reservation.user.phone == phone
            ):

                matches.append(
                    reservation
                )

        if not matches:
            print(
                "\nNo reservations found."
            )

            return

        print(
            f"\nFound "
            f"{len(matches)} "
            f"reservation(s).\n"
        )

        for reservation in matches:

            try:

                bus = self._get_bus(
                    reservation.bus_id
                )
                reservation.display(
                    bus
                )
            except BusNotFoundError:

                reservation.display()
                
    # -------------------------------------------------
    # Search By Passenger Name
    # -------------------------------------------------

    def search_by_name(self):

        name = self._input(
            "\nEnter Passenger Name: "
        ).lower()

        matches = []

        for reservation in (
            self.reservations.values()
        ):

            if (
                name
                in
                reservation.user.name.lower()
            ):

                matches.append(
                    reservation
                )

        if not matches:

            print(
                "\nNo reservations found."
            )

            return

        print(
            f"\nFound "
            f"{len(matches)} "
            f"reservation(s).\n"
        )

        for reservation in matches:

            try:

                bus = self._get_bus(
                    reservation.bus_id
                )

                reservation.display(
                    bus
                )

            except BusNotFoundError:

                reservation.display()

    # -------------------------------------------------
    # Bus Occupancy Report
    # -------------------------------------------------

    def bus_occupancy_report(self):

        try:

            bus_id = self._input(
                "\nEnter Bus ID: "
            )

            bus = self._get_bus(
                bus_id
            )

            total = bus.total_seats

            reserved = len(
                bus.reserved_seats
            )

            available = len(
                bus.available_seats
            )

            occupancy = (
                reserved / total * 100
            )

            print("\n" + "=" * 60)

            print(
                f"Bus ID       : "
                f"{bus.bus_id}"
            )

            print(
                f"Name         : "
                f"{bus.name}"
            )

            print(
                f"Type         : "
                f"{bus.bus_type}"
            )

            print(
                f"Route        : "
                f"{bus.route}"
            )

            print(
                f"Departure    : "
                f"{bus.departure_display}"
            )

            print(
                f"Total Seats  : "
                f"{total}"
            )

            print(
                f"Reserved     : "
                f"{reserved}"
            )

            print(
                f"Available    : "
                f"{available}"
            )

            print(
                f"Occupancy    : "
                f"{occupancy:.2f}%"
            )

            print("=" * 60)

        except BusNotFoundError as e:

            print(
                f"\nError: {e}"
            )                
                
    # -------------------------------------------------
    # Daily Rollover
    # -------------------------------------------------

    def rollover_if_needed(self):

        if self.fm.file_exists_today():

            return

        latest_date = (
            self.fm.latest_bus_date()
        )

        if latest_date is None:

            return

        old_buses = (
            self.fm.load_buses(
                latest_date
            )
        )

        active_buses = {}

        for bus_id, bus in (
            old_buses.items()
        ):

            if not bus.has_departed():

                active_buses[
                    bus_id
                ] = bus

        new_buses = (
            BusGenerator.generate(
                existing_buses=
                active_buses
            )
        )

        active_buses.update(
            new_buses
        )

        self.fm.save_buses(
            active_buses
        )

        self.buses = (
            active_buses
        )            
        
    def _create_demo_bookings(self):
        import random

        from models.user import User
        from models.reservation import Reservation

        reservation_counter = 1

        for bus in self.buses.values():

        # 30% buses remain empty

            if random.random() < 0.30:

                continue

            max_bookings = max(
                1,
                bus.total_seats // 10
                )

            booking_count = random.randint(
                1,
                max_bookings
                )

            available = bus.available_seats.copy()

            for _ in range(booking_count):

                if not available:

                    break

                group_size = random.randint(
                    1,
                    min(4, len(available))
                    )

                chosen = random.sample(
                    available,
                    group_size
                    )

                booking_id = (
                    f"PRE{reservation_counter:05d}"
                    )

                reservation_counter += 1

                user = User(
                    f"Existing Customer "
                    f"{reservation_counter}",
                    f"900000{reservation_counter:04d}",
                    f"customer"
                    f"{reservation_counter}"
                    f"@mail.com"
                    )

                for seat_no in chosen:

                    bus.get_seat(
                        seat_no
                        ).reserve(
                            user,
                            booking_id
                            )

                    available.remove(
                        seat_no
                        )

                reservation = Reservation(
                    booking_id=booking_id,
                    user=user,
                    bus_id=bus.bus_id,
                    seat_numbers=chosen,
                    booking_time=datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                        ),
                    total_fare=(
                        len(chosen)
                        * bus.fare
                        )
                    )

                self.reservations[
                        booking_id
                    ] = reservation
    