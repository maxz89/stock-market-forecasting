import psycopg2
from psycopg2 import Error
import app_secrets
import os

# Script to import all downloaded csv files with stock data into PostGres
try:
    # Connect to an existing database
    connection = psycopg2.connect(user="postgres",
                                  password=app_secrets.db_password,
                                  host="127.0.0.1",
                                  port="5432",
                                  database="stock_data")

    # Create a cursor to perform database operations
    cursor = connection.cursor()
    # Print PostgreSQL details
    print("PostgreSQL server information")
    print(connection.get_dsn_parameters(), "\n")

    # cursor.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")
    # print (cursor.fetchall())

    # Executing a SQL query
    
    

    directory = os.fsencode("C:\\Users\\huazh\\OneDrive - Georgia Institute of Technology\\Documents\\CS 4420\\evadb-stock-forecasting\\archive\\stocks")
    
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        ticker = filename[:-4]
        if ticker.isalpha():
            print(f"Working on: {ticker}" )
            create_query = f"CREATE TABLE {ticker}(date varchar, open double precision, high double precision, low double precision, close double precision, adj_close double precision, volume double precision);"
            copy_query = f"COPY {ticker} FROM 'C:\\Users\\huazh\\OneDrive - Georgia Institute of Technology\\Documents\\CS 4420\\evadb-stock-forecasting\\archive\\stocks\{ticker}.csv' DELIMITER ',' CSV HEADER"
            cursor.execute(create_query)
            cursor.execute(copy_query)
    # # Fetch result
    # # record = cursor.fetchone()
    

    print("You are connected to - \n")
    connection.commit()

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if (connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")