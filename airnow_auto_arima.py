import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from pmdarima.arima import auto_arima
import numpy as np


# import and transform data
df = pd.read_csv('/Users/josephdixon/Desktop/Data Projects/AirNow/airnow_data.csv')
df = df.drop('0', axis = 1)
df['DateObserved'] = pd.to_datetime(df['DateObserved'])
df = df[['DateObserved','Ozone']]
df = df.set_index('DateObserved')
df_monthly = df.resample('M').mean()

# # explore shape of data and test for stationarity
# sns.lineplot(x = df['DateObserved'], y = df['Ozone'])
# sns.lineplot(x = df_monthly.index.values, y = df_monthly['Ozone'])
# plt.show()
# stationarity_test = adfuller(df['Ozone'])
# print(stationarity_test) # Data is stationary

# # explore parameters with ACF and PACF charts
# plot_acf(df_monthly['Ozone'], lags = 40)
# plot_pacf(df_monthly['Ozone'], lags = 20)
# plt.show()

arima_model=auto_arima(df_monthly,
 start_p=1, start_q=1,
 max_p=10, max_q=10,
 d=0, max_d=10,
 D=None,
 start_Q=0, max_Q=3,
 start_P = 0, max_P = 3,
 max_order=5, m=12, seasonal=True, stationary=True,
 trace=True,
 error_action= 'ignore',
 suppress_warnings=True,
 stepwise=True)

# generate index for plotting alongside historical
fcst_index = [np.datetime64('2020-11')]
for n in range(23):
    next_step = np.datetime64(fcst_index[-1]) + np.timedelta64(1,'M')
    fcst_index.append(next_step)

prediction = pd.DataFrame(arima_model.predict(n_periods = 24), index = fcst_index)

# # plot residuals
# resids = arima_model.resid()
# plot_acf(resids)
# plot_pacf(resids)
# plt.show()
#
# # plot predictions as extension of historical
# plt.plot(df_monthly, label = 'historical')
# plt.plot(prediction, label = 'forecast')
# plt.legend(loc='upper left')
# plt.show()
