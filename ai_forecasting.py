import warnings
import itertools
import matplotlib
import matplotlib.pyplot as plt
import math
import pandas as pd
import statsmodels.api as sm
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import numpy as np

DEBUG = 1
PLOT_DEBUG = 3

def time_series_prophet(sales, index_col, target_col, period, holidays, country, flexibity, multi):
	print('## Time Series Modeling with Prophet')

	from fbprophet import Prophet

	y_sales = sales[target_col]
	sales = pd.DataFrame({index_col:y_sales.index, target_col:y_sales.values})
	sales = sales.rename(columns={index_col: 'ds', target_col: 'y'})
	sales_model = Prophet(yearly_seasonality=flexibity)
	if multi :
		sales_model = Prophet(yearly_seasonality=flexibity,seasonality_mode='multiplicative')
	if holidays :
		sales_model.add_country_holidays(country_name=country)
	sales_model.fit(sales)
  

	sales_forecast = sales_model.make_future_dataframe(periods=period)
	sales_forecast = sales_model.predict(sales_forecast)

	sales_model.plot(sales_forecast, xlabel = 'Date', ylabel = target_col)

	sales_model.plot_components(sales_forecast)
	plt.show()

def Time_Series_SARIMA(furniture, target_col, forecast_steps, p,d,q,m,sp,sd,sq):
	print("## Time series forecasting with SARIMA")
	y = furniture[target_col]
	mod = sm.tsa.statespace.SARIMAX(y,
								order=(p, d, q),
								seasonal_order=(m, sp, sd, sq),
								enforce_stationarity=False,
								enforce_invertibility=False)
	results = mod.fit(disp=False)

	print("Plot Time series forecasting with SARIMA")
	results.plot_diagnostics(figsize=(16, 8))
	plt.figure(1)
	plt.title("Time series forecasting plot_diagnostics with SARIMA(SARIMAX)")

	pred = results.get_prediction(dynamic=False)
	pred_ci = pred.conf_int()

	print('Plot ' + target_col + ' Forecast')
	plt.figure(2)
	plt.subplot(211)
	ax = y.plot(label='observed')

	ax.set_xlabel('Date')   
	ax.set_ylabel(target_col)
	
	plt.title(target_col + ' Forecast')
	plt.legend()

	pred_uc = results.get_forecast(steps=forecast_steps)
	pred_ci = pred_uc.conf_int()	
	print(pred_uc.summary_frame())	

	print('Plot ' + target_col + ' Forecast ' + str(forecast_steps) + ' steps')
	plt.subplot(212)
	pred_uc.predicted_mean.plot()
	plt.title(target_col + ' Forecast ' + str(forecast_steps) + 'steps')
	plt.legend()
	plt.figure(2)

	plt.show()


def	Time_Series_VARMA(endog,p,q,periods):
	mod = sm.tsa.VARMAX(endog, order=(p, q), error_cov_type='diagonal')
	res = mod.fit(maxiter=1000, disp=False)
	pred = res.predict()
	forecast = res.forecast(periods)

	if DEBUG > 0:
		print(res.summary())
	if DEBUG > 1:
		print("pred:")
		print(pred)

	if PLOT_DEBUG > 0:
		pred.columns = pred.columns + '_pred'
		forecast.columns = forecast.columns + '_pred'
		merged = endog
		merged[pred.columns] = pred
		#merged[forecast.columns] = forecast
		merged = pd.concat([merged, forecast], axis=0, sort=False)

		merged.plot()

		plt.title('VMA Forecasting Results')

		plt.show()

def	time_Read_Data(fname):
	"""
		Read Data from input file
	"""

	if DEBUG > 0:
		print("Read Data from file: ", fname)

	df = pd.read_excel(fname, index_col=None)

	if DEBUG > 1:
		print("df.head()")
		print(df.head())

	if DEBUG > 2:
		df.to_csv(fname + ".csv", index=False)

	return df

def	time_Read_Data2(fname):
	data = pd.read_csv(fname, index_col=None)#'YearMonth')

	if DEBUG > 0:
		print("Read csv file: ", fname)
		print(data)

	return data

def	Select_Index_Target(selected_data, index_col, target_col):

	#selected_data.drop(cols_to_remove, axis=1, inplace=True)
	selected_data = selected_data[[index_col, target_col]]	# Select only index_col and target_col

	if DEBUG > 0:
		date_min = selected_data[index_col].min()
		date_max = selected_data[index_col].max()

		print("min: ", date_min)
		print("max: ", date_max)

	selected_data = selected_data.sort_values(index_col)

	selected_data = selected_data.groupby(index_col)[target_col].sum().reset_index()

	selected_data = selected_data.set_index(index_col)

	return selected_data

def Find_ARIMA_Parameters(furniture, target_col):
	#
	# Parameter Selection for the ARIMA Time Series Model
	y = furniture[target_col]

	p = d = q = range(0, 2)
	pdq = list(itertools.product(p, d, q))
	seasonal_pdq = [(x[0], x[1], x[2], 12) for x in pdq]

	print('Examples of parameter combinations for Seasonal ARIMA...')
	print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[1]))
	print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[2]))
	print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[3]))
	print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[4]))
	
	warnings.filterwarnings("ignore")
	
	select_candi = 10000000
	param_candi = ( 0, 0, 0 )
	param_seasonal_candi = ( 0, 0, 0)

	count=0
	end_count=len(pdq)

	for param in pdq:
		for param_seasonal in seasonal_pdq:
			try:
				mod = sm.tsa.statespace.SARIMAX(y,
											order=param,
											seasonal_order=param_seasonal,
											enforce_stationarity=False,
											enforce_invertibility=False
											)
				results = mod.fit()
				count+=1
				if count<=5:
					print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))

				if results.aic + results.bic < select_candi:
					select_candi = results.aic + results.bic
					param_candi = param
					param_seasonal_candi = param_seasonal

			except:
				continue

	print(param_candi,param_seasonal,select_candi)
	return param_candi, param_seasonal
