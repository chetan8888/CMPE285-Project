from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
import requests
from random import randrange

API_KEY = "CHX24ZAMVDU3MJ6D"
SYMBOLS_URL = "https://cloud.iexapis.com/beta/ref-data/symbols?token=sk_d240706be75b46eb8dc6dcb8cde34005"
NUMBER_SYMBOLS = 30



views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():    
    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

def get_indicators():
    indicators = {}
    indicators['ethical'] = 'RSI'
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

    indexes = []
    for i in range(NUMBER_SYMBOLS):
        indexes.append(randrange(0,len(symbols_data)))
    
    for index in indexes:
        symbols.append(symbols_data[index]['symbol'])
        
    
    indicators = get_indicators()
    
    for strategy in strategies:
        for symbol in symbols:
            indicator = indicators[strategy]
            url = 'https://www.alphavantage.co/query?&&interval=monthly&time_period=10&series_type=open&apikey=' + API_KEY
            url += '&symbol=' + symbol + '&function=' + indicator
            
            response = requests.get(url)
            data = response.json()

            value = 0
            count = 0
            key = 'Technical Analysis: ' + indicator
            for date in data[key]:
                value += float(data[key][date][indicator])
                count += 1
            
            if count != 0:
                value = value/count
                stocks.append([symbol, value])
    
    return stocks

@views.route('/portfolio', methods=['POST','GET'])
def portfolio():
    stocks = {}
    if request.method == 'POST':
        strategies = []
        amount = request.form.get('amount')
        for strategy in request.form:
            if request.form.get(strategy) == '1':
                strategies.append(strategy)
        
        print(amount ,strategies)

        stocks = get_stocks(strategies)
        print(stocks)


    return render_template("portfolio.html", user=current_user, stocks=stocks)