# services/reservation_system.py

import random
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
        self.reservations = self.fm.load_reservations()
        self.users = self.fm.load_users()

        self._seed_buses_if_needed()
        self._seed_users_if_needed()

    # -------------------------------------------------
    # Startup & Seeding
    # -------------------------------------------------

    def _seed_buses_if_needed(self):
        if self.buses:
            return

        print("\nGenerating Goa Express fixed bus schedule (3-day window)...")
        self.buses = BusGenerator.generate(days_window=3)
        self._create_demo_bookings()

        self.fm.save_buses(self.buses)
        self.fm.save_reservations(self.reservations)
        print(f"{len(self.buses)} scheduled buses generated across 3 days.")

    def _seed_users_if_needed(self):
        if self.users:
            return

        demo_user = User(
            name="Arnav Kamat",
            phone="9876543210",
            email="arnav@example.com"
        )
        demo_user.set_password("pass123")
        self.users[demo_user.email] = demo_user
        self.fm.save_users(self.users)

    # -------------------------------------------------
    # User Authentication Helpers
    # -------------------------------------------------

    def register_user(self, name: str, phone: str, email: str, password: str) -> User:
        email = email.strip().lower()
        if email in self.users:
            raise ValueError(f"An account with email '{email}' already exists.")

        user = User(name=name, phone=phone, email=email)
        user.set_password(password)
        self.users[email] = user
        self.fm.save_users(self.users)
        return user

    def authenticate_user(self, email_or_phone: str, password: str) -> User:
        email_or_phone = email_or_phone.strip().lower()
        target_user = None

        # Look up by email or phone
        for user in self.users.values():
            if user.email.lower() == email_or_phone or user.phone == email_or_phone:
                target_user = user
                break

        if not target_user:
            raise ValueError("No account found with this email or phone number.")

        if not target_user.verify_password(password):
            raise ValueError("Incorrect password. Please try again.")

        return target_user

    # -------------------------------------------------
    # Booking IDs
    # -------------------------------------------------

    def _new_booking_id(self):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"BKG-{timestamp}"

    # -------------------------------------------------
    # Helpers
    # -------------------------------------------------

    def _get_bus(self, bus_id):
        if bus_id not in self.buses:
            raise BusNotFoundError(f"Bus '{bus_id}' not found.")
        return self.buses[bus_id]

    def _get_reservation(self, booking_id):
        if booking_id not in self.reservations:
            raise ReservationNotFoundError(f"Booking '{booking_id}' not found.")
        return self.reservations[booking_id]

    @staticmethod
    def _input(prompt):
        return input(prompt).strip()

    # -------------------------------------------------
    # Bus Visibility (Up to 3 days from now)
    # -------------------------------------------------

    def visible_buses(self):
        """
        Return only buses whose departure time is still in the future.
        """
        now = datetime.now()
        visible = {}

        for bus_id, bus in self.buses.items():
            try:
                departure = datetime.strptime(bus.departure_dt, "%Y-%m-%d %H:%M")
                if departure > now:
                    visible[bus_id] = bus
            except ValueError:
                visible[bus_id] = bus

        return visible

    # -------------------------------------------------
    # Bus Listing (CLI)
    # -------------------------------------------------

    def list_buses(self):
        buses = self.visible_buses()
        if not buses:
            print("\nNo buses available.")
            return

        print("\n" + "=" * 105)
        print(
            f"{'ID':<8}"
            f"{'TYPE':<10}"
            f"{'ROUTE':<36}"
            f"{'DEPARTURE (12h)':<25}"
            f"{'FARE':<10}"
            f"{'SEATS':<10}"
        )
        print("=" * 105)

        for bus in buses.values():
            seats_str = f"{bus.available_seats_count}/{bus.total_seats}"
            print(
                f"{bus.bus_id:<8}"
                f"{bus.bus_type:<10}"
                f"{bus.route:<36}"
                f"{bus.departure_display:<25}"
                f"Rs.{bus.fare:<8.0f}"
                f"{seats_str:<10}"
            )

        print("=" * 105)

    # -------------------------------------------------
    # Bus Search (CLI)
    # -------------------------------------------------

    def find_bus(self):
        bus_id = self._input("\nEnter Bus ID: ")
        try:
            bus = self._get_bus(bus_id)
            print("\n" + "=" * 60)
            print(f"Bus ID      : {bus.bus_id}")
            print(f"Name        : {bus.name}")
            print(f"Type        : {bus.bus_type}")
            print(f"Route       : {bus.route}")
            print(f"Departure   : {bus.departure_display}")
            print(f"Arrival     : {bus.arrival_display}")
            print(f"Fare        : Rs.{bus.fare:.2f}")
            print(f"Seats       : {bus.available_seats_count}/{bus.total_seats} available")
            print("=" * 60)
        except BusNotFoundError as e:
            print("\n", e)

    # -------------------------------------------------
    # Seat Layout (CLI)
    # -------------------------------------------------

    def view_seat_layout(self):
        bus_id = self._input("\nEnter Bus ID: ")
        try:
            bus = self._get_bus(bus_id)
            print(f"\nSeat Layout for {bus.bus_id} ({bus.name})")
            bus.display_layout()
        except BusNotFoundError as e:
            print("\n", e)

    # -------------------------------------------------
    # Booking (CLI)
    # -------------------------------------------------

    def book_seats(self):
        try:
            bus_id = self._input("\nEnter Bus ID: ")
            bus = self._get_bus(bus_id)

            print(f"\nSelected Bus: {bus.route} ({bus.departure_display})")
            bus.display_layout()

            name = self._input("\nPassenger Name: ")
            phone = self._input("Phone Number: ")
            email = self._input("Email: ")
            seats_text = self._input("Seat Numbers (comma separated): ")

            seat_numbers = [int(seat.strip()) for seat in seats_text.split(",")]

            for seat_no in seat_numbers:
                seat = bus.get_seat(seat_no)
                if seat.is_reserved:
                    raise SeatNotAvailableError(f"Seat {seat_no} is already reserved.")

            print("\nSelect Payment Method:")
            print("1. UPI (GPay / PhonePe / Paytm)")
            print("2. Credit / Debit Card")
            print("3. Net Banking")
            print("4. Cash on Boarding")
            pay_choice = self._input("Payment Choice (1-4) [default: 1]: ") or "1"
            pay_modes = {
                "1": "UPI (GPay / PhonePe)",
                "2": "Credit/Debit Card",
                "3": "Net Banking",
                "4": "Cash on Boarding"
            }
            payment_mode = pay_modes.get(pay_choice, "UPI")

            booking_id = self._new_booking_id()
            user = User(name, phone, email)

            for seat_no in seat_numbers:
                bus.get_seat(seat_no).reserve(user, booking_id)

            total_fare = len(seat_numbers) * bus.fare

            reservation = Reservation(
                booking_id=booking_id,
                user=user,
                bus_id=bus.bus_id,
                seat_numbers=seat_numbers,
                booking_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                total_fare=total_fare,
                payment_mode=payment_mode,
                payment_status="Confirmed (Paid)"
            )

            self.reservations[booking_id] = reservation
            self.fm.save_buses(self.buses)
            self.fm.save_reservations(self.reservations)

            print("\nBooking Successful! Here is your E-Ticket:")
            reservation.display(bus)

        except (
            BusNotFoundError,
            InvalidSeatError,
            SeatNotAvailableError,
            ValueError
        ) as e:
            print(f"\nError: {e}")

    # -------------------------------------------------
    # View Reservation (CLI)
    # -------------------------------------------------

    def view_reservation(self):
        try:
            booking_id = self._input("\nEnter Booking ID: ")
            reservation = self._get_reservation(booking_id)
            bus = self._get_bus(reservation.bus_id)
            reservation.display(bus)
        except (ReservationNotFoundError, BusNotFoundError) as e:
            print(f"\nError: {e}")

    # -------------------------------------------------
    # Cancellation (CLI)
    # -------------------------------------------------

    def cancel_seats(self):
        try:
            booking_id = self._input("\nEnter Booking ID: ")
            reservation = self._get_reservation(booking_id)
            bus = self._get_bus(reservation.bus_id)

            print(f"\nBooked Seats: {reservation.seat_numbers}")
            seats_text = self._input("Seats to cancel (comma separated): ")
            seats_to_cancel = [int(seat.strip()) for seat in seats_text.split(",")]

            for seat_no in seats_to_cancel:
                if seat_no not in reservation.seat_numbers:
                    raise ValueError(f"Seat {seat_no} is not part of this booking.")

            for seat_no in seats_to_cancel:
                bus.get_seat(seat_no).cancel()

            reservation.remove_seats(seats_to_cancel)
            reservation.total_fare = len(reservation.seat_numbers) * bus.fare

            if not reservation.seat_numbers:
                del self.reservations[booking_id]
                print("\nAll seats cancelled. Reservation removed.")
            else:
                print("\nCancellation successful.")
                print("Remaining seats:", reservation.seat_numbers)
                print(f"Updated Fare: Rs.{reservation.total_fare:.2f}")

            self.fm.save_buses(self.buses)
            self.fm.save_reservations(self.reservations)

        except (ReservationNotFoundError, BusNotFoundError, ValueError) as e:
            print(f"\nError: {e}")

    # -------------------------------------------------
    # List All Reservations (CLI)
    # -------------------------------------------------

    def list_reservations(self):
        if not self.reservations:
            print("\nNo reservations found.")
            return

        print("\n" + "=" * 115)
        print(
            f"{'BOOKING ID':<22}"
            f"{'PASSENGER':<20}"
            f"{'BUS ID':<10}"
            f"{'SEATS':<18}"
            f"{'FARE':<12}"
            f"{'BOOKED ON (12h)':<25}"
        )
        print("=" * 115)

        for reservation in self.reservations.values():
            seats = ", ".join(map(str, reservation.seat_numbers))
            print(
                f"{reservation.booking_id:<22}"
                f"{reservation.user.name:<20}"
                f"{reservation.bus_id:<10}"
                f"{seats:<18}"
                f"Rs.{reservation.total_fare:<10.2f}"
                f"{reservation.booking_time_display:<25}"
            )

        print("=" * 115)
        print(f"\nTotal Reservations: {len(self.reservations)}")

    # -------------------------------------------------
    # Search By Phone (CLI)
    # -------------------------------------------------

    def search_by_phone(self):
        phone = self._input("\nEnter Phone Number: ")
        matches = [r for r in self.reservations.values() if r.user.phone == phone]

        if not matches:
            print("\nNo reservations found.")
            return

        print(f"\nFound {len(matches)} reservation(s).\n")
        for reservation in matches:
            try:
                bus = self._get_bus(reservation.bus_id)
                reservation.display(bus)
            except BusNotFoundError:
                reservation.display()

    # -------------------------------------------------
    # Search By Passenger Name (CLI)
    # -------------------------------------------------

    def search_by_name(self):
        name = self._input("\nEnter Passenger Name: ").lower()
        matches = [r for r in self.reservations.values() if name in r.user.name.lower()]

        if not matches:
            print("\nNo reservations found.")
            return

        print(f"\nFound {len(matches)} reservation(s).\n")
        for reservation in matches:
            try:
                bus = self._get_bus(reservation.bus_id)
                reservation.display(bus)
            except BusNotFoundError:
                reservation.display()

    # -------------------------------------------------
    # Bus Occupancy Report (CLI)
    # -------------------------------------------------

    def bus_occupancy_report(self):
        try:
            bus_id = self._input("\nEnter Bus ID: ")
            bus = self._get_bus(bus_id)

            total = bus.total_seats
            reserved = len(bus.reserved_seats)
            available = len(bus.available_seats)
            occupancy = (reserved / total * 100) if total > 0 else 0.0

            print("\n" + "=" * 60)
            print(f"Bus ID       : {bus.bus_id}")
            print(f"Name         : {bus.name}")
            print(f"Type         : {bus.bus_type}")
            print(f"Route        : {bus.route}")
            print(f"Departure    : {bus.departure_display}")
            print(f"Arrival      : {bus.arrival_display}")
            print(f"Total Seats  : {total}")
            print(f"Reserved     : {reserved}")
            print(f"Available    : {available}")
            print(f"Occupancy    : {occupancy:.2f}%")
            print("=" * 60)

        except BusNotFoundError as e:
            print(f"\nError: {e}")

    # -------------------------------------------------
    # Daily Rollover
    # -------------------------------------------------

    def rollover_if_needed(self):
        if self.fm.file_exists_today():
            return

        latest_date = self.fm.latest_bus_date()
        if latest_date is None:
            return

        old_buses = self.fm.load_buses(latest_date)
        active_buses = {
            bus_id: bus
            for bus_id, bus in old_buses.items()
            if not bus.has_departed()
        }

        new_buses = BusGenerator.generate(
            existing_buses=active_buses,
            days_window=3
        )
        active_buses.update(new_buses)

        self.fm.save_buses(active_buses)
        self.buses = active_buses

    def _create_demo_bookings(self):
        reservation_counter = 1
        for bus in self.buses.values():
            # 35% buses remain completely empty
            if random.random() < 0.35:
                continue

            max_bookings = max(1, bus.total_seats // 10)
            booking_count = random.randint(1, max_bookings)
            available = bus.available_seats.copy()

            for _ in range(booking_count):
                if not available:
                    break

                group_size = random.randint(1, min(3, len(available)))
                chosen = random.sample(available, group_size)

                booking_id = f"PRE{reservation_counter:05d}"
                reservation_counter += 1

                user = User(
                    name=f"Customer {reservation_counter}",
                    phone=f"982200{reservation_counter:04d}",
                    email=f"customer{reservation_counter}@goaexpress.in"
                )

                for seat_no in chosen:
                    bus.get_seat(seat_no).reserve(user, booking_id)
                    available.remove(seat_no)

                reservation = Reservation(
                    booking_id=booking_id,
                    user=user,
                    bus_id=bus.bus_id,
                    seat_numbers=chosen,
                    booking_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    total_fare=len(chosen) * bus.fare,
                    payment_mode="UPI (GPay)",
                    payment_status="Confirmed (Paid)"
                )

                self.reservations[booking_id] = reservation