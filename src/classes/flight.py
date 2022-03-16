from src.classes.database import Database


class Flight(Database):    
    def __init__(self):
        super().__init__()
        self.flight_id = 0
        self.airline = ""
        self.flight_num = ""
        self.depart_code = ""
        self.dest_code = ""
        self.depart_date = ""
        self.depart_time = ""
        self.cost = 0
        self.avail_seats = 0
        self.avail_flights = []


    def set_flight(self, flight_id, airline, flight_num, depart_code, dest_code,
                   depart_date, depart_time, cost, avail_seats, avail_flights
                   ):
        self.flight_id = flight_id
        self.flight_num = flight_num
        self.airline = airline
        self.flight_num = flight_num
        self.depart_code = depart_code
        self.dest_code = dest_code
        self.depart_time = depart_time
        self.depart_time = depart_time
        self.cost = cost
        self.avail_seats = avail_seats
        self.avail_flights = avail_flights
