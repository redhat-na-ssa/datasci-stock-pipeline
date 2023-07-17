#
# Read stock market data from Yahoo and save to a csv file.
#

import os
import argparse

import yfinance as yf
from pandas_datareader import data as pdr

def get_args():

    parser = argparse.ArgumentParser(
             description="Get Stock Info"
    )

    # parser.set_defaults("IBM")
    parser.add_argument("ticker", nargs="?", type=str, help="Stock Ticker", default="IBM")
    parser.add_argument("filename", nargs="?", type=str, help="Filename")
    parser.add_argument("-s", "--start-date", type=str, help="Start Date", default="2023-01-01")
    parser.add_argument("-e", "--end-date", type=str, help="End Date", default="2023-06-01")

    args = parser.parse_args()

    try:
        return args
    except:
        print(args)

def output_stock_data(ticker, start_date, end_date, filename):

    print(f"Ticker: {ticker}")

    yf.pdr_override()
    df = pdr.get_data_yahoo(ticker, start=start_date, end=end_date)

    print(f"Count: \n{df.count()}")
    print(f"Saving: {filename}...")

    df.to_csv(filename)


if __name__ == "__main__":

    # create scratch path
    scratch = os.getenv("SCRATCH", "../scratch/")
    os.makedirs(scratch, exist_ok=True)

    args = get_args()

    if args.filename:
        filename = args.filename
    else:
        filename = scratch + args.ticker.upper() + "-sample.csv"

    output_stock_data(args.ticker, start_date=args.start_date, end_date=args.end_date, filename=filename)
