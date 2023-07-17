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

# from pandas_datareader import data as pdr
# import yfinance as yf
import tensorflow as tf
import os
from minio import Minio
from minio.error import S3Error
import tf2onnx
import onnx
import glob

# print(f'******* Env AWS_ACCESS_KEY_ID = {os.getenv("AWS_ACCESS_KEY_ID")}')
# print(f'******* Env AWS_SECRET_ACCESS_KEY = {os.getenv("AWS_SECRET_ACCESS_KEY")}')
# print(f'******* Env AWS_S3_ENDPOINT = {os.getenv("AWS_S3_ENDPOINT")}')

def train_model():
    ticker = "IBM"
    start_date = "1980-12-01"
    end_date = "2018-12-31"

    # yf.pdr_override()
    # stock_data = pdr.get_data_yahoo(tickers, start_date)

    scratch = os.getenv("SCRATCH", "../scratch/")
    
    filename = "../data/" + ticker + ".csv"
    stock_data = pd.read_csv(filename)

    stock_data_len = stock_data["Close"].count()
    print(f"Read in {stock_data_len} stock values")

    close_prices = stock_data.iloc[:, 1:2].values
    # print(close_prices)

    # Some of the weekdays might be public holidays in which case no price will be available.
    # For this reason, we will fill the missing prices with the latest available prices

    all_business_days = pd.date_range(start=start_date, end=end_date, freq="B")
    print(all_business_days)

    close_prices = stock_data.reindex(all_business_days)
    close_prices = stock_data.fillna(method="ffill")

    # The dataset is now complete and free of missing values. Let's have a look to the data frame summary:
    # Feature scaling

    training_set = close_prices.iloc[:, 1:2].values

    sc = MinMaxScaler(feature_range=(0, 1))
    training_set_scaled = sc.fit_transform(training_set)
    # print(training_set_scaled.shape)

    # LSTMs expect the data in a specific format, usually a 3D tensor. I start by creating data with 60 days and converting it into an array using NumPy.
    # Next, I convert the data into a 3D dimension array with feature_set samples, 60 days and one feature at each step.
    features = []
    labels = []
    for i in range(60, stock_data_len):
        features.append(training_set_scaled[i - 60 : i, 0])
        labels.append(training_set_scaled[i, 0])

    features = np.array(features)
    labels = np.array(labels)

    features = np.reshape(features, (features.shape[0], features.shape[1], 1))

    #
    # Feature tensor with three dimension: features[0] contains the ..., features[1] contains the last 60 days of values and features [2] contains the  ...
    #
    # Create the LSTM network
    # Let's create a sequenced LSTM network with 50 units. Also the net includes some dropout layers with 0.2 which means that 20% of the neurons will be dropped.

    model = tf.keras.models.Sequential(
        [
            tf.keras.layers.LSTM(
                units=50, return_sequences=True, input_shape=(features.shape[1], 1)
            ),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.LSTM(units=50, return_sequences=True),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.LSTM(units=50, return_sequences=True),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.LSTM(units=50),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(units=1),
        ]
    )

    print(model.summary())

    # The model will be compiled and optimize by the adam optimizer and set the loss function as mean_squarred_error

    model.compile(optimizer="adam", loss="mean_squared_error")

    #
    # For testing purposes, train for 2 epochs. This should be increased to improve model accuracy.
    #
    from time import time

    model_epochs = int(os.getenv("MODEL_EPOCHS", "2"))

    start = time()
    history = model.fit(features, labels, epochs=model_epochs, batch_size=32, verbose=1)
    end = time()

    print("Total training time {} seconds".format(end - start))

    #
    # Save the model
    #
    print("Saving the model to ../scratch/stocks/1")

    #
    # Tensorflow "save_model" format.
    #
    tf.keras.models.save_model(model, "../scratch/stocks/1")

    #
    # onnx format
    #
    # input_signature = [tf.TensorSpec([3, 3], tf.float32, name='x')]
    # onnx_model, _ = tf2onnx.convert.from_keras(model, input_signature, opset=13)
    onnx_model, _ = tf2onnx.convert.from_keras(model)

    onnx.save(onnx_model, "../scratch/stocks.onnx")


def upload_to_s3(bucket, local_path, bucket_path):
    # Create a client with the MinIO server playground, its access key
    # and secret key.
    client = Minio(
        endpoint=os.getenv("AWS_S3_ENDPOINT").lstrip("http://"),
        access_key=os.getenv("AWS_ACCESS_KEY_ID"),
        secret_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        secure=False,
    )

    # Create a bucket if it does not exist.
    found = client.bucket_exists(bucket)

    if not found:
        print(f"Using Endpoint: {os.getenv('AWS_S3_ENDPOINT')}")
        print(f"Attempting to create bucket: {bucket}")
        client.make_bucket(bucket)
    else:
        print(f"Bucket {bucket} already exists")

    try:
        print(f"Pushing {local_path} to {bucket}/{bucket_path}")
        client.fput_object(bucket, bucket_path, local_path)

    except S3Error as err:
        print(err)

def upload_local_directory_to_s3(bucket, local_path, bucket_path):
    # Create a client with the MinIO server playground, its access key
    # and secret key.
    client = Minio(
        endpoint=os.getenv("AWS_S3_ENDPOINT").lstrip("http://"),
        access_key=os.getenv("AWS_ACCESS_KEY_ID"),
        secret_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        secure=False,
    )

    assert os.path.isdir(local_path)

    for local_file in glob.glob(local_path + "/**"):
        local_file = local_file.replace(os.sep, "/")  # Replace \ with / on Windows
        if not os.path.isfile(local_file):
            upload_local_directory_to_s3(
                bucket, local_file, bucket_path + "/" + os.path.basename(local_file)
            )
        else:
            remote_path = os.path.join(bucket_path, local_file[1 + len(local_path) :])
            remote_path = remote_path.replace(
                os.sep, "/"
            )  # Replace \ with / on Windows
            client.fput_object(bucket, remote_path, local_file)


train_model()

upload_to_s3("models", "../scratch/stocks.onnx", "stocks.onnx")
upload_local_directory_to_s3("models", "../scratch/stocks", "stocks")
