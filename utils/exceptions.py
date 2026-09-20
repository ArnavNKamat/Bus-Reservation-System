# utils/exceptions.py

class SeatNotAvailableError(Exception):
    """Raised when a seat is already reserved."""
    pass


class InvalidSeatError(Exception):
    """Raised when a seat number does not exist."""
    pass


class ReservationNotFoundError(Exception):
    """Raised when a booking ID cannot be found."""
    pass


class BusNotFoundError(Exception):
    """Raised when a bus ID cannot be found."""
    pass