#
# Read stock market data from Yahoo and save to a csv file.
#

from pandas_datareader import data as pdr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

if __name__ == '__main__':
    ticker = 'IBM'
    filename = ticker + '.csv'
    yf.pdr_override()
    df = pdr.get_data_yahoo(ticker, start='2023-01-01', end='2023-06-01')
    print(f'Count = {df.count()}')
    print(f'Saving as {filename}')
    df.to_csv(filename)
