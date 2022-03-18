import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv
import os


class Database:    
    def __init__(self):
        self.name = "database_connect"


    def execute_sql(self, sql, update=False):
        """method opens db connection and executes SQL statement.
            Update variable determines SQL statement type"""
        try:
            load_dotenv()
            conn = psycopg2.connect(
                user=os.environ.get('USER'),
                password=os.environ.get('PASSWORD'),
                database="air_res_prod_db",
                port="5432",
            )
            cur = conn.cursor()
            if update == True:
                # runs any statement other than SELECT
                cur.execute(sql)
                conn.commit()
                return None
            else:
                # runs a SELECT statement
                cur.execute(sql)
                sql_query = cur.fetchall()
                return sql_query

        except (Error) as e:
            print("Error while connecting to PostgreSQL ", e)

        finally:
            if conn:
                cur.close()
                conn.close()
