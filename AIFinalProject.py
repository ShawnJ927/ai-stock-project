"""
This is an AI Project designed train an AI which will determine whether a stock price will 
increase or decrease and the percentage change of the price by training the AI through 
historical stock pricing data

Authors: *** INSERT EVERYONE'S NAMES HERE *** Shawn Jordan

Note from Shawn - I've added initials to any comments I've made. Hopefully it gives 
us somewhere to start.
"""

import requests
import numpy as np
# These imports were suggested by a ChatGPT search - SJ
# To install them on pc, I used pip install scikit-learn
from hmmlearn import hmm
from sklearn.linear_model import LogisticRegression 
from sklearn.model_selection import train_test_split

# This is our API Key and Time Interval for the stock data - SJ
API_KEY = "VG7A8JAI80Y6VTCA"
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

    # check if response is successful, may want to rewrite this - SJ
    while response.status_code != 200:
        print("Error: ", response.status_code, " - response request unsuccessful")
        symbol = input("Stock Symbol entered Invalid. Please Reenter Stock Symbol\n").upper()
            
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_{INTERVAL.upper()}_ADJUSTED&symbol={symbol}&outputsize=full&apikey={API_KEY}" 
        response = requests.get(url)
    
    stock_data = response.json()

    return stock_data

def get_stock_historical_prices(data):
    """
    returns a numpy array containing the historical prices set on a specified interval
    from the extraced json respose
    """
    # change the case of the Interval value to match 
    first_letter = INTERVAL[0]
    rest_of_word = INTERVAL[1:].lower()
    Interval = first_letter + rest_of_word

    prices = list()
    for date, info in data[f"Time Series ({Interval})"].items():
        # gets the closing price of the stock for the specified interval as float - SJ
        price = float(info["4. close"])
        prices.append(price)

    # Convert the prices list to a numpy array - SJ
    prices = np.array(prices)
    
    return prices

# This is a function that I might refactor and delete later since it is a bit redundant - SJ
def get_stock_direction_and_percentage_change(prices):
    """
    uses the stock prices to train the AI using two functions and
    determines whether the stock price will go up (1) or down (0)
    """

    # cuts the numpy array down to the last 5 years of historical data
    # not sure what amount of data we want to feed the algorithm yet
    # may want longer or shorter to determine trend? - SJ
    prices_last_5_years = prices[-(5*252):]

    # algorithm n stuff go vroom here - SJ
    
    # once complete, return the direction and percentage change - SJ
    return get_stock_direction_change(prices_last_5_years), get_stock_percentage_change(prices_last_5_years)

# This is a function to learn from the given data to determine the direction of price change
def get_stock_direction_change(prices_x_years):
    """
    This will run the data through an algorithm and determine the direction of change
    given the historical pricing data fed to it
    """
    # placeholder variables - SJ
    # calculate the change in price for each day
    difference = np.diff(prices_x_years)
    # exclude the first element from the array to make data for next day
    up_or_down = np.where(difference[1:] > 0.0, 1, 0) # if the price is > 0, return 1, else 0
    
    logistic_regression = LogisticRegression(random_state=69) # create logistic regression model
    # input for current day's data by excluding the last element in the array
    x = difference[:-1].reshape(-1,1) 

    # Use LR to train
    # Split the data into training and testing data for the prediction model 
    x_train, x_test, y_train, y_test = train_test_split(x, up_or_down, test_size=.2, random_state=69, shuffle=False)
    logistic_regression.fit(x_train, y_train)
    
    # Make a prediction with LR Model for next day (modified from ChatGPT)
    y_prediction = logistic_regression.predict(x_test)
    # compare the actual data vs the prediction to determine the accuracy of the model
    # I got this ide from ChatGPT
    accuracy = np.mean(y_prediction == y_test)
    print("Calculated Accuracy for LR Model:",accuracy)
    # return whether the price went up or down (binary)
    return y_prediction[0]

def get_stock_percentage_change(prices_x_years):
    """
    This will run the data through an algorithm and determine the percentage of change
    given the historical pricing data fed to it
    """

    # Define model
    model = hmm.GaussianHMM(n_components=4, n_iter=100)

    # Fit model to data
    model.fit(prices_x_years.reshape(-1, 1))

    # Predict hidden states using model
    hidden_states = model.predict(prices_x_years.reshape(-1, 1))

    # Compute mean percentage change for each hidden state
    mean_changes = np.zeros(model.n_components)
    for i in range(model.n_components):
        mean_changes[i] = np.mean(np.diff(prices_x_years[hidden_states == i]) / prices_x_years[hidden_states == i][:-1])

    # Predict next hidden state based on current state
    current_state = hidden_states[-1]
    next_state = model.predict(prices_x_years[-1].reshape(-1, 1))[0]

    # Predict the percentage change in stock prices based on the current and next hidden states
    percentage_change = mean_changes[next_state] - mean_changes[current_state]

    return percentage_change

# This will check the stock based on the symbol the user enters in the command line, 

stock_symbol = input("Please enter a stock symbol you want to check\n").upper()
historical_prices = get_stock_historical_prices(get_stock_data(stock_symbol))
stock_direction, percentage_change = get_stock_direction_and_percentage_change(historical_prices)
if (stock_direction == 1):
    print ("Predicted direction of change is increasing using Logistic Regression")
else:
    print ("Predicted direction of change is decreasing using Logistic Regression")
print("Using HMM:")
print("Predicted Percentage Change of",stock_symbol,"-", percentage_change, "%")

