from src.classes.database import Database


class User(Database):
    def __init__(self):
        self.username = ""
        self.password = ""
        self.f_name = ""
        self.l_name = ""

    def set_user(self, username, password, f_name, l_name):
        self.username = username
        self.password = password
        self.f_name = f_name
        self.l_name = l_name
        

    def verify_username(self, update=False):
        """Method verifies username is unique"""
        # use global user_reg
        sql = """ SELECT username
                FROM users
                WHERE username = '%s'
                """ % (
            self.username
        )
        sql_query = self.execute_sql(sql, update)
        if sql_query == []:
            # username is unique and can be used
            return True
        else:
            # username is not unique and cannot be used
            return False

    def set_user_db(self, update=True):
        """Method updates user table with user registration information"""
        verify = self.verify_username()
        if verify:
            try:
                sql = """INSERT INTO users (username, pass, f_name, l_name)
                        VALUES ('%s', '%s', '%s', '%s')
                        """ % (self.username, self.password, self.f_name, self.l_name)
                self.execute_sql(sql, update)
                return True
            except Exception as e:
                print("Error updating users table", e)
                return False
        else:
            return False

    def login(self, username, password):
        # declare global user = User()
        """Method verifies username and password match"""
        sql = """ SELECT username, pass
                FROM users
                WHERE username = '%s'
                AND pass = '%s'
                """ % (username, password)

        sql_query = self.execute_sql(sql, update=False)
        if sql_query == []:
            # no matching username and password
            return False
        elif sql_query[0][0] == username and sql_query[0][1] == password:
            # username and password match
            self.get_user_db(username)
            return True
        else:
            # username or password is incorrect
            return False

    def get_user_db(self, username):
        """Method gets user information based on log in information"""
        sql = """ SELECT f_name, l_name
                FROM users
                WHERE username = '%s'
                """ % (username)
                
        sql_query = self.execute_sql(sql)
        self.username = username
        self.f_name = sql_query[0][0]
        self.l_name = sql_query[0][1]


    def logout(self, search, res, flight):
        """Method initializes all global variables on log out"""
        
        # initialize user object
        self.username = ''
        self.password = ''
        self.f_name = ''
        self.l_name = ''
        # initialize search object
        search.username = ''
        search.depart_code = ''
        search.dest_code = ''
        search.depart_date = ''
        search.seats_requested = 0
        # initialize res object
        res.username = ''
        res.f_name = ''
        res.l_name = ''
        res.flight_id = 0
        res.airline = ''
        res.flight_num = ''
        res.depart_date = ''
        res.dest_code = ''
        res.depart_date = ''
        res.depart_time = ''
        res.cost = 0
        res.avail_seats = 0
        res.seats_requested = 0
        res.total_cost = 0
        # initialize flight object
        flight.flight_id = 0
        flight.airline = ""
        flight.flight_num = ""
        flight.depart_code = ""
        flight.dest_code = ""
        flight.depart_date = ""
        flight.depart_time = ""
        flight.cost = 0
        flight.avail_seats = 0
        flight.avail_flights = []
        

    def update_user(self, username, password, f_name, l_name, update=True):
        """Method allows the user to update profile information"""
        try:
            sql = """UPDATE users SET
            pass = '%s',
            f_name = '%s',
            l_name = '%s'
            WHERE username = '%s'
            """ % (password, f_name, l_name, username)
            self.execute_sql(sql, update)
        except Exception as e:
            print("Error updating users table", e)
            return False


    def delete_user(self, username, update=True):
        """Method allows the user to delete user profile"""
        try:
            sql = """DELETE FROM users
                        WHERE username = '%s'       
                        """ % (username, )
            self.execute_sql(sql, update)
        except Exception as e:
            print("Error updating users table", e)
            return False
        
        
    def get_password(self, username):
        try:
            sql = """SELECT pass
                    FROM users
                    WHERE username = '%s'
                    """ % (username, )
            sql_query = self.execute_sql(sql)
            return sql_query
        except Exception as e:
            print("Error updating users table", e)
            return False
