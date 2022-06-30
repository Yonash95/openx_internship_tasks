import functions


def basic_menu():
    """Menu for whole program"""
    menu = {"1.": "Booking list", "2.": "Booking description", "3.": "Create new booking",
            "4.": "Update booking", "5.": "Correct booking", "6.": "Delete booking",
            "7.": "Save booking list to file (absent from current version)", "0.": "End"}
    while True:
        options = menu.keys()
        for entry in options:
            print(entry, menu[entry])
        try:
            select = int(input("Select: "))
        except ValueError:
            print("It must be a number")
            continue
        if select == 0:
            break

        elif select == 1:  # reservations list
            print("1. Whole list \n2. Filter")
            sub_select = int(input("Select: "))
            if sub_select == 1:  # all reservations
                lista = functions.get_bookingids().json()
                print(lista)
                print("Number of all bookings: ", len(lista))
            else:  # specified reservations
                lista = functions.filtered_list()
                print(lista)
                print("Number of filtered bookings : ", len(lista))

        elif select == 2:  # database query
            try:
                booking_id = int(input("Enter booking id: "))
                print(functions.get_booking(booking_id).json())
            except Exception:
                print("No booking with this id")
                continue

        elif select == 3:  # new database entry
            booking = functions.create_booking_data()
            functions.create_booking(booking)
            new_booking = functions.get_bookingids(firstname=booking['firstname'])
            print(" Id of new booking: ", new_booking.json()[0]['bookingid'])

        elif select == 4:  # whole entry update
            booking_id = int(input("Enter booking id: "))
            booking = functions.create_booking_data()
            functions.update_booking(booking_id, booking)

        elif select == 5:  # partial entry update
            booking_id = int(input("Enter booking id: "))
            functions.partial_update(booking_id)

        elif select == 6:  # delete entry from data base
            booking_id = int(input("Enter booking number: "))
            functions.delete_booking(booking_id)


basic_menu()
