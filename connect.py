import psycopg2
from config import config
import json
from utilities import DatetimeEncoder

class Connect:
    connection = None
    def __init__(self):
        try:
            # read connection parameters
            params = config()

            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database')
            self.connection = psycopg2.connect(**params)

            # create cursor
            # cursor = connection.cursor()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            
    
    def closeConnection(self):
        if self.connection is not None:
                self.connection.close()
                print('Database connection closed')

    def getTest(self):
        cur = self.connection.cursor()
        cur.execute('SELECT * FROM dziekanat.studenci')
        answer = cur.fetchone()
        return json.dumps(answer, cls=DatetimeEncoder)
    
'''
def connect():
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database')
        conn = psycopg2.connect(**params)

        # create cursor
        cur = conn.cursor()

        #print('PostgreSQL database version:')
        cur.execute('SELECT * FROM dziekanat.studenci')

        db_version = cur.fetchone()
        print(db_version)

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()
            print('Database connection closed')

if __name__ == '__main__':
    connect()

'''