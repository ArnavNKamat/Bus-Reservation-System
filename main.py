from services.reservation_system import (
    ReservationSystem
)


def print_menu():

    print("\n" + "=" * 50)

    print("      BUS RESERVATION SYSTEM")

    print("=" * 50)

    print("1. List Available Buses")

    print("2. Find Bus")

    print("3. View Seat Layout")

    print("4. Book Seats")

    print("5. View Reservation")

    print("6. Cancel Seats")

    print("7. List All Reservations")

    print("8. Search Reservation by Phone")

    print("9. Search Reservation by Name")

    print("10. Bus Occupancy Report")

    print("0. Exit")

    print("=" * 50)


def main():

    system = ReservationSystem()

    while True:

        print_menu()

        choice = input(
            "\nEnter choice: "
        ).strip()

        try:

            if choice == "1":

                system.list_buses()

            elif choice == "2":

                system.find_bus()

            elif choice == "3":

                system.view_seat_layout()

            elif choice == "4":

                system.book_seats()

            elif choice == "5":

                system.view_reservation()

            elif choice == "6":

                system.cancel_seats()

            elif choice == "7":

                system.list_reservations()

            elif choice == "8":

                system.search_by_phone()

            elif choice == "9":

                system.search_by_name()

            elif choice == "10":

                system.bus_occupancy_report()

            elif choice == "0":

                print(
                    "\nThank you for using "
                    "Bus Reservation System."
                )

                break

            else:

                print(
                    "\nInvalid choice."
                )

        except KeyboardInterrupt:

            print(
                "\n\nProgram interrupted."
            )

            break

        except Exception as e:

            print(
                f"\nUnexpected Error: {e}"
            )


if __name__ == "__main__":

    main()