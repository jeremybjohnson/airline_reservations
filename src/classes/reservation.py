from src.classes.user import User
from src.classes.flight import Flight
from src.classes.search import Search


class Reservation(User, Flight, Search):
    def __init__(self):
        super().__init__()
        self.total_cost = 0

    
    def set_res(self, flight_id, username, seats_requested):
        """Verify this flight is not already reserved"""
        unique = self.verify_res_unique(flight_id, username)
        """Create the reservation"""
        if unique == True:
            sql = """ SELECT cost, avail_seats
                    FROM flights 
                    WHERE flight_id = '%s'
                    AND avail_seats >= '%s'        
                    """ % (flight_id, seats_requested)
            sql_query = self.execute_sql(sql)
            self.username = username
            self.flight_id = flight_id
            self.cost = sql_query[0][0]
            self.avail_seats = sql_query[0][1]
            self.seats_reserved = seats_requested
            self.total_cost = self.cost * self.seats_reserved
            try:
                self.dec_avail_seats()
            except Exception as e:
                print("There was an error updating the flights table", e)
        else:
            return False
    
    
    def verify_res_unique(self, flight_id, username):
        sql = """SELECT * FROM reservations 
                WHERE flight_id = '%s'
                AND username = '%s'""" % (flight_id, username)
        res_return = self.execute_sql(sql)
        if res_return == []:
            return True
        else:
            return False

    def dec_avail_seats(self):
        """Method sends SQL to decrease the avail_flights by the reserved amount in the flights table - 
            uses flight_id as the query parameter"""
        seats_avail = self.avail_seats - self.seats_reserved
        sql = """ UPDATE flights
                SET avail_seats = '%s'
                WHERE flight_id = '%s'
                """ % (
            seats_avail,
            self.flight_id,
        )
        self.execute_sql(sql, update=True)


    def set_res_db(self):
        """Method sends SQL to update the reservations table for the highlighted available flight"""
        try:
            sql = """INSERT INTO reservations (flight_id, username, total_cost, reserved_seats)
                    VALUES ('%s', '%s','%s','%s')
                    """ % (self.flight_id, self.username, self.total_cost, self.seats_reserved)
            self.execute_sql(sql, update=True)
            return True
        except Exception as e:
            print("Error updating the reservations table", e)
            return False

    def get_res_db(self, username):
        """Gets the reservation information from reservations, flights and users tables.
        Queries on username. Returns a list of flight data for all flights reserved"""
        sql = """SELECT f.flight_id, u.f_name, u.l_name, f.airline, f.flight_number, 
                f.depart_code, f.dest_code, TO_CHAR(f.depart_date, 'MM/DD/YYYY'), 
                TO_CHAR(f.depart_time, 'HH24:MI'), r.reserved_seats, r.total_cost::numeric::money
                FROM reservations r
                JOIN flights f
                ON r.flight_id = f.flight_id
                JOIN users u 
                ON r.username = u.username
                WHERE u.username = '%s'     
                """ % (username)
        res_list = self.execute_sql(sql)
        return res_list

    """Below are for reservation cancellation """

    def delete_res(self, flight_id, username, seats_reserved):
        """Method deletes reservation from reservations table"""
        try:
            # delete reservation from reservation database
            sql = """ DELETE FROM reservations
                    WHERE username = '%s'
                    AND flight_id = '%s'
                    """ % (
                username,
                flight_id,
            )
            self.execute_sql(sql, update=True)
            # increase seats in flights table by seats_reserved amount
            self.inc_avail_seats(flight_id, seats_reserved)
        except Exception as e:
            print("Error deleting reservation ", e)

    def inc_avail_seats(self, flight_id, seats_reserved):
        """Increases avail_seats in the flights table by the number of seats_reserved in the reservations table"""
        # calculate the new avail_seats amount
        sql = """ SELECT avail_seats
                FROM flights
                WHERE flight_id = '%s'
                """ % (
            flight_id
        )
        avail_seats = self.execute_sql(sql)
        for flights in avail_seats:
            for data in flights:
                seats = data
        seats_avail = seats + seats_reserved
        # update flights database to the new avail_seats amount
        try:
            sql = """UPDATE flights
                    SET avail_seats = '%s'
                    WHERE flight_id = '%s'
                    """ % (
                seats_avail,
                flight_id,
            )
            self.execute_sql(sql, update=True)
            return None
        except Exception as e:
            print("Error updating flights table", e)

    """ Methods for testing purposes only """

    def reset_avail_seats(self, flight_id):
        """For testing purpose only, resets the avail_seats to 100 avail_seats"""
        sql = """UPDATE flights
                SET avail_seats = '%s'
                WHERE flight_id = '%s'""" % (100, flight_id)
        self.execute_sql(sql, update=True)


    def query_avail_seats(self, flight_id):
        """for testing purposes only, queries avail_seats from the flights db """
        sql = """SELECT avail_seats FROM flights WHERE flight_id = '%s'""" % (
            flight_id)
        query = self.execute_sql(sql)
        return query
