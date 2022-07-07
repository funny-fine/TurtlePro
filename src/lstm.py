import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
from sklearn.metrics import mean_squared_error
import numpy as np
import math



def difference(data_set, interval=1):
    diff = list()
    for i in range(interval, len(data_set)):
        value = data_set[i] - data_set[i - interval]
        diff.append(value)
    return pd.Series(diff)



def invert_difference(history, yhat, interval=1):
    return yhat + history[-interval]



def timeseries_to_supervised(data, lag=1):
    df = pd.DataFrame(data)
    columns = [df.shift(i) for i in range(1, lag + 1)]
    columns.append(df)
    df = pd.concat(columns, axis=1)
    df.fillna(0, inplace=True)
    return df



def scale(train, test):

    scaler = MinMaxScaler(feature_range=(-1, 1))

    scaler = scaler.fit(train)

    train_scaled = scaler.transform(train)
    test_scaled = scaler.transform(test)
    return scaler, train_scaled, test_scaled



def invert_scale(scaler, X, y):

    new_row = [x for x in X] + [y]

    array = np.array(new_row)

    array = array.reshape(1, len(array))

    invert = scaler.inverse_transform(array)

    return invert[0, -1]



def fit_lstm(train, batch_size, nb_epoch, neurons):

    X, y = train[:, 0:-1], train[:, -1]

    X = X.reshape(X.shape[0], 1, X.shape[1])

    model = Sequential()
    model.add(LSTM(neurons, batch_input_shape=(batch_size, X.shape[1], X.shape[2]), stateful=True))
    model.add(Dense(1))

    model.compile(loss='mean_squared_error', optimizer='adam')
    for i in range(nb_epoch):

        his = model.fit(X, y, batch_size=batch_size, verbose=1, shuffle=False)

        model.reset_states()
    return model



def forecast_lstm(model, batch_size, X):

    X = X.reshape(1, 1, len(X))

    yhat = model.predict(X, batch_size=batch_size)

    return yhat[0, 0]



data = pd.read_csv('LBMA-GOLD21.csv')
series = data.set_index(['Date'], drop=True)


raw_value = series.values


diff_value = difference(raw_value, 2)

supervised = timeseries_to_supervised(diff_value, 1)
supervised_value = supervised.values


testNum = 400
train, test = supervised_value[:-testNum], supervised_value[-testNum:]


scaler, train_scaled, test_scaled = scale(train, test)


lstm_model = fit_lstm(train_scaled, 1, 1, 4)

predictions = list()
for i in range(len(test_scaled)):

    X, y = test[i, 0:-1], test[i, -1]

    yhat = forecast_lstm(lstm_model, 1, X)

    yhat = invert_scale(scaler, X, yhat)

    yhat = invert_difference(raw_value, yhat, len(test_scaled) + 1 - i)

    predictions.append(yhat)


rmse = mean_squared_error(raw_value[:testNum], predictions)
print("Test RMSE:", rmse)
print(predictions)
plt.plot(predictions)
del predictions[0]

plt.plot(raw_value[-testNum:])
plt.plot(predictions)
plt.legend(['pred','true', 'pred_del'])
plt.show()