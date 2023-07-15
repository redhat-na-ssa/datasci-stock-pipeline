#!/usr/bin/env python
# coding: utf-8
#
# Predict stock prices with Long short-term memory (LSTM)
# This simple example will show you how LSTM models predict time series data. Stock market data is a great choice for this because it's quite regular and widely available via the Internet.
#
# Introduction
# LSTMs are very powerful in sequence prediction problems. They can store past information.
# Loading the dataset
# Use the pandas-data reader to get the historical stock prices from Yahoo! finance.
# For this example, I get only the historical data till the end of *training_end_data*.
#

import numpy as np
import pandas as pd

from sklearn.preprocessing import MinMaxScaler

from pandas_datareader import data as pdr
import yfinance as yf

from minio import Minio
from minio.error import S3Error

import onnx

# print(f'******* Env AWS_ACCESS_KEY_ID = {os.getenv("AWS_ACCESS_KEY_ID")}')
# print(f'******* Env AWS_SECRET_ACCESS_KEY = {os.getenv("AWS_SECRET_ACCESS_KEY")}')
# print(f'******* Env AWS_S3_ENDPOINT = {os.getenv("AWS_S3_ENDPOINT")}')


def predict():

    print(f"Model: Loading...")
    onnx.load_model("../scratch/stocks.onnx")
    print(f"Model: Loaded")

    # sc = MinMaxScaler(feature_range=(0, 1))

    # testing_start_date = "2019-01-01"
    # testing_end_date = "2019-04-10"

    # test_stock_data = pdr.get_data_yahoo(tickers, testing_start_date, testing_end_date)

    # test_stock_data = test_stock_data.iloc[:, 1:2].values

    # all_stock_data = pd.concat((stock_data["Close"], test_stock_data["Close"]), axis=0)

    # inputs = all_stock_data[len(all_stock_data) - len(test_stock_data) - 60 :].values
    # inputs = inputs.reshape(-1, 1)
    # inputs = sc.transform(inputs)

    # X_test = []
    # for i in range(60, 129):
    #     X_test.append(inputs[i - 60 : i, 0])

    # X_test = np.array(X_test)
    # X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    # predicted_stock_price = model.predict(X_test)
    # predicted_stock_price = sc.inverse_transform(predicted_stock_price)
    
    
predict()
