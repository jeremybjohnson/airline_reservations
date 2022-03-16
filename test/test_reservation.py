from src.classes.search import Search
from src.classes.reservation import Reservation

import pytest


def test_initialize_reservation():
    """Tests the initialization of the class Reservation"""
    res = Reservation()
    res.total_cost = 0


def test_set_res(global_user1, global_search):
    """Tests creating first reservation
        Tests dec_avail_seats
        Tests verify_res_unique when no reservation exists
        Tests the calculation of total_cost"""
    user = global_user1
    search = global_search
    res = Reservation()
    res.reset_avail_seats(48)
    res.set_res(48, user.username, search.seats_requested)
    assert res.username == 'johndoe'
    assert res.flight_id == 48
    assert res.cost == 400
    assert res.avail_seats == 100
    assert res.seats_reserved == 2
    assert res.total_cost == 800
    
    """Test dec_avail_seats - 100 seats originally, 2 reserved above yields 98 seats"""
    query = res.query_avail_seats(48)
    assert query == [(98, )]

    """Reset avail_seats to 100 for flight 48"""
    res.reset_avail_seats(48)


def test_set_res_db_and_get_res_db(global_user1, global_search):
    """ Set up for testing """
    user = global_user1
    search = global_search
    res = Reservation()
    res.set_res(48, user.username, search.seats_requested)
    
    """execute set_res_db to add a reservation to the database"""
    res.set_res_db()

    """execute get_res_db to get to verify set_res_db was successful and get_res_db returns the reservation"""
    reservation = res.get_res_db(user.username)
    assert reservation == [(48, 'john', 'doe', 'DEF', 'DEF1234', 'IAH', 'WAS', 
                            '02/22/2022', '14:00', 2, '$800.00')]
    
    """Delete reservation to reset the database and reset number of seats"""
    res.delete_res(48, user.username, search.seats_requested)
    res.reset_avail_seats(48)


def test_verify_res_unique_reservation_already_exists(global_user1, global_search):
    """One reservation for flight 48 and global_user1 already exists. It is no longer unique for that user"""
    user = global_user1
    search = global_search
    res = Reservation()
    res.set_res(48, user.username, search.seats_requested)

    """execute set_res_db to add a reservation to the database"""
    res.set_res_db()

    """verify the reservation is not unique"""
    unique = res.verify_res_unique(48, user.username)
    assert unique == False
    
    """Delete reservation to reset the database and reset number of seats"""
    res.delete_res(48, user.username, search.seats_requested)
    res.reset_avail_seats(48)


def test_verify_res_unique_no_reservation_exists(global_user2):
    """"Reservation for flight 48 exists only for global_user1"""
    user2 = global_user2
    res = Reservation()
    unique = res.verify_res_unique(48, user2.username)
    assert unique == True
    

def test_delete_res_and_inc_avail_seats(global_user1, global_search):
    """Tests deleting a reservation from the reservations table
        tests increasing the number of avail_seats in the flights table by the number of seats_reserved"""
    user = global_user1
    search = global_search
    res = Reservation()
    res.set_res(48, user.username, search.seats_requested)
    
    """Reset avail_seats for flight 48"""
    res.reset_avail_seats(48)

    """execute set_res_db to add a reservation to the database"""
    res.set_res_db()
    """Delete the reservation"""
    res.delete_res(48, user.username, search.seats_requested)
    
    """Write test for checking reservations database for deleted reservation
        should return [] because only reservation made in testing was deleted"""
    res_return = res.get_res_db(user.username)
    assert res_return == []
    
    """Reset avail_seats for flight 48"""
    res.reset_avail_seats(48)

def test_inc_avail_seats():
    """Test that test_inc_avail_seats increases the total number of seats by 2
        100 original seats, 2 added yields 102"""
    res = Reservation()
    res.inc_avail_seats(48, 2)
    query = res.query_avail_seats(48)
    assert query == [(102, )]
    
    """Reset avail_seats for flight 48"""
    res.reset_avail_seats(48)


def test__only_logged_in_user_name_returns_in_query(global_user1, global_user2, global_search):
    """Set up 2 reservations. 1 for global_user1 and 1 for global_user2 on the different
        return query for global_user2 flight confirm global_user1 flight not returned."""
        
    """Set up global_user1 flight"""
    user = global_user1
    search = global_search
    res = Reservation()
    res.set_res(48, user.username, search.seats_requested)
    
    """Set up global_user2 flight"""
    user2 = global_user2
    user2.set_user_db()
    search2 = Search()
    search2.set_search(user2.username, 'IAH', 'SEA', '2022/02/22', 1)
    res2 = Reservation()
    res2.set_res(47, user2.username, search2.seats_requested)

    """execute set_res_db to add a reservations to the database"""
    res.set_res_db()
    res2.set_res_db()
    
    """Query the database for user2 flights """
    user2_query = res2.get_res_db(user2.username)
    assert user2_query == [(47, 'tom', 'brown', 'ABC', 'ABC1234', 'IAH',
                            'SEA', '02/22/2022', '14:00', 1, '$400.00')]
    
    """Delete reservations to reset the database and reset seat counts """
    res.delete_res(48, user.username, search.seats_requested)
    res2.delete_res(47, user2.username, search2.seats_requested)
    res2.reset_avail_seats(47)
    res.reset_avail_seats(48)


def test__multiple_reserved_flights_are_queried(global_user1, global_user2, global_search):
    """Set up 3 reservations. 2 for global_user1 and 1 for global_user2 on the different
        return query for global_user1 flight confirm 2 flights are returned and 
        global_user2 flight not returned."""

    """Set up global_user1 flight 1"""
    user = global_user1
    search = global_search
    res = Reservation()
    res.set_res(48, user.username, search.seats_requested)
    
    """Set up global_user1 flight 2"""
    user1 = global_user1
    search1 = Search()
    search1.set_search(user1.username, 'IAH', 'SEA', '2022/02/22', 1)
    res1 = Reservation()
    res1.set_res(47, user1.username, search1.seats_requested)
    
    """Set up global_user2 flight"""
    user2 = global_user2
    user2.set_user_db()
    search2 = Search()
    search2.set_search(user2.username, 'IAH', 'SEA', '2022/02/22', 1)
    res2 = Reservation()
    res2.set_res(47, user2.username, search2.seats_requested)

    """execute set_res_db to add a reservations to the database"""
    res.set_res_db()
    res1.set_res_db()
    res2.set_res_db()
    
    """Query the database for user2 flights """
    user1_query = res1.get_res_db(user1.username)
    assert user1_query == [(48, 'john', 'doe', 'DEF', 'DEF1234', 'IAH',
                            'WAS', '02/22/2022', '14:00', 2, '$800.00'),
                           (47, 'john', 'doe', 'ABC', 'ABC1234', 'IAH',
                            'SEA', '02/22/2022', '14:00', 1, '$400.00')]
    
    """Delete reservations to reset the database and reset seat counts"""
    res.delete_res(48, user.username, search.seats_requested)
    res1.delete_res(47, user.username, search1.seats_requested)
    res2.delete_res(47, user2.username, search2.seats_requested)
    res.reset_avail_seats(48)
    res1.reset_avail_seats(47)
