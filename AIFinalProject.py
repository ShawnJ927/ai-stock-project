"""
This is an AI Project designed train an AI which will determine whether a stock price will 
increase or decrease and the percentage change of the price by training the AI through 
historical stock pricing data

Authors: *** INSERT EVERYONE'S NAMES HERE *** Shawn Jordan

Note from Shawn - I've added initials to any comments I've made. This is just starter code
I have come up with and might end up wildly different in the end, but hopefully it gives 
us somewhere to start.
"""

import requests
import numpy as np

# Replace empty API_Key with Alpha Vantage API key once we have it - SJ
API_KEY = ""
INTERVAL = "DAILY"

# This is a sample function that we might be able to use to build on or change to fit other functions - SJ
def get_stock_data(symbol):
    """
    Returns the stock data for a given symbol using daily intervals.
    note in the URL - &outputsize can be set to either ---
        full - Outputs data on the set "interval" for the last 20 years
        compact - Outputs data on the set "interval" for the last 100 data points
    We can also set the interval var from DAILY to WEEKLY or MONTHLY
    """

    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_{INTERVAL.upper()}_ADJUSTED&symbol={symbol}&outputsize=full&apikey={API_KEY}" 
    response = requests.get(url)
    stock_data = response.json()

    return stock_data

def get_stock_historical_prices(data):
    """
    returns a numpy array containing the historical prices set on a specified interval
    from the extraced json respose
    """

    prices = list()
    for date, info in data[f"Time Series ({INTERVAL})"].items():
        # gets the closing price of the stock for the specified interval as float - SJ
        price = float(info["4. close"])
        prices.append(price)

    # Convert the prices list to a numpy array - SJ
    prices = np.array(prices)
    
    return prices

# This is a function that needs editing to work with a training algorithm - SJ
def get_stock_direction_and_percentage_change(prices):
    """
    uses the stock prices to train the AI using selected algorithm and
    determines whether the stock price will go up (1) or down (0)
    """
    # Placeholder - SJ
    direction = 0
    percentage_change = 0.0

    # cuts the numpy array down to the last 5 years of historical data
    # not sure what amount of data we want to feed the algorithm yet
    # may want longer or shorter to determine trend? - SJ
    prices_last_5_years = prices[-(5*252):]

    # algorithm n stuff go vroom here - SJ
    
    # once complete, return the direction and percentage change - SJ
    return direction, percentage_change

# This will check the stock based on the symbol the user enters in the command line, 
# We will need to modify this probably to check if a stock symbol is a valid one - SJ

stock_symbol = input("Please enter a stock symbol you want to check")
historical_prices = get_stock_historical_prices(get_stock_data(stock_symbol))
stock_direction, percentage_change = get_stock_direction_and_percentage_change(historical_prices)
if (stock_direction == 1):
    print(f'The stock price will increase approximately {percentage_change:.2f}%.')
else:
    print(f'The stock price will decrease approximately {percentage_change:.2f}%.')
