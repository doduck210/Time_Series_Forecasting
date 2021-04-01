# Time_Series_Forecasting   

it can be run by command "python3 Time_Series_Forecast.py"   
default data is air_passenger   

You can forecast any csv or xls files from : Time_Series_Forecast.py/__main__ -> fname (csv:time_Read_Data, xls:time_Read_Data2)    

required packages : PyQt5, matplotlib, pandas, statsmodels, numpy, fbprophet, plotly   

There are Prophet, (S)ARIMA, VAR forecasting models in it.   
There is SARIMA Parameter autoset feature, which is using Grid search finding minimum sum of aic and bic. It may takes a few seconds to run with this feature.     

Its guidance is available from Guide.pptx(https://github.com/doduck210/Time_Series_Forecasting/blob/master/Guide.pptx)
