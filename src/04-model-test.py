#!/usr/bin/env python
# coding: utf-8
#

import onnx

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
