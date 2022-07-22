'''
psycopg2-test.py

Sample code demonstrating how to use the psycopg2 Python library to
connect to a database and execute a query.

author: Amy Csizmar Dalal
date: 26 April 2021
Adapted from code originally written by Jeff Ondich
'''

import psycopg2
import psqlConfig as config

def connect():
    '''
    Establishes a connection to the database with the following credentials:
        user - username, which is also the name of the database
        password - the password for this database on perlman

    Returns: a database connection.

    Note: exits if a connection cannot be established.
    '''
    try:
        connection = psycopg2.connect(database=config.database, user=config.user, password=config.password, host="localhost")
    except Exception as e:
        print("Connection error: ", e)
        exit()
    return connection

def getQuakesAboveMagnitude(connection, magnitude):
    '''
    Retrieves all earthquakes with a magnitude greater than the specified magnitude

    Parameters:
        connection - the connection to the database
        magnitude - retrieve all earthquakes above this magnitude from the data

    Returns:
        a collection of all earthquakes above this magnitude, or None if the query fails.
    '''
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM earthquakes WHERE mag>%s ORDER BY mag DESC"
        cursor.execute(query, (magnitude,))
        return cursor.fetchall()

    except Exception as e:
        print ("Something went wrong when executing the query: ", e)
        return None

def main():
    # Connect to the database
    connection = connect()

    # Execute a simple query: how many earthquakes above the specified magnitude are there in the data?
    results = getQuakesAboveMagnitude(connection, 5)

    if results is not None:
        print("Query results: ")
        for item in results:
            print(item)

    # Disconnect from database
    connection.close()

main()
