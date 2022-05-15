from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import portfolio, User
from . import db
import json
import requests
from random import randrange
from . import models

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
    if len(strategies) > 1:
        indexes.append(randrange(0,10))

        i = randrange(0,10)
        while i == indexes[-1]:
            i = randrange(0,10)
        
        indexes.append(i)
        indexes.append(randrange(11,20))
    else:
        while len(indexes) < 3:
            index = randrange(0,len(symbols))
            if index not in indexes:
                indexes.append(index)
    
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

@views.route('/show_portfolio', methods=['POST','GET'])
@login_required
def show_portfolio():
    if request.method == 'POST':
        stocks = []
        if request.method == 'POST':
            strategies = []
            amount = int(request.form.get('amount'))
            for strategy in request.form:
                if request.form.get(strategy) == '1':
                    strategies.append(strategy)
            
            print(amount ,strategies)

            stock_data = get_stocks(strategies)
            print(stock_data)
            
            # stock_data = sorted(stock_data, key=lambda x:x[1])

            # if len(stock_data) > 3:
            #     stock_data = stock_data[:3]
            
            price = 0
            if len(stock_data) != 0:
                price = amount/len(stock_data)
            
            for s in stock_data:
                stocks.append([s, price])
            
            print(stocks)
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
        return render_template("portfolio.html", user=current_user)