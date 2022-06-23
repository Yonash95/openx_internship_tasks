import requests


def ping():
    """A simple health check endpoint to confirm whether the API is up and running."""
    response = requests.get("https://restful-booker.herokuapp.com/ping")
    return response


def get_bookingids(filter_dict=""):
    """Returns the ids of all the bookings.
    Can take optional query strings to search and return a subset of booking ids """
    url = "https://restful-booker.herokuapp.com/booking?"
    if filter_dict:
        keys = list(filter_dict.keys())
        for entry in keys:
            url = url + entry + "=" + filter_dict[entry] + "&"
    response = requests.get(url=url)
    return response


def get_booking(booking_id):
    """Returns a specific booking based upon the booking id provided"""
    response = requests.get(url=f"https://restful-booker.herokuapp.com/booking/{booking_id}")
    return response


def create_booking(new_booking_data):
    """Creates a new booking in the API"""
    response = requests.post(url="https://restful-booker.herokuapp.com/booking", json=new_booking_data)
    return response


def create_token(username, password):
    """Creates a new auth token to use for access to the PUT and DELETE /booking"""
    response = requests.post(url="https://restful-booker.herokuapp.com/auth",
                             data={"username": username, "password": password})
    return response


def update_booking(booking_id, update):
    """Updates a current booking"""
    response = requests.put(
        url=f"https://restful-booker.herokuapp.com/booking/{booking_id}",
        json=update,
        cookies={"token": create_token("admin", "password123").json()["token"]})
    return response


def partial_update(booking_id):
    """Updates a current booking with a partial payload"""
    response = requests.patch(
        url=f"https://restful-booker.herokuapp.com/booking/{booking_id}",
        json=create_partial_update(),
        cookies={"token": create_token("admin", "password123").json()["token"]})
    return response


def delete_booking(booking_id):
    """Deletes booking with given id"""
    response = requests.delete(
        url=f"https://restful-booker.herokuapp.com/booking/{booking_id}",
        cookies={"token": create_token("admin", "password123").json()["token"]})
    return response


def create_booking_data():
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
            print("Podano zły typ danych, patrz nawiasy")
            continue


def create_partial_update():
    """creates dictionary for partial update"""
    update = {}
    while True:
        try:
            print("Co chcesz poprawić?: ")
            menu = {"1.": "Imię", "2.": "Nazwisko", "3.": "Cenę", "4.": "Kaucja", "5.": "Data zameldowania",
                    "6.": "Data wymeldowania", "7.": "Dodatkowe informacje", "0.": "Już wszstko"}
            option = menu.keys()
            for entry in option:
                print(entry, menu[entry])

            select = int(input("Wybierz: "))
            if select == 0:
                break
            elif select == 1:
                update['firstname'] = input("Nowe imię: ")
            elif select == 2:
                update['lastname'] = input("Nowe nazwisko: ")
            elif select == 3:
                update['totalprice'] = int(input("Nowa cena (cyfry): "))
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

        except ValueError:
            print("Podano zły typ danych, patrz nawiasy")
    return update


def filtered_list():
    filters = {}
    print("Po czym chcesz wyszukiwać")
    menu = {"1.": "Imię", "2.": "Nazwisko", "3.": "Data zameldowania", "4.": "Data wymeldowania", "0.": "Zakończ"}
    option = menu.keys()
    for entry in option:
        print(entry, menu[entry])
    while True:
        select = int(input("Wybierz: "))
        if select == 0:
            break
        elif select == 1:
            filters['firstname'] = input("Imię: ")
        elif select == 2:
            filters['lastname'] = input("Nazwisko: ")
        elif select == 3:
            filters['checkin'] = input("Data zamelodwania (rrrr-mm-dd): ")
        elif select == 4:
            filters['checkout'] = input("Data wymeldowania (rrrr-mm-dd): ")
    booking_list = get_bookingids(filters)
    return booking_list.json()
