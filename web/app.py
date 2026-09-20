# web/app.py

import os
import sys
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

# Ensure root directory is in sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from models.user import User
from models.reservation import Reservation
from services.file_manager import FileManager
from services.reservation_system import ReservationSystem
from services.bus_generator import BusGenerator
from utils.constants import GOA_TOWNS, ALL_DESTINATIONS, OUTSTATION_CITIES, BUS_TYPES
from utils.exceptions import (
    BusNotFoundError,
    ReservationNotFoundError,
    SeatNotAvailableError,
    InvalidSeatError
)

# Ensure FileManager points to the root data directory
FileManager.DATA_FOLDER = os.path.join(ROOT_DIR, "data")

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "templates"),
    static_folder=os.path.join(os.path.dirname(__file__), "static")
)
CORS(app)

# Initialize the reservation system
reservation_system = ReservationSystem()


@app.route("/")
def index():
    """Render main web application interface."""
    return render_template("index.html")


@app.route("/api/locations", methods=["GET"])
def get_locations():
    """Return available source towns and destinations."""
    return jsonify({
        "success": True,
        "sources": GOA_TOWNS,
        "destinations": ALL_DESTINATIONS,
        "outstation": OUTSTATION_CITIES
    })


@app.route("/api/buses", methods=["GET"])
def get_buses():
    """List buses with optional filters for source, destination, date, and bus type."""
    # Perform rollover check if date changed
    reservation_system.rollover_if_needed()

    source = request.args.get("source", "").strip()
    destination = request.args.get("destination", "").strip()
    date = request.args.get("date", "").strip()
    bus_type = request.args.get("type", "").strip()

    visible = reservation_system.visible_buses()
    result = []

    for bus in visible.values():
        # Filter by source
        if source and bus.source.lower() != source.lower():
            continue
        # Filter by destination
        if destination and bus.destination.lower() != destination.lower():
            continue
        # Filter by date (YYYY-MM-DD)
        if date:
            dep_date = bus.departure_dt.split(" ")[0]
            if dep_date != date:
                continue
        # Filter by bus type (Seater / Sleeper)
        if bus_type and bus.bus_type.lower() != bus_type.lower():
            continue

        result.append({
            "bus_id": bus.bus_id,
            "name": bus.name,
            "source": bus.source,
            "destination": bus.destination,
            "route": bus.route,
            "departure_dt": bus.departure_dt,
            "arrival_dt": bus.arrival_dt,
            "departure_display": bus.departure_display,
            "arrival_display": bus.arrival_display,
            "fare": bus.fare,
            "bus_type": bus.bus_type,
            "total_seats": bus.total_seats,
            "available_seats_count": bus.available_seats_count,
            "reserved_seats_count": len(bus.reserved_seats)
        })

    # Sort by departure datetime
    result.sort(key=lambda x: x["departure_dt"])

    return jsonify({
        "success": True,
        "count": len(result),
        "buses": result
    })


@app.route("/api/buses/<bus_id>", methods=["GET"])
def get_bus_details(bus_id):
    """Get complete details and seat layout for a specific bus."""
    try:
        bus = reservation_system._get_bus(bus_id)
        seats_list = []
        for seat_no in range(1, bus.total_seats + 1):
            seat = bus.seats[seat_no]
            seats_list.append({
                "seat_number": seat.seat_number,
                "seat_type": seat.seat_type,
                "is_reserved": seat.is_reserved,
                "booking_id": seat.booking_id if seat.is_reserved else ""
            })

        return jsonify({
            "success": True,
            "bus": {
                "bus_id": bus.bus_id,
                "name": bus.name,
                "source": bus.source,
                "destination": bus.destination,
                "route": bus.route,
                "departure_dt": bus.departure_dt,
                "arrival_dt": bus.arrival_dt,
                "departure_display": bus.departure_display,
                "arrival_display": bus.arrival_display,
                "fare": bus.fare,
                "bus_type": bus.bus_type,
                "total_seats": bus.total_seats,
                "available_seats_count": bus.available_seats_count,
                "reserved_seats_count": len(bus.reserved_seats),
                "seats": seats_list
            }
        })
    except BusNotFoundError as e:
        return jsonify({"success": False, "error": str(e)}), 404


@app.route("/api/bookings", methods=["POST"])
def create_booking():
    """Book seats on a bus."""
    data = request.get_json() or {}
    bus_id = data.get("bus_id", "").strip()
    name = data.get("name", "").strip()
    phone = data.get("phone", "").strip()
    email = data.get("email", "").strip()
    seat_numbers = data.get("seats", [])

    if not bus_id:
        return jsonify({"success": False, "error": "Bus ID is required"}), 400
    if not name or not phone or not email:
        return jsonify({"success": False, "error": "Passenger name, phone, and email are required"}), 400
    if not seat_numbers:
        return jsonify({"success": False, "error": "At least one seat must be selected"}), 400

    try:
        # Convert seats to integers
        seat_numbers = [int(s) for s in seat_numbers]
    except ValueError:
        return jsonify({"success": False, "error": "Invalid seat numbers format"}), 400

    try:
        bus = reservation_system._get_bus(bus_id)

        # Validate all seats first
        for seat_no in seat_numbers:
            seat = bus.get_seat(seat_no)
            if seat.is_reserved:
                raise SeatNotAvailableError(f"Seat {seat_no} is already reserved.")

        booking_id = reservation_system._new_booking_id()
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
            total_fare=total_fare
        )

        reservation_system.reservations[booking_id] = reservation
        reservation_system.fm.save_buses(reservation_system.buses)
        reservation_system.fm.save_reservations(reservation_system.reservations)

        return jsonify({
            "success": True,
            "message": "Booking successful!",
            "reservation": reservation.to_dict(),
            "bus_details": {
                "name": bus.name,
                "route": bus.route,
                "departure_display": bus.departure_display,
                "arrival_display": bus.arrival_display,
                "bus_type": bus.bus_type
            }
        }), 201

    except (BusNotFoundError, InvalidSeatError, SeatNotAvailableError) as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": f"Unexpected error: {str(e)}"}), 500


@app.route("/api/reservations", methods=["GET"])
def list_reservations():
    """List all reservations."""
    result = []
    for res in reservation_system.reservations.values():
        bus_info = None
        if res.bus_id in reservation_system.buses:
            bus = reservation_system.buses[res.bus_id]
            bus_info = {
                "name": bus.name,
                "route": bus.route,
                "departure_display": bus.departure_display,
                "arrival_display": bus.arrival_display,
                "bus_type": bus.bus_type
            }

        res_dict = res.to_dict()
        res_dict["bus_info"] = bus_info
        result.append(res_dict)

    # Sort latest first
    result.sort(key=lambda x: x.get("booking_time", ""), reverse=True)

    return jsonify({
        "success": True,
        "count": len(result),
        "reservations": result
    })


@app.route("/api/reservations/<booking_id>", methods=["GET"])
def get_reservation(booking_id):
    """Get single reservation by ID."""
    try:
        res = reservation_system._get_reservation(booking_id)
        bus_info = None
        if res.bus_id in reservation_system.buses:
            bus = reservation_system.buses[res.bus_id]
            bus_info = {
                "name": bus.name,
                "route": bus.route,
                "departure_display": bus.departure_display,
                "arrival_display": bus.arrival_display,
                "bus_type": bus.bus_type
            }

        res_dict = res.to_dict()
        res_dict["bus_info"] = bus_info
        return jsonify({"success": True, "reservation": res_dict})
    except ReservationNotFoundError as e:
        return jsonify({"success": False, "error": str(e)}), 404


@app.route("/api/reservations/<booking_id>/cancel", methods=["POST"])
def cancel_reservation(booking_id):
    """Cancel specific seats or the entire reservation."""
    try:
        reservation = reservation_system._get_reservation(booking_id)
        bus = reservation_system._get_bus(reservation.bus_id)

        data = request.get_json() or {}
        seats_to_cancel = data.get("seats")

        if not seats_to_cancel:
            # Cancel all seats in this reservation
            seats_to_cancel = reservation.seat_numbers.copy()
        else:
            seats_to_cancel = [int(s) for s in seats_to_cancel]

        for seat_no in seats_to_cancel:
            if seat_no not in reservation.seat_numbers:
                raise ValueError(f"Seat {seat_no} is not part of this booking.")

        for seat_no in seats_to_cancel:
            bus.get_seat(seat_no).cancel()

        reservation.remove_seats(seats_to_cancel)
        reservation.total_fare = len(reservation.seat_numbers) * bus.fare

        removed_completely = False
        if not reservation.seat_numbers:
            del reservation_system.reservations[booking_id]
            removed_completely = True

        reservation_system.fm.save_buses(reservation_system.buses)
        reservation_system.fm.save_reservations(reservation_system.reservations)

        return jsonify({
            "success": True,
            "message": "Reservation cancelled completely." if removed_completely else "Selected seats cancelled successfully.",
            "removed_completely": removed_completely,
            "cancelled_seats": seats_to_cancel,
            "remaining_seats": reservation.seat_numbers if not removed_completely else [],
            "updated_fare": reservation.total_fare if not removed_completely else 0
        })

    except (ReservationNotFoundError, BusNotFoundError, ValueError) as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": f"Unexpected error: {str(e)}"}), 500


@app.route("/api/reservations/search", methods=["GET"])
def search_reservations():
    """Search reservations by phone number or passenger name."""
    phone = request.args.get("phone", "").strip()
    name = request.args.get("name", "").strip().lower()

    if not phone and not name:
        return jsonify({"success": False, "error": "Please provide a phone number or passenger name to search."}), 400

    matches = []
    for res in reservation_system.reservations.values():
        matched = False
        if phone and res.user.phone == phone:
            matched = True
        if name and name in res.user.name.lower():
            matched = True

        if matched:
            bus_info = None
            if res.bus_id in reservation_system.buses:
                bus = reservation_system.buses[res.bus_id]
                bus_info = {
                    "name": bus.name,
                    "route": bus.route,
                    "departure_display": bus.departure_display,
                    "arrival_display": bus.arrival_display,
                    "bus_type": bus.bus_type
                }
            res_dict = res.to_dict()
            res_dict["bus_info"] = bus_info
            matches.append(res_dict)

    return jsonify({
        "success": True,
        "count": len(matches),
        "reservations": matches
    })


@app.route("/api/reports/occupancy/<bus_id>", methods=["GET"])
def bus_occupancy_report(bus_id):
    """Get occupancy report for a specific bus."""
    try:
        bus = reservation_system._get_bus(bus_id)
        total = bus.total_seats
        reserved = len(bus.reserved_seats)
        available = len(bus.available_seats)
        occupancy = (reserved / total * 100) if total > 0 else 0.0

        return jsonify({
            "success": True,
            "report": {
                "bus_id": bus.bus_id,
                "name": bus.name,
                "bus_type": bus.bus_type,
                "route": bus.route,
                "departure_display": bus.departure_display,
                "arrival_display": bus.arrival_display,
                "total_seats": total,
                "reserved_seats_count": reserved,
                "available_seats_count": available,
                "occupancy_percentage": round(occupancy, 2),
                "reserved_seats": bus.reserved_seats,
                "available_seats": bus.available_seats
            }
        })
    except BusNotFoundError as e:
        return jsonify({"success": False, "error": str(e)}), 404


@app.route("/api/reports/all-occupancy", methods=["GET"])
def all_occupancy_reports():
    """Get occupancy reports for all current visible buses."""
    visible = reservation_system.visible_buses()
    reports = []
    for bus in visible.values():
        total = bus.total_seats
        reserved = len(bus.reserved_seats)
        available = len(bus.available_seats)
        occupancy = (reserved / total * 100) if total > 0 else 0.0
        reports.append({
            "bus_id": bus.bus_id,
            "name": bus.name,
            "bus_type": bus.bus_type,
            "route": bus.route,
            "departure_display": bus.departure_display,
            "arrival_display": bus.arrival_display,
            "total_seats": total,
            "reserved_seats_count": reserved,
            "available_seats_count": available,
            "occupancy_percentage": round(occupancy, 2)
        })

    reports.sort(key=lambda x: x["occupancy_percentage"], reverse=True)
    return jsonify({
        "success": True,
        "count": len(reports),
        "reports": reports
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
