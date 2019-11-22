import psycopg2
from myConfig import configDB
import json
from utilities import DatetimeEncoder
import datetime

def dateConverter(o):
    if isinstance(o, datetime.date):
        return o.isoformat()

def resultToJson(cur, numberOfRows):
    r = [dict((cur.description[i][0], value) \
        for i, value in enumerate(row)) for row in cur.fetchmany(numberOfRows)]
    return r

class Connect:
    connection = None
    def __init__(self):
        try:
            # read connection parameters
            params = configDB()

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
        result = resultToJson(cur,2)

        jsontest = "[ \
            {\
                'id': 1, \
                'first_name': 'Jan1', \
                'last_name': 'Kowalski1' \
            }, \
            {\
                'id': 2, \
                'first_name': 'Jan2', \
                'last_name': 'Kowalski2'\
            }, \
            {\
                'id': 3, \
                'first_name': 'Jan3', \
                'last_name': 'Kowalski3'\
            }, \
        ]"

        print(jsontest)
        #answer = cur.fetchone()
        #print(answer)
        
        print(json.dumps(jsontest, default=dateConverter))
        return json.dumps(jsontest, default=dateConverter)#cls=DatetimeEncoder)
    
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