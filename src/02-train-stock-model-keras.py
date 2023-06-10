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
import matplotlib.pyplot as plt 
from pandas_datareader import data as pdr 
import yfinance as yf
import tensorflow as tf

tickers = 'IBM'
start_date = '1980-12-01'
end_date = '2018-12-31'

yf.pdr_override()
stock_data = pdr.get_data_yahoo(tickers, start_date)

stock_data_len = stock_data['Close'].count()
print(f'Read in {stock_data_len} stock values')


close_prices = stock_data.iloc[:, 1:2].values
# print(close_prices)

# Some of the weekdays might be public holidays in which case no price will be available. 
# For this reason, we will fill the missing prices with the latest available prices

all_bussinessdays = pd.date_range(start=start_date, end=end_date, freq='B')
print(all_bussinessdays)

close_prices = stock_data.reindex(all_bussinessdays)
close_prices = stock_data.fillna(method='ffill')

# The dataset is now complete and free of missing values. Let's have a look to the data frame summary:
# Feature scaling

training_set = close_prices.iloc[:, 1:2].values

from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range = (0, 1))
training_set_scaled = sc.fit_transform(training_set)
# print(training_set_scaled.shape)

# LSTMs expect the data in a specific format, usually a 3D tensor. I start by creating data with 60 days and converting it into an array using NumPy. 
# Next, I convert the data into a 3D dimension array with feature_set samples, 60 days and one feature at each step.
features = []
labels = []
for i in range(60, stock_data_len):
    features.append(training_set_scaled[i-60:i, 0])
    labels.append(training_set_scaled[i, 0])

features = np.array(features)
labels = np.array(labels)

features = np.reshape(features, (features.shape[0], features.shape[1], 1))

#
# Feature tensor with three dimension: features[0] contains the ..., features[1] contains the last 60 days of values and features [2] contains the  ...
#
# Create the LSTM network
# Let's create a sequenced LSTM network with 50 units. Also the net includes some dropout layers with 0.2 which means that 20% of the neurons will be dropped.

model = tf.keras.models.Sequential([
    tf.keras.layers.LSTM(units = 50, return_sequences = True, input_shape = (features.shape[1], 1)),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.LSTM(units = 50, return_sequences = True),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.LSTM(units = 50, return_sequences = True),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.LSTM(units = 50),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(units = 1)
])

print(model.summary())

# The model will be compiled and optimize by the adam optimizer and set the loss function as mean_squarred_error

model.compile(optimizer = 'adam', loss = 'mean_squared_error')

from time import time
start = time()
history = model.fit(features, labels, epochs = 2, batch_size = 32, verbose = 1)
end = time()

print('Total training time {} seconds'.format(end - start))

#
# Save the model
#
tf.keras.models.save_model(model, 'stocks/1')

testing_start_date = '2019-01-01'
testing_end_date = '2019-04-10'

test_stock_data = pdr.get_data_yahoo(tickers, testing_start_date, testing_end_date)

test_stock_data_processed = test_stock_data.iloc[:, 1:2].values

all_stock_data = pd.concat((stock_data['Close'], test_stock_data['Close']), axis = 0)

inputs = all_stock_data[len(all_stock_data) - len(test_stock_data) - 60:].values
inputs = inputs.reshape(-1,1)
inputs = sc.transform(inputs)

X_test = []
for i in range(60, 129):
    X_test.append(inputs[i-60:i, 0])

X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
predicted_stock_price = model.predict(X_test)
predicted_stock_price = sc.inverse_transform(predicted_stock_price)

#
# Plots
#
# plt.figure(figsize=(10,6))  
# plt.plot(test_stock_data_processed, color='blue', label='Actual Apple Stock Price')  
# plt.plot(predicted_stock_price , color='red', label='Predicted Apple Stock Price')  
# plt.title('Apple Stock Price Prediction')  
# plt.xlabel('Date')  
# plt.ylabel('Apple Stock Price')  
# plt.legend()  
# plt.show()  

