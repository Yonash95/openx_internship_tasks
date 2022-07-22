import requests
import json
# import datetime
# import pathlib
import pandas as pd


def ping():
    """A simple health check endpoint to confirm whether the API is up and running."""
    response = requests.get("https://restful-booker.herokuapp.com/ping")
    return response


def get_bookingids(filter_dict=None):
    """Returns the ids of all the bookings.
    Can take optional query strings to search and return a subset of booking ids """
    url = "https://restful-booker.herokuapp.com/booking?"
    if filter_dict:
        keys = list(filter_dict.keys())
        for entry in keys:
            url = url + entry + "=" + filter_dict[entry] + "&"
    response = requests.get(url=url)
    booking_list = [response.json()[x]['bookingid'] for x in range(len(response.json()))]
    return booking_list


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
    """allow to create filters for easier search of bookings"""
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
    return booking_list


def save_to_file():
    """saves first 10 bookings to file, just for practice"""
    id_list = get_bookingids()
    with open("booking_list.json", "w") as bookings_list:
        booking = []
        i = 0
        for j in id_list[:10]:  # loop in place of list comprehension so we can ad id to each booking
            booking.append(get_booking(j).json())
            booking[i]['id'] = j
            i += 1
        bookings_list.write(json.dumps(booking))
        bookings_list.close()
    return bookings_list


def archive_saved_file():
    """makes a archive of booking_list file saved in save_to_file function"""
    pass
    """with open("booking_list.json") as booking_list:
        file_pattern = ".json"
        main_dir = "archive"
        date_string = datetime.date.today().strftime("%Y-%m-%d")
        cur_path = pathlib.Path(".")
        paths = cur_path.glob(file_pattern)
        for path in paths:
            new_filename = f"{path.stem}_{date_string}.{path.suffix}"
            new_path = cur_path.joinpath(main_dir, new_filename)
            path.rename(new_path)"""


def load_pandas():
    df = pd.read_json('booking_list.json')
    df = df[['id'] + [col for col in df.columns if col != 'id']]  # id on first place
    print(df.to_string())
