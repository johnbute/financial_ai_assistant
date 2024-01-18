from neuralintents import GenericAssistant
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader as web
import mplfinance as mpf
import yfinance
import pickle
import sys
import datetime as dt



portfolio = {'AAPL': 20, 'TSLA': 5, 'GS': 10}

with open('portfolio.pkl', 'rb') as f:
    portfolio = pickle.load(f)



def save_portfolio():
    with open('portfolio.pkl', 'wb') as f:
        pickle.dump(portfolio, f)


def add_portfolio():
    ticker = input("Which Stok do you want to add: ")
    amount = input("How many shares do you want to add: ")
    
    if ticker in portfolio.keys():
        portfolio[ticker] += amount
    else:
        portfolio[ticker] = amount
    save_portfolio()


def remove_portfolio():
    ticker = input("Wich stock do you want to sell: ")
    amount = input("How many shares do you want to sell: ")

    if ticker in portfolio.keys():
        if amount <= portfolio[ticker]:
            portfolio[ticker] -= amount
            save_portfolio()
        else:
            print("You don't have enough shares!")

    else:
        print(f"You do not own any shares of {ticker}")


def show_portfolio():
    print("Your portfolio: ")
    for ticker in portfolio.keys():
        print(f"You own {portfolio[ticker]} shares of {ticker}")



def portfolio_worth():
    sum = 0
    for ticker in portfolio.keys():
        data = yfinance.download(ticker)
        price = data['Close'].iloc[-1]
        sum += price
    print(f"Your portfolio is worth {sum} USD")



def portfolio_gains():
    starting_date = input("Enter a date for comparison (YYYY-MM-DD): ")

    sum_now = 0
    sum_then = 0

    try:
        for ticker in portfolio.keys():
            data = yfinance.download(ticker, starting_date)
            price_now = data['Close'].iloc[-1]
            price_then = data.loc[data.index == starting_date]['Close'].values[0]
            sum_now += price_now
            sum_then += price_then

        print(f"Relative Gains: {(sum_now- sum_then)/sum_then * 100}% ")
        print(f"Absolute Gains: {(sum_now- sum_then)} USD ")


    except IndexError:
        print("There was no trading on this day")

print(portfolio)



def plot_chart():
    ticker = input("Choose a ticker symbol: ")
    starting_string = input("Choose a starting date (DD/MM/YYYY): ")

    plt.style.use('dark_background')
    start = dt.datetime.strptime(starting_string, "%d/%m/%Y")

    end = dt.datetime.now()


    data = yfinance.download(ticker,start,end)

    colors = mpf.make_marketcolors(up = '#00ff00', down = '#ff0000', wick = 'inherit', edge = 'inherit', volume = 'in')
    mpf_style = mpf.make_mpf_style(base_mpf_style = 'nightclouds', marketcolors = colors)

    mpf.plot(data, type = 'candle', style = mpf_style, volume = True)



def bye():
    print("Goodbye")

    sys.exit(0)

def handle_unknown():
    print("I'm sorry, I didn't understand that. Could you please be more specific?")


mappings = {
    'plot_chart' : plot_chart,
    'add_portfolio' : add_portfolio,
    'remove_portfolio': remove_portfolio,
    'show_portfolio' : show_portfolio,
    'portfolio_worth' : portfolio_worth,
    'portfolio_gains' : portfolio_gains,
    'bye': bye,

    'show_stock_price' : plot_chart,
    'unkown' : handle_unknown
    
}
assistant = GenericAssistant('intents.json', mappings)

assistant.fit_model(epochs = 13)

assistant.save_model()

while True:
    message = input("User: ")
    
    assistant.process_input(message)

