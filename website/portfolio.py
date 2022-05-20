# import pandas as pd

import pandas_datareader.data as web
import matplotlib.pyplot as plt
import datetime as dt


def createPlot(tickers, amounts):
  tickers = ['WFC', 'AAPL','MSFT']
  amounts = [100, 100,20]
  prices = []
  total = []

  for ticker in tickers:
      df = web.DataReader(ticker, 'yahoo', dt.datetime(2019,8,1), dt.datetime.now())
      price = df[-1:]['Close'][0]
      prices.append(price)
      index = prices.index(price)
      total.append(price * amounts[index])
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
  # plt.plot()
  plt.savefig("website/output/portfolio_graph.png")


#TEST CODE
# tickers = ['WFC', 'AAPL','MSFT']
# amounts = [100, 100,20]
# createPlot(tickers, amounts)