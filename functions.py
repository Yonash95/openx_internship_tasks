import requests
import json


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
            booking = {'firstname': input("First name: "),
                       'lastname': input("Last name: "),
                       'totalprice': int(input("Total price (digits): ")),
                       'depositpaid': bool(input("Deposit paid? (1) Yes, (0) No: ")),
                       'bookingdates': {'checkin': input("Checkin date (rrrr-mm-dd): "),
                                        'checkout': input("Checkout date (rrrr-mm-dd): ")},
                       'additionalneeds': input("Additional needs: ")}

            print(booking)
            return booking
        except ValueError:
            print("Bad data type entered")
            continue


def create_partial_update():
    """creates dictionary for partial update"""
    update = {}
    while True:
        try:
            print("What do you want to correct: ")
            menu = {"1.": "First name", "2.": "Last name", "3.": "Total price", "4.": "Deposit", "5.": "Checkin date",
                    "6.": "Checkout date", "7.": "Additional information", "0.": "Finalise"}
            option = menu.keys()
            for entry in option:
                print(entry, menu[entry])

            select = int(input("Select: "))
            if select == 0:
                break
            elif select == 1:
                update['firstname'] = input("New first name: ")
            elif select == 2:
                update['lastname'] = input("New Last name: ")
            elif select == 3:
                update['totalprice'] = int(input("New total price (digits)"))
            elif select == 4:
                update['depositpaid'] = bool(input("Deposit paid? (1) Yes, (0) No: "))
            elif select == 5 or 6:
                if 'bookingdates' not in update:
                    update['bookingdates'] = {}
                if select == 5:
                    update['bookingdates']['checkin'] = input("New checkin date (yyyy-mm-dd): ")
                elif select == 6:
                    update['bookingdates']['checkout'] = input("New checkout date (yyyy-mm-dd): ")
            print(update)

        except ValueError:
            print("Bad data type")
    return update


def filtered_list():
    filters = {}
    print("Select filters")
    menu = {"1.": "First name", "2.": "Last name", "3.": "Checkin date", "4.": "Checkout date", "0.": "Finalize"}
    option = menu.keys()
    for entry in option:
        print(entry, menu[entry])
    while True:
        select = int(input("Select: "))
        if select == 0:
            break
        elif select == 1:
            filters['firstname'] = input("First name: ")
        elif select == 2:
            filters['lastname'] = input("Last name ")
        elif select == 3:
            filters['checkin'] = input("Checkin date (yyyy-mm-dd): ")
        elif select == 4:
            filters['checkout'] = input("Checkout date (yyyy-mm-dd): ")
    booking_list = get_bookingids(filters)
    return booking_list.json()


def save_to_file():
    idlist = get_bookingids().json()
    for i in range(len(idlist)):
        idlist[i] = idlist[i]['bookingid']
    with open("booking_list.txt", "a") as bookingslist:
        for i in idlist[:10]:  # Only ten entries is saved because it takes a lot of time to save all ;)
            booking = get_booking(i).json()
            print(booking)
            bookingslist.write(json.dumps(booking))
        bookingslist.close()

