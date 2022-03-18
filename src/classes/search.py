from src.classes.database import Database


class Search(Database):    
    def __init__(self):
        super().__init__()
        self.username = ""
        self.depart_code = ""
        self.dest_code = ""
        self.depart_date = ""
        self.seats_requested = 0


    def set_search(self, username, depart_code, dest_code, depart_date, seats_requested):
        self.username = username
        self.depart_code = depart_code
        self.dest_code = dest_code
        self.depart_date = depart_date
        self.seats_requested = seats_requested


    def get_flights_db(self):
        """Method sends sql statement to query the flights table and returns false or a list of flights"""
        sql = """SELECT flight_id, airline, flight_number, depart_code, dest_code, 
                TO_CHAR(depart_date, 'MM/DD/YYYY'), TO_CHAR(depart_time, 'HH24:MI'), cost::numeric::money, avail_seats
                FROM flights
                WHERE depart_code = '%s' 
                AND dest_code = '%s'
                AND depart_date = '%s'
                AND avail_seats >= '%s'
                 """ % (
            self.depart_code,
            self.dest_code,
            self.depart_date,
            self.seats_requested,
        )
        avail_flights = self.execute_sql(sql)
        if avail_flights == []:
            return False
        else:
            return avail_flights
