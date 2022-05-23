# import pandas as pd

import pandas_datareader.data as web
import matplotlib.pyplot as plt
import datetime as dt
# from . import views

# stock_data = show_portfolio(strategies)

def createPlot(tickers, investment_amount):
  tickers = ['WFC', 'AAPL','MSFT']
  # investment_amount = amounts
  print("Investment_amount\n")
  print(investment_amount)

  # amounts = [100, 100,20]
  prices = []
  total = []

  # Dollar invested  [1000,1000,1000]
  # prices [x,y,z]
  # amounts = [1000/x, 1000/y, 1000/z] i.e test
  test = []
  amounts = []
  for ticker in tickers:
      df = web.DataReader(ticker, 'yahoo', dt.datetime(2019,8,1), dt.datetime.now())
      price = df[-1:]['Close'][0]
      prices.append(price)
      
      index = prices.index(price)
      print("Index", index)
      print("price", price)
      # print("investment_amount", investment_amount[index])
      print("calculation",  investment_amount[index]/price)

      test.append(investment_amount[index]/price)
      print(test)
      
      total.append(price * test[index])

      print("total")
      print(total)
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

  # final_amt = sum(total)
  ax.text(-2,1, 'PORTFOLIO OVERVIEW:', fontsize=14, color="#ffe536", horizontalalignment='center', verticalalignment='center')
  ax.text(-2,0.85, f'Total USD Amount: {sum(total):.2f} $', fontsize=12, color="white", horizontalalignment='center', verticalalignment='center')

  # ax.text(-2,0.85, "TOTAL AMOUNT", fontsize=12, color="white", horizontalalignment='center', verticalalignment='center')

  counter = 0.15
  for ticker in tickers:
      ax.text(-2, 0.85 - counter, f'{ticker}: {total[tickers.index(ticker)]:.2f} $', fontsize=12, color="white",
              horizontalalignment='center', verticalalignment='center')
      counter += 0.15
  plt.plot()
  fig.savefig("static/output/portfolio_graph.png")


#TEST CODE
tickers = ['FB', 'AAPL','MSFT']
amounts = [2000.0, 2000.0, 2000.0]
createPlot(tickers, amounts)