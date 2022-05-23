from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import portfolio, User
from . import db
import json
import requests
from random import randrange
from . import models
from . import portfolio as pf
import matplotlib.pyplot as plt
import matplotlib
# import pandas_datareader as web
# import yfinance as yfin
# yfin.pdr_override()
from pandas_datareader import data as pdr
import datetime as dt
# import yfinance as yfin
# yfin.pdr_override()


API_KEY = "CHX24ZAMVDU3MJ6D"
SYMBOLS_URL = "https://cloud.iexapis.com/beta/ref-data/symbols?token=sk_d240706be75b46eb8dc6dcb8cde34005"
NUMBER_SYMBOLS = 20

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    portfolio_row = portfolio.query.filter_by(user_id = current_user.id).first()
    if portfolio_row is None:
        return render_template("home.html", user=current_user)
    else:
        return render_template("portfolio.html", user=current_user)

def get_indicators():
    indicators = {}
    indicators['ethical'] = 'ADXR'
    indicators['growth'] = 'SMA'
    indicators['index'] = 'EMA'
    indicators['quality'] = 'ADX'
    indicators['value'] = 'CCI'
    return indicators

def individual_trends(tickers):
    # tickers = ["FB", "AMZN", "AAPL"]
    matplotlib.use('agg')
    print(tickers)
    multpl_stocks = pdr.get_data_yahoo(tickers,
    start = "2022-05-8",
    end = "2022-05-16")
    fig = plt.figure(figsize=(20,20))
    ax1 = fig.add_subplot(321)
    ax2 = fig.add_subplot(322)
    ax3 = fig.add_subplot(323)
    ax1.plot(multpl_stocks['Adj Close'][tickers[0]])
    ax1.set_title(tickers[0]).set_fontsize(20)
    ax2.plot(multpl_stocks['Adj Close'][tickers[1]])
    ax2.set_title(tickers[1]).set_fontsize(20)
    ax3.plot(multpl_stocks['Adj Close'][tickers[2]])
    ax3.set_title(tickers[2]).set_fontsize(20)
    plt.subplots_adjust(left=0.1,
                    bottom=0.1, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.4, 
                    hspace=0.4)
    plt.savefig("website/output/indiv_trend.png")
    return multpl_stocks

def createPlot(tickers, amounts):
  matplotlib.use('agg')
  print("Inside Create plot")
#   tickers = ['WFC', 'AAPL','MSFT']
#   amounts = [100, 100,20]
  prices = []
  total = []
  print("tickers")

  print(tickers)

  for ticker in tickers:
      df = pdr.DataReader(ticker, 'yahoo', dt.datetime(2022,5,15), dt.datetime.now())
      price = df[-1:]['Close'][0]
      prices.append(price)
      index = prices.index(price)
    #   total.append(price * amounts[index])
      total = amounts
  fig = plt.figure()
  g, ax = plt.subplots(figsize=(18,8))
  ax.set_facecolor('black')
  ax.figure.set_facecolor('#121212')
  ax.tick_params(axis='x', colors='white')
  ax.tick_params(axis='y', colors='white')
  ax.set_title("PORTFOLIO VISUALIZER", color='#EF6C35', fontsize=20)

# patches, texts, autotexts = ax.pie(total, labels=tickers, autopct='%1.1f%%', pctdistance=1)
  patches, texts, autotexts = ax.pie(total, labels=tickers, autopct='%1.1f%%', pctdistance=1)
  [text.set_color('white') for text in texts]

  my_circle = plt.Circle((0, 0), 0.55, color='black')
  plt.gca().add_artist(my_circle)
  ax.text(-2,1, 'PORTFOLIO OVERVIEW:', fontsize=14, color="#ffe536", horizontalalignment='center', verticalalignment='center')
  ax.text(-2,0.85, f'Total USD Amount: {sum(total):.2f} $', fontsize=12, color="white", horizontalalignment='center', verticalalignment='center')
  # ax.text(-2,0.85, "TOTAL AMOUNT", fontsize=12, color="white", horizontalalignment='center', verticalalignment='center')

  counter = 0.15
  for ticker in tickers:
      ax.text(-2, 0.85 - counter, f'{ticker}: {total[tickers.index(ticker)]:.2f} $', fontsize=12, color="white",
              horizontalalignment='center', verticalalignment='center')
      counter += 0.15
  # plt.plot()
  plt.savefig("website/output/portfolio_graph.png")


def portfolio_trend(multpl_stocks):
  matplotlib.use('agg')
  multpl_stock_daily_returns = multpl_stocks['Adj Close'].pct_change()

  # multpl_stock_monthly_returns = multpl_stocks['Adj Close'].resample('M').ffill().pct_change()
  fig = plt.figure()
  (multpl_stock_daily_returns + 1).cumprod().plot()
  # plt.show()
  plt.savefig("website/output/portfolio_trend.png")

def get_stocks(strategies):
    stocks = []

    symbols = []
    symbols_response = requests.get(SYMBOLS_URL)
    symbols_data = symbols_response.json()
    # print("symbols: ", symbols_data)

    indexes = []
    for i in range(NUMBER_SYMBOLS):
        indexes.append(randrange(0,len(symbols_data)))
    
    print("indexes: ", indexes)
    
    for index in indexes:
        symbols.append(symbols_data[index]['symbol'])
    
    print("symbols: ", symbols)
    indicators = get_indicators()

    indexes = []
    while len(indexes) < 3:
        index = randrange(0,len(symbols))
        if index not in indexes and symbols[index][-1] != '+':
            indexes.append(index)
        else:
            index = randrange(0,len(symbols))

    # if len(strategies) > 1:
        
    #     i = randrange(0,10)
    #     while symbols[i][-1] == '+':
    #         i = randrange(0,10)
    #     indexes.append(i)

    #     i = randrange(0,10)
    #     while i == indexes[-1] or symbols[i][-1] == '+':
    #         i = randrange(0,10)
        
    #     indexes.append(i)
    #     indexes.append(randrange(11,20))
    # else:
    #     while len(indexes) < 3:
    #         index = randrange(0,len(symbols))
    #         if index not in indexes and symbols[index][-1] == '+':
    #             indexes.append(index)
    
    for i in indexes:
        stocks.append(symbols[i])

    
    # for strategy in strategies:
    #     for symbol in symbols:
    #         indicator = indicators[strategy]
    #         url = 'https://www.alphavantage.co/query?&interval=monthly&time_period=10&apikey=' + API_KEY
    #         url += '&symbol=' + symbol + '&function=' + indicator
    #         print(url)
            
    #         response = requests.get(url)
    #         data = response.json()
    #         for k in data:
    #             print(k)

    #         value = 0
    #         count = 0
    #         key = 'Technical Analysis: ' + indicator
    #         if key in data:
    #             for date in data[key]:
    #                 value += float(data[key][date][indicator])
    #                 count += 1
                
    #             if count != 0:
    #                 value = value/count
    #                 stocks.append([symbol, value])
    
    return stocks

    # def dummy:

@views.route('/show_portfolio', methods=['POST','GET'])
@login_required
def show_portfolio():
    print(request.form)
    if request.method == 'POST':
        stocks = []
        if request.method == 'POST':
            strategies = []
            amount = int(request.form.get('amount'))
            if amount < 5000:
                flash('Amount must be atleast $5000.', category='error')
                return render_template("home.html", user=current_user)
            else:
                for strategy in request.form:
                        if request.form.get(strategy) == '1':
                            strategies.append(strategy)

                if len(strategies)==0:
                    flash('Select atleast one strategy!', category='error')
                    return render_template("home.html", user=current_user)
                elif len(strategies)>2:
                    flash('Select maximum two strategies!', category='error')
                    return render_template("home.html", user=current_user)
                else:
                    
                    print(amount ,strategies)

                    stock_data = get_stocks(strategies)
                    print(stock_data)
                    
                    # stock_data = sorted(stock_data, key=lambda x:x[1])

                    # if len(stock_data) > 3:
                    #     stock_data = stock_data[:3]
                    
                    price = 0
                    investment_price = []
                    if len(stock_data) != 0:
                        price = amount/len(stock_data)
                        # investment_price.append(price)
                        # investment_price.append(price)
                        # investment_price.append(price)
                    

                    for s in stock_data:
                        print(s)
                        stocks.append([s, price])
                        investment_price.append(price)
                        # pf.createPlot(stock_data, [100, 100,20])

                    print("Investment Price")
                    print(investment_price)

                    print("stocks")
                    print(stocks)
                    print(stocks[0])
                    
                    multpl_stocks = individual_trends(stock_data)
                    print("multpl_stocks", multpl_stocks)
                    portfolio_trend(multpl_stocks)
                    amounts = [100, 100,20]
                    createPlot(stock_data, investment_price)

                    print("Here")
                    stock1 = ''
                    stock2 = ''
                    stock3 = ''

                    if len(stocks) > 0:
                        stock1 = stocks[0]
                    if len(stocks) > 1:
                        stock2 = stocks[1]
                    if len(stocks) > 2:
                        stock3 = stocks[2]
                    
                    new_portfolio = portfolio(stock1='stock1', stock2='stock2', stock3='stock3', price=price, user_id=current_user.id)
                    db.session.add(new_portfolio)
                    db.session.commit()
                    flash("Portfolio added!", category='success')
                    # Sample stocks
                    # [['GJP', 1666.6666666666667], ['EBET', 1666.6666666666667], ['ADAL', 1666.6666666666667]]
                    return render_template("portfolio.html", user=current_user)
    else:
        # multpl_stocks = individual_trends(stock_data)
        # print("multpl_stocks", multpl_stocks)
        # portfolio_trend(multpl_stocks)
        # amounts = [100, 100,20]
        # createPlot(stock_data, investment_price)
        return render_template("portfolio.html", user=current_user)



        