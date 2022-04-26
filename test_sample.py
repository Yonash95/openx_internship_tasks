import requests


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
        print(i)
        if i:
            if i == firstname:
                url = url + "firstname=" + i + "&"
            if i == lastname:
                url = url + "lastname=" + i + "&"
            if i == checkin:
                url = url + "checkin=" + i + "&"
            if i == checkout:
                url = url + "checkout=" + i + "&"

    print(url)
    response = requests.get(url=url.format())
    return response


def get_booking(booking_id):
    """Returns a specific booking based upon the booking id provided"""
    response = requests.get(url="https://restful-booker.herokuapp.com/booking/{}".format(booking_id))
    return response


def create_booking(fname, lname, tprice, dpaid, indate, outdate, add=""):
    """Creates a new booking in the API"""
    response = requests.post(url="https://restful-booker.herokuapp.com/booking", json={
        "firstname": fname,
        "lastname": lname,
        "totalprice": tprice,
        "depositpaid": dpaid,
        "bookingdates": {
            "checkin": indate,
            "checkout": outdate
        },
        "additionalneeds": add
    },
                             )
    return response


def create_token(uname, passw):
    """Creates a new auth token to use for access to the PUT and DELETE /booking"""
    response = requests.post(url="https://restful-booker.herokuapp.com/auth",
                             data={"username": uname, "password": passw})
    return response


def update_booking(booking_id, fname, lname, tprice, dpaid, indate, outdate, add=""):
    response = requests.put(
        url="https://restful-booker.herokuapp.com/booking/{}".format(booking_id),
        json={
            "firstname": fname,
            "lastname": lname,
            "totalprice": tprice,
            "depositpaid": dpaid,
            "bookingdates": {
                "checkin": indate,
                "checkout": outdate
            },
            "additionalneeds": add
        }, cookies={"token": create_token("admin", "password123").json()["token"]})
    return response


'''def partial_update(booking_id, firstname="", lastname="", totalprice="", depositpaid="", checkin="", checkout="", additionalneeds=""):
    """Updates a current booking with a partial payload"""
    arg_list = [booking_id, firstname, lastname, totalprice, depositpaid, checkin, checkout, additionalneeds]
    narg_list = []
    booking = get_booking(booking_id)
    for i,j in enumerate(arg_list):
        if i:
            narg_list.append(j)
        else:
            narg_list.append(booking[i])
    response = requests.patch(
        url="https://restful-booker.herokuapp.com/booking/{}".format(booking_id),
        json={"firstname": firstname,
              "lastname": lastname,
              "totalprice": totalprice,
              "depositpaid": depositpaid,
              "bookingdates": {
                  "checkin": checkin,
                  "checkout": checkout
              },
              "additionalneeds": additionalneeds
              }, cookies={"token": create_token("admin", "password123").json()["token"]})
    return response
'''


def delete_booking(booking_id):
    """Deletes booking with given id"""
    response = requests.delete(
        url="https://restful-booker.herokuapp.com/booking/{}".format(booking_id),
        cookies={"token": create_token("admin", "password123").json()["token"]})
    return response


class Tests:
    def test_ping(self):
        """healthcheck test"""
        assert ping().status_code == 201

    def test_get_bookingids(self):
        """get_bookingids test without arguments"""
        assert get_bookingids().status_code == 200

    def test_get_bookingids_fname(self):
        """get_bookingids test with one argument"""
        create_booking("Jan", "Kowalski", 212, True, "2022-01-01", "2022-01-02", "dinner")
        assert get_bookingids(firstname="Jan").status_code == 200

    def test_get_bookingids_fandlname(self):
        """get_bookingids test with two arguments"""
        create_booking("Jan", "Kowalski", 212, True, "2022-01-01", "2022-01-02", "dinner")
        assert get_bookingids(firstname="Jan", lastname="Kowalski").status_code == 200

    def test_get_bookingids_fname_empty(self):
        """get_bookingids test with empty firstname value"""
        create_booking("Jan", "Kowalski", 212, True, "2022-01-01", "2022-01-02", "dinner")
        assert get_bookingids(firstname="").status_code == 200

    def test_get_bookingids_checkin(self):
        """get_bookingids test with checkin value greater than in argument"""
        create_booking("Jan", "Kowalski", 212, True, "2022-01-01", "2022-01-02", "dinner")
        assert get_bookingids(checkin="2021-01-01").status_code == 200

    def test_get_bookingids_checkin_year(self):
        """get_bookingids test with only year in checkin value"""
        create_booking("Jan", "Kowalski", 212, True, "2022-01-01", "2022-01-02", "dinner")
        assert get_bookingids(checkin="2021").status_code == 200

    def test_get_bookingids_checkin_incorrect(self):
        """get_bookingids test with incorrect checkin value"""
        create_booking("Jan", "Kowalski", 212, True, "2022-01-01", "2022-01-02", "dinner")
        assert get_bookingids(checkin="20").status_code == 500

    def test_get_bookingids_checkin_empty(self):
        """get_bookingids test with empty checkin value"""
        create_booking("Jan", "Kowalski", 212, True, "2022-01-01", "2022-01-02", "dinner")
        assert get_bookingids(checkin="").status_code == 200

    def test_get_bookings_id(self):
        """get_booking with correct id value"""
        booking = get_bookingids().json()[0]['bookingid']
        assert get_booking(booking).status_code == 200

    def test_get_bookings_badid(self):
        """get_booking with incorrect id value"""
        assert get_booking(0).status_code == 404

    def test_create_booking_correct_value(self):
        """create_booking with correct values"""
        assert create_booking("Jan", "Kowalski", 212, True, "2022-01-01", "2022-01-02", "dinner").status_code == 200

    def test_create_booking_no_additional(self):
        """create_booking with correct values without key 'additionalneeds' """
        assert create_booking("Jan", "Kowalski", 212, True, "2022-01-01", "2022-01-02").status_code == 200

    def test_create_booking_incorrect_value(self):
        """create_booking with incorrect 'firstname' type"""
        assert create_booking(1, "Kowalski", 212, True, "2022-01-01", "2022-01-02", "elo").status_code == 500

    def test_create_booking_empty_value(self):
        """create_booking with incorrect 'firstname' type"""
        assert create_booking(None, "Kowalski", 212, True, "2022-01-01", "2022-01-02", "elo").status_code == 500

    def test_create_token_correct(self):
        """create_token with correct admin and password values"""
        assert create_token("admin", "password123").status_code == 200

    def test_create_token_incorrect(self):
        """create_token with incorrect admin and password values"""
        assert create_token("admi", "assword123").json() == {'reason': 'Bad credentials'}

    def test_create_token_empty(self):
        """create_token with empty admin and password values"""
        assert create_token("", "").json() == {'reason': 'Bad credentials'}

    def test_update_booking_correct(self):
        """update_booking with correct values"""
        booking = create_booking("Jan", "Kowalski", 212, True, "2022-01-01", "2022-01-02").json()['bookingid']
        assert update_booking(booking, "Henry", "Kowalski", 212, True, "2020-02-03", "2021-03-04",
                              "no bed").status_code == 200

    def test_update_booking_incorrect_id(self):
        """update_booking with incorrect id"""
        assert update_booking(0, "Henry", "Kowalski", 212, True, "2020-02-03", "2021-03-04",
                              "no bed").status_code == 405

    def test_update_booking_incorrect_values(self):
        """update_booking with incorrect values"""
        booking = create_booking("Jan", "Kowalski", 212, True, "2022-01-01", "2022-01-02").json()['bookingid']
        assert update_booking(booking, "Henry", True, 212, "jam", "2020-02-03", "2021-03-04", "no bed").status_code == 500

    def test_delete_booking(self):
        """delete_booking with correct id"""
        booking = create_booking("Jan", "Kowalski", 212, True, "2022-01-01", "2022-01-02").json()['bookingid']
        assert delete_booking(booking).status_code == 201

    def test_delete_booking_incorrect_id(self):
        """delete_booking with incorrect id"""
        assert delete_booking(0).status_code == 405


'''    def test_partial_update_booking_correct(self):
        """partial_update with correct values"""
        assert partial_update(booking_id=1, fname="Harry").status_code == 200'''
