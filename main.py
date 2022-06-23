import functions


def basic_menu():
    """Menu for whole program"""
    menu = {"1.": "Podaj listę rezerwacji", "2.": "Opis rezerwacji o wskazanym numerze", "3.": "Utwórz nową rezerwację",
            "4.": "Zaktualizuj wybraną rezerwację", "5.": "Popraw wpis", "6.": "Usuń wpis",
            "7.": "Zapisz listę rezerwacji", "0.": "Zakończ"}
    while True:
        options = menu.keys()
        for entry in options:
            print(entry, menu[entry])
        try:
            select = int(input("Wybierz: "))
        except ValueError:
            print("Musisz podać cyfrę")
            continue
        if select == 0:
            break

        elif select == 1:  # reservations list
            print("1. Cała lista \n2. Filtruj")
            sub_select = int(input("Wybierz: "))
            if sub_select == 1:  # all reservations
                lista = functions.get_bookingids().json()
                print(lista)
                print("Liczba wszystkich rezerwacji: ", len(lista))
            else:  # specified reservations
                lista = functions.filtered_list()
                print(lista)
                print("Liczba poszukiwanych rezerwacji: ", len(lista))

        elif select == 2:  # database query
            try:
                booking_id = int(input("Podaj numer rezerwacji: "))
                print(functions.get_booking(booking_id).json())
            except Exception:
                print("Nie ma rezerwacji o takim numerze")
                continue

        elif select == 3:  # new database entry
            booking = functions.create_booking_data()
            functions.create_booking(booking)
            new_booking = functions.get_bookingids(firstname=booking['firstname'])
            print("Numer nowej rezerwacji to: ", new_booking.json()[0]['bookingid'])

        elif select == 4:  # whole entry update
            booking_id = int(input("Podaj numer rezerwacji: "))
            booking = functions.create_booking_data()
            functions.update_booking(booking_id, booking)

        elif select == 5:  # partial entry update
            booking_id = int(input("Podaj numer rezerwacji: "))
            functions.partial_update(booking_id)

        elif select == 6:  # delete entry from data base
            booking_id = int(input("Podaj numer rezerwacji: "))
            functions.delete_booking(booking_id)


basic_menu()
