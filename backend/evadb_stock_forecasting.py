# Import the EvaDB package
import evadb
import app_secrets

# Connect to EvaDB and get a database cursor for running queries
cursor = evadb.connect().cursor()

cursor.query('''
CREATE DATABASE IF NOT EXISTS postgres_data
WITH ENGINE = 'postgres',
PARAMETERS = {
    "user": "postgres",
    "password": "''' + app_secrets.db_password + '''",
    "host": "localhost",
    "port": "5432",
    "database": "stock_data"
}
''').df()

def getForecast(ticker: str, model: str):
    cursor.query(f'''
        CREATE OR REPLACE FUNCTION ForecastTicker FROM
        (
            SELECT *
            FROM postgres_data.{ticker} 
        )
        TYPE Forecasting
        PREDICT 'close'
        HORIZON 50
        TIME 'date'
        MODEL '{model}'
        FREQUENCY 'D';
        ''').df()
    forecast_output = cursor.query('''SELECT ForecastTicker();''').df()
    close_lo = forecast_output.loc[0, "close-lo"]
    close_hi = forecast_output.loc[0, "close-hi"]
    next_day_forecast = forecast_output.loc[0, "close"]
    print(f'returning {next_day_forecast}')
    return (next_day_forecast, close_lo, close_hi)
getForecast('amzn', 'Theta')




# print(cursor.query('''
# SELECT * FROM postgres_data.AAPL limit 3;
# ''').df())

# print(cursor.query('''
# CREATE OR REPLACE FUNCTION ApplePriceForecastRecent50 FROM
# (
#     SELECT *
#     FROM postgres_data.AAPL 
#     WHERE date > "2019-04-01"
# )
# TYPE Forecasting
# PREDICT 'close'
# HORIZON 50
# TIME 'date'
# FREQUENCY 'D';
# ''').df())

# print(cursor.query('''
# CREATE OR REPLACE FUNCTION AllyPriceForecast50 FROM
# (
#     SELECT *
#     FROM postgres_data.ALLY
# )
# TYPE Forecasting
# PREDICT 'close'
# HORIZON 50
# TIME 'date'
# FREQUENCY 'D';
# ''').df())

# print(cursor.query('''
# SELECT AllyPriceForecast50();
# ''').df())


# print(cursor.query('''
# CREATE OR REPLACE FUNCTION FordPriceForecast50 FROM
# (
#     SELECT *
#     FROM postgres_data.F
# )
# TYPE Forecasting
# PREDICT 'close'
# HORIZON 50
# TIME 'date'
# FREQUENCY 'D';
# ''').df())

# print(cursor.query('''
# SELECT FordPriceForecast50();
# ''').df())


# print(cursor.query(''''''))

# All data with horizon 8
# print(cursor.query('''
# SELECT ApplePriceForecast();
# ''').df())


# All data with horizon 50
# Results in pretty accurate next day data but no real price oscillations after that causes inaccuracy
# Predicts a slower long term growth trend -> the price rising from 243.38 to 246.9 in next 50 days
# print(cursor.query('''
# SELECT ApplePriceForecast50();
# ''').df())

# Past 5 years with horizion 50
# Results in pretty accurate direction of movement predictions next 5 days but not after
# The actual next day price is not as accurate
# print(cursor.query('''
# SELECT ApplePriceForecastRecent50();
# ''').df())

