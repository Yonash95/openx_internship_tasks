import test_sample
# menu for app

def basic_menu():
    """Menu do obsługi bazy danych"""
    menu = {"1.": "Podaj listę rezerwacji", "2.": "Opis rezerwacji o wskazanym numerze", "3.": "Utwórz nową rezerwację",
            "4.": "Zaktualizuj wybraną rezerwację", "5.": "Popraw wpis", "6.": "Usuń wpis"}
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
            booking = update_data()
            test_sample.partial_update(id, booking)
        elif select == 6:
            pass


def booking_data():
    booking = {'firstname': input("Imię: "),
                'lastname': input("Nazwisko: "),
                'totalprice': int(input("Cena: ")),
                'depositpaid': bool(input("Wpłacono kaucję? (1) Tak, (0) Nie")),
                'bookingdates': {'checkin': input("Data zameldowania (rrrr-mm-dd): "),
                                 'checkout': input("Data wymeldowania (rrrr-mm-dd): ")},
                'additionalneeds': input("Dodatkowe informacje: ")}
    print(booking)
    return booking


def update_data():
    update = {}
    booking = booking_data()
    for entry in booking:
        if booking['entry'] is not "":
            update['entry'] = booking['entry']
    print(update)
    return update



basic_menu()