import pytest
from src.classes.search import Search


def test_initialize_search():
    search = Search()
    assert search.username == ""
    assert search.depart_code == ""
    assert search.dest_code == ""
    assert search.depart_date == ""
    assert search.seats_requested == 0


def test_set_search(global_user1):
    user = global_user1
    search = Search()
    search.set_search(user.username, 'IAH', 'PDX', '2/16/2022', 2)
    assert search.username == "johndoe"
    assert search.depart_code == "IAH"
    assert search.dest_code == "PDX"
    assert search.depart_date == "2/16/2022"
    assert search.seats_requested == 2


def test_get_flights_db_no_seats_available(global_user1):
    """flight has 0 seats available"""
    user = global_user1
    search = Search()
    search.set_search(user.username, 'PDX', 'IAH', '2/22/2022', 1)
    flights = search.get_flights_db()
    assert flights == False


def test_get_flights_db_not_enough_seats_available(global_user1):
    """returns 1 flight because the other one only has 1 seat available"""
    user = global_user1
    search = Search()
    search.set_search(user.username, 'LAX', 'IAH', '2/22/2022', 2)
    avail_flights = [(42, 'United Airlines', 'UA3456', 'LAX', 'IAH', '02/22/2022', '14:00', '$400.00', 100)]
    flights = search.get_flights_db()
    assert flights == avail_flights


def test_get_flights_db_incorrect_data(global_user1):
    """Data entered is not in the database"""
    user = global_user1
    search = Search()
    search.set_search(user.username, 'ABC', 'XYZ', '2/20/2022', 2)
    flights = search.get_flights_db()
    assert flights == False


def test_get_flights_db_1_flight_available(global_user1):
    user = global_user1
    search = Search()
    search.set_search(user.username, 'IAH', 'SEA', '2022/2/22', 1)
    avail_flights = [(47, 'ABC', 'ABC1234', 'IAH', 'SEA', '02/22/2022', '14:00', '$400.00', 100)]
    flights = search.get_flights_db()
    assert flights == avail_flights


def test_get_flights_db_2_flight_available(global_user1):
    user = global_user1
    search = Search()
    search.set_search(user.username, 'SFO', 'IAH', '2/22/2022', 2)
    avail_flights = [(41, 'United Airlines', 'UA2345', 'SFO', 'IAH', '02/22/2022', '14:00', '$300.00', 90),
                     (44, 'American Airlines', 'AA2345', 'SFO', 'IAH', '02/22/2022', '14:00', '$300.00', 100)]
    flights = search.get_flights_db()
    assert flights == avail_flights
