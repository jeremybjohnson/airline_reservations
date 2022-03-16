import pytest
from src.classes.user import User
from src.classes.search import Search
from src.classes.reservation import Reservation
from src.classes.flight import Flight


def test_initialize_user():
    user = User()
    assert user.username == ''
    assert user.password == ''
    assert user.f_name == ''
    assert user.l_name == ''    


def test_set_user(global_user1):
    assert global_user1.username == 'johndoe'
    assert global_user1.password == '1234'
    assert global_user1.f_name == 'john'
    assert global_user1.l_name == 'doe'


def test_set_user_db(global_user1):
    """generate test setup for user1 to test the user functionality
        inserts user 1 data into the database
        method calls verify_username"""
    user = global_user1
    user.set_user_db()
    
    
def test_verify_username_user_already_exists(global_user2):
    """User already registered. Trying to register a second time """
    user = global_user2
    assert user.set_user_db() == False


def test_verify_username_user_does_not_exist():
    """User2 is not in the database, so the name should be unique
    verify_username yields true if the user is unique"""
    user = User()
    user.set_user('jackjohnson', '2345', 'Jack', 'Johnson')
    assert user.verify_username() == True


def test_login_username_password_match(global_user1):
    """Username and password match for user1
    also tests get_user_db"""
    user = global_user1
    assert user.login('johndoe', '1234') == True
    """Test get_user_db, called from successful login"""
    assert user.username == 'johndoe'
    assert user.f_name == 'john'
    assert user.l_name == 'doe'


def test_login_username_password_do_not_match(global_user1):
    """Username and password do not match for user1"""
    user = global_user1
    assert user.login('johndoe', '1235') == False
    
    
def test_login_username_does_not_exist():
    user = User()
    user.set_user('tomjones', '7890', 'tom', 'jones')
    assert user.login('tomejones', '7890') == False


def test_logout(global_user1, global_search):
    """Tests to see if user, search, res and show_res objects are initialized
        Should test to see if avail_flights and res_list are set to [] - test is failing"""
    user = global_user1
    search = global_search
    flight = Flight()
    #add flight
    flight.set_flight (48, 'DEF', 'DEF1234', 'IAH', 'WAS', '02/22/2022', '14:00', 400, 100, 100)  
    res = Reservation()
    res.set_res(flight.flight_id, user.username, search.seats_requested)
    user.logout(search, res, flight)
    """Assert user is initialized"""
    assert user.username == ''
    assert user.f_name == ''
    assert user.l_name == ''
    """Assert search is initialized"""
    assert search.username == ''
    assert search.depart_code == ''
    assert search.dest_code == ''
    assert search.depart_date == ''
    assert search.seats_requested == 0
    """Assert res is initialized"""
    assert res.username == ''
    assert res.f_name == ''
    assert res.l_name == ''
    assert res.flight_id == 0
    assert res.airline == ''
    assert res.flight_num == ''
    assert res.depart_date == ''
    assert res.dest_code == ''
    assert res.depart_date == ''
    assert res.depart_time == ''
    assert res.cost == 0
    assert res.avail_seats == 0
    assert res.seats_requested == 0
    assert res.total_cost == 0    
    """Assert flight is initialized"""        
    assert flight.flight_id == 0
    assert flight.airline == ""
    assert flight.flight_num == ""
    assert flight.depart_code == ""
    assert flight.dest_code == ""
    assert flight.depart_date == ""
    assert flight.depart_time == ""
    assert flight.cost == 0
    assert flight.avail_seats == 0
    assert flight.avail_flights == []
    """Assert lists are empty"""
    """Reset avail_seats for flight 48"""
    res.reset_avail_seats(flight.flight_id)

    
def test_delete_user_existing_user():
    user = User()
    user.set_user('a', 'a', 'a', 'a')
    add_user = user.set_user_db()
    user.delete_user(user.username)
    assert user.login(user.username, user.password) == False


def test_update_user_existing_user():
    user = User()
    user.set_user('a', 'a', 'a', 'a')
    add_user = user.set_user_db()
    user.update_user('a', 'b', 'b', 'b')
    user.get_user_db(user.username)
    password = user.get_password(user.username)
    assert user.f_name == 'b'
    assert user.l_name == 'b'
    assert password == [('b', )]
    user.delete_user(user.username)

