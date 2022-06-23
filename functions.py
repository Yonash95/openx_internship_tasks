import requests

booking_data = {'firstname': 'Jan',
                'lastname': 'Kowalski',
                'totalprice': 212,
                'depositpaid': True,
                'bookingdates': {'checkin': '2022-01-01', 'checkout': '2022-01-02'},
                'additionalneeds': 'dinner'}  # global variable for tests


def ping():
    """A simple health check endpoint to confirm whether the API is up and running."""
    response = requests.get("https://restful-booker.herokuapp.com/ping")
    return response


def get_bookingids(firstname="", lastname="", checkin="", checkout=""):
    """Returns the ids of all the bookings.
    Can take optional query strings to search and return a subset of booking ids """
    varlist = [firstname, lastname, checkin, checkout]
    url = "https://restful-booker.herokuapp.com/booking?"
    for i in varlist:
        if i:
            if i == firstname:
                url = url + "firstname=" + i + "&"
            if i == lastname:
                url = url + "lastname=" + i + "&"
            if i == checkin:
                url = url + "checkin=" + i + "&"
            if i == checkout:
                url = url + "checkout=" + i + "&"
    response = requests.get(url=url)
    return response


def get_booking(booking_id):
    """Returns a specific booking based upon the booking id provided"""
    response = requests.get(url=f"https://restful-booker.herokuapp.com/booking/{booking_id}")
    return response


def create_booking(update):
    """Creates a new booking in the API"""
    response = requests.post(url="https://restful-booker.herokuapp.com/booking", json=update)
    return response


def create_token(uname, passw):
    """Creates a new auth token to use for access to the PUT and DELETE /booking"""
    response = requests.post(url="https://restful-booker.herokuapp.com/auth",
                             data={"username": uname, "password": passw})
    return response


def update_booking(booking_id, update):
    """Updates a current booking"""
    response = requests.put(
        url=f"https://restful-booker.herokuapp.com/booking/{booking_id}",
        json=update,
        cookies={"token": create_token("admin", "password123").json()["token"]})
    return response


def partial_update(booking_id, update):
    """Updates a current booking with a partial payload"""
    response = requests.patch(
        url=f"https://restful-booker.herokuapp.com/booking/{booking_id}",
        json=update,
        cookies={"token": create_token("admin", "password123").json()["token"]})
    return response


def delete_booking(booking_id):
    """Deletes booking with given id"""
    response = requests.delete(
        url=f"https://restful-booker.herokuapp.com/booking/{booking_id}",
        cookies={"token": create_token("admin", "password123").json()["token"]})
    return response