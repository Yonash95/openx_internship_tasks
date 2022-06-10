import test_sample
# menu for app

def basic_menu():
    """Menu do obsługi bazy danych"""
    menu = {"1.": "Podaj listę rezerwacji", "2.": "Opis rezerwacji o wskazanym numerze", "3.": "Utwórz nową rezerwację",
            "4.": "Zaktualizuj wybraną rezerwację", "5.": "Popraw wpis", "6.": "Usuń wpis", "0.": "Zakończ"}
    while True:
        options = menu.keys()
        for entry in options:
            print(entry, menu[entry])
        select = int(input("Wybierz: "))
        if select == 0:
            break

        elif select == 1:  # lista rezerwacji
            print(test_sample.get_bookingids().json())

        elif select == 2:  # wpis do bazy o podanym id
            id = int(input("Podaj numer rezerwacji: "))
            print(test_sample.get_booking(id).json())

        elif select == 3:  # nowy wpis do bazy
            booking = booking_data()
            test_sample.create_booking(booking)
            new_booking = test_sample.get_bookingids(firstname=booking['firstname'])
            print("Numer nowej rezerwacji to: ", new_booking.json()[0]['bookingid'])

        elif select == 4:  # aktualizacja wpisu
            id = int(input("Podaj numer rezerwacji: "))
            booking = booking_data()
            test_sample.update_booking(id, booking)
            new_booking = test_sample.get_bookingids(firstname=booking['firstname'])
            print("Numer nowej rezerwacji to: ", new_booking.json()[0]['bookingid'])
        elif select == 5:
            id = int(input("Podaj numer rezerwacji: "))
            update = partial_update()
            print(update)
            test_sample.partial_update(id, update)
        elif select == 6:
            pass


def booking_data():
    booking = {'firstname': input("Imię: "),
                'lastname': input("Nazwisko: "),
                'totalprice': int(input("Cena: ")),
                'depositpaid': bool(input("Wpłacono kaucję? (1) Tak, (0) Nie: ")),
                'bookingdates': {'checkin': input("Data zameldowania (rrrr-mm-dd): "),
                                 'checkout': input("Data wymeldowania (rrrr-mm-dd): ")},
                'additionalneeds': input("Dodatkowe informacje: ")}
    print(booking)
    return booking


def update_data():
    update = {}
    booking = booking_data()
    for entry in booking:
        if booking[entry] != "":
            update[entry] = booking[entry]
    print(update)
    return update


def partial_update():
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
            update['totalprice'] = input("Nowa cena: ")
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
