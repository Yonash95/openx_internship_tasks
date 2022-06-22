import test_sample


def basic_menu():
    """Menu for whole program"""
    menu = {"1.": "Podaj listę rezerwacji", "2.": "Opis rezerwacji o wskazanym numerze", "3.": "Utwórz nową rezerwację",
            "4.": "Zaktualizuj wybraną rezerwację", "5.": "Popraw wpis", "6.": "Usuń wpis", "0.": "Zakończ"}
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
            print(test_sample.get_bookingids().json())

        elif select == 2:  # database query
            try:
                booking_id = int(input("Podaj numer rezerwacji: "))
                print(test_sample.get_booking(booking_id).json())
            except Exception:
                print("Nie ma rezerwacji o takim numerze")
                continue

        elif select == 3:  # new database entry
            booking = booking_data()
            test_sample.create_booking(booking)
            new_booking = test_sample.get_bookingids(firstname=booking['firstname'])
            print("Numer nowej rezerwacji to: ", new_booking.json()[0]['bookingid'])

        elif select == 4:  # whole entry update
            booking_id = int(input("Podaj numer rezerwacji: "))
            booking = booking_data()
            test_sample.update_booking(booking_id, booking)
            new_booking = test_sample.get_bookingids(firstname=booking['firstname'])
            print("Numer nowej rezerwacji to: ", new_booking.json()[0]['bookingid'])

        elif select == 5:  # partial entry update
            booking_id = int(input("Podaj numer rezerwacji: "))
            update = partial_update()
            print(update)
            test_sample.partial_update(booking_id, update)

        elif select == 6:  # delete entry from data base
            booking_id = int(input("Podaj numer rezerwacji: "))
            test_sample.delete_booking(booking_id)


def booking_data():
    """creates dictionary with booking data for create and update functionality"""
    while True:
        try:
            booking = {'firstname': input("Imię: "),
                       'lastname': input("Nazwisko: "),
                       'totalprice': int(input("Cena (cyfry): ")),
                       'depositpaid': bool(input("Wpłacono kaucję? (1) Tak, (0) Nie: ")),
                       'bookingdates': {'checkin': input("Data zameldowania (rrrr-mm-dd): "),
                                        'checkout': input("Data wymeldowania (rrrr-mm-dd): ")},
                       'additionalneeds': input("Dodatkowe informacje: ")}

            print(booking)
            return booking
        except ValueError:
            print("Podano zły typ")
            continue




def partial_update():
    """creates dictionary for partial update"""
    update = {}
    loop = True
    while loop is True:
        print("Co chcesz poprawić?: ")
        partial_update_menu = {"1.": "Imię", "2.": "Nazwisko", "3.": "Cenę", "4.": "Kaucja", "5.": "Data zameldowania",
                               "6.": "Data wymeldowania", "7.": "Dodatkowe informacje", "0.": "Już wszstko"}
        option = partial_update_menu.keys()
        for entry in option:
            print(entry, partial_update_menu[entry])

        select = int(input("Wybierz: "))
        if select == 0:
            break
        elif select == 1:
            update['firstname'] = input("Nowe imię: ")
        elif select == 2:
            update['lastname'] = input("Nowe nazwisko: ")
        elif select == 3:
            update['totalprice'] = int(input("Nowa cena: "))
        elif select == 4:
            update['depositpaid'] = bool(input("Wpłacono kaucję? (1) Tak, (0) Nie: "))
        elif select == 5 or 6:
            if 'bookingdates' not in update:
                update['bookingdates'] = {}
            if select == 5:
                update['bookingdates']['checkin'] = input("Nowa data zamelodwania (rrrr-mm-dd): ")
            elif select == 6:
                update['bookingdates']['checkout'] = input("Nowa data wymeldowania (rrrr-mm-dd): ")
        print(update)
    return update


basic_menu()
