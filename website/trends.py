import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader as web

#work on  this for other stocks

def individual_trends(tickers):

    tickers = ["FB", "AMZN", "AAPL"]
    multpl_stocks = web.get_data_yahoo(tickers,
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
    # plt.show()
    plt.savefig("website/static/output/indiv_trend.png")

    return multpl_stocks


def portfolio_trend(multpl_stocks):

  multpl_stock_daily_returns = multpl_stocks['Adj Close'].pct_change()
  # multpl_stock_monthly_returns = multpl_stocks['Adj Close'].resample('M').ffill().pct_change()
  fig = plt.figure()
  (multpl_stock_daily_returns + 1).cumprod().plot()
  # plt.show()
  plt.savefig("websi/static/output/portfolio_trend.png")

# tickers = ["FB", "AMZN", "AAPL"]
# multpl_stocks = individual_trends(tickers)
# portfolio_trend(multpl_stocks)