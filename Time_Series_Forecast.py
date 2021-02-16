
#from config_gui_pm import *		# Configuration of the GUI, PyQt Ver. 4 or 5

#if PYQT_VER == 5:
#	from PyQt5 import *
#	from PyQt5.QtCore import *
#	from PyQt5.QtGui import *
#	from PyQt5.QtWidgets import *
#	from MenuBar_Grid import *
#elif PYQT_VER == 4:
#	from PyQt4 import *
#	#from PyQt4 import QtGui, QtCore
#	from PyQt4.QtCore import *
#	from PyQt4.QtGui import *
#	from MenuBar_Grid5 import *
#else:
#	print("Unexpected PYQT_VER: ", PYQT_VER)
#	exit(0)

#from MenuBar_Grid import *

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
'''
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import pandas as pd
import datetime
from dateutil import parser
from pandas.plotting import scatter_matrix
'''
import ai_forecasting

# Time Series Dialog
class TS_Forecast_Dialog(QWidget):
	def __init__(self, inputs, outputs, df):
		super().__init__()
		self.initUI(inputs, outputs, df)

	def initUI(self, inputs, outputs, df):
		#print("inputs: ", inputs)
		#print("outputs: ", outputs)
		#print("df: ", df.describe())
		#period
		self.periodLabel=QLabel('Period')
		self.periodSet=QSpinBox()
		self.periodSet.setMinimum(1)
		self.periodSet.setMaximum(10000)
		self.periodSet.setValue(50)
		self.periodSet.setSingleStep(10)

		#models
		self.modelLabel=QLabel('Model')
		self.modelSet=QComboBox()
		self.modelSet.addItem('Prophet')
		self.modelSet.addItem('ARIMA')
		self.modelSet.addItem('SARIMA')
		self.modelSet.addItem('VAR')
		#self.modelSet.addItem('VARMA')
		self.modelSet.activated.connect(self.disabling)

		#prophet
		self.holidayCheck=QCheckBox('Holidays')
		self.countryLabel=QLabel('Country')
		self.countrySet=QComboBox()
		self.countrySet.addItem('KR')
		self.countrySet.addItem('IN')
		self.countrySet.addItem('EG')
		self.countrySet.addItem('CN')
		self.countrySet.addItem('RU')
		self.countrySet.addItem('US')
		self.weightLabel=QLabel('Holiday\'s weight')
		self.weightSet=QDoubleSpinBox()
		self.weightSet.setMinimum(0.01)
		self.weightSet.setMaximum(20)
		self.weightSet.setValue(10)		
		self.flexLabel=QLabel('Flexibity')
		self.flexSet=QDoubleSpinBox()
		self.flexSet.setMinimum(0.01)
		self.flexSet.setMaximum(20)
		self.flexSet.setValue(0.05)
		self.multiCheck=QCheckBox('Multiplicable Seasonality')

		#ARIMA
		self.arLabel=QLabel('AR')
		self.iLabel=QLabel('I')
		self.maLabel=QLabel('MA')
		self.arSet=QSpinBox()
		self.arSet.setMinimum(0)
		self.arSet.setMaximum(20)
		self.arSet.setValue(1)
		self.iSet=QSpinBox()
		self.iSet.setMinimum(0)
		self.iSet.setMaximum(2)
		self.iSet.setValue(1)
		self.maSet=QSpinBox()
		self.maSet.setMinimum(0)
		self.maSet.setMaximum(20)
		self.maSet.setValue(1)
		
		#SARIMA
		self.autoCheck=QCheckBox('SARIMA Para AutoSet')
		self.mLabel=QLabel('M')
		self.pLabel=QLabel('P')
		self.dLabel=QLabel('D')
		self.qLabel=QLabel('Q')
		self.mSet=QSpinBox()
		self.mSet.setMinimum(0)
		self.mSet.setMaximum(20)
		self.mSet.setValue(12)
		self.pSet=QSpinBox()
		self.pSet.setMinimum(0)
		self.pSet.setMaximum(20)
		self.pSet.setValue(1)
		self.dSet=QSpinBox()
		self.dSet.setMinimum(0)
		self.dSet.setMaximum(2)
		self.dSet.setValue(1)
		self.qSet=QSpinBox()
		self.qSet.setMinimum(0)
		self.qSet.setMaximum(20)
		self.qSet.setValue(0)

		#VARMA
		self.varLabel=QLabel('VARMA-P')
		self.vmaLabel=QLabel('VARMA-Q')
		self.varSet=QSpinBox()
		self.varSet.setMinimum(0)
		self.varSet.setMaximum(20)
		self.varSet.setValue(2)
		self.vmaSet=QSpinBox()
		self.vmaSet.setMinimum(0)
		self.vmaSet.setMaximum(20)
		self.vmaSet.setValue(0)

		#button
		self.forecastButton=QPushButton('Forecast')
		self.forecastButton.clicked.connect(lambda: self.doForecast(inputs,outputs,df))
		self.cancelButton=QPushButton('Cancel')
		self.cancelButton.clicked.connect(QCoreApplication.instance().quit)

		#Basic
		self.initialDisabling()
		self.boxlayout()
		self.setWindowTitle('Forecast')
		self.center()
		self.resize(400, 500)
		self.show()

	def initialDisabling(self):
		self.holidayCheck.setEnabled(True)
		self.countrySet.setEnabled(True)
		self.weightSet.setEnabled(True)
		self.flexSet.setEnabled(True)
		self.multiCheck.setEnabled(True)
		self.arSet.setEnabled(False)
		self.iSet.setEnabled(False)
		self.maSet.setEnabled(False)
		self.mSet.setEnabled(False)
		self.pSet.setEnabled(False)
		self.dSet.setEnabled(False)
		self.qSet.setEnabled(False)
		self.autoCheck.setEnabled(False)
		self.varSet.setEnabled(False)
		self.vmaSet.setEnabled(False)

	def disabling(self):
		model=self.modelSet.currentIndex()
		self.holidayCheck.setEnabled(False)
		self.countrySet.setEnabled(False)
		self.weightSet.setEnabled(False)
		self.flexSet.setEnabled(False)
		self.multiCheck.setEnabled(False)
		self.arSet.setEnabled(False)
		self.iSet.setEnabled(False)
		self.maSet.setEnabled(False)
		self.mSet.setEnabled(False)
		self.pSet.setEnabled(False)
		self.dSet.setEnabled(False)
		self.qSet.setEnabled(False)
		self.varSet.setEnabled(False)
		self.vmaSet.setEnabled(False)

		if model==0:
			print("Prophet")
			self.holidayCheck.setEnabled(True)
			self.countrySet.setEnabled(True)
			self.weightSet.setEnabled(True)
			self.flexSet.setEnabled(True)
			self.multiCheck.setEnabled(True)
		elif model==1:
			print("ARIMA")
			self.arSet.setEnabled(True)
			self.iSet.setEnabled(True)
			self.maSet.setEnabled(True)
		elif model==2:
			print("SARIMA")
			self.arSet.setEnabled(True)
			self.iSet.setEnabled(True)
			self.maSet.setEnabled(True)
			self.mSet.setEnabled(True)
			self.pSet.setEnabled(True)
			self.dSet.setEnabled(True)
			self.qSet.setEnabled(True)
			self.autoCheck.setEnabled(True)
		elif model==3:
			print("VAR")
			self.varSet.setEnabled(True)
		elif model==4:
			print("VARMA")
			self.varSet.setEnabled(True)
			self.vmaSet.setEnabled(True)
	
	def timeError(self):
		msg=QMessageBox()
		msg.setIcon(QMessageBox.Information)

		msg.setWindowTitle("Column Set Error")
		msg.setText("'setup - select columns' should be done correctly\n")
		msg.setInformativeText("One time input\nOne (VAR-more than one) numeric type output")
		msg.setStandardButtons(QMessageBox.Ok)

		retval = msg.exec_()

	def doForecast(self,inputs,outputs,df):
		
		print("inputs: ", inputs)
		print("outputs: ", outputs)
		print("df: ", df.describe())
		
		if(len(inputs)!=1 or len(outputs)<1):
			self.timeError()
			return
		
		period=self.periodSet.value()	  
		model=self.modelSet.currentIndex()

		holiday=self.holidayCheck.isChecked()
		countryNumb=self.countrySet.currentIndex()
		if countryNumb==0:
			country='KR'
		elif countryNumb==1:
			country='IN'
		elif countryNumb==2:
			country='EG'
		elif countryNumb==3:
			country='CN'
		elif countryNumb==4:
			country='RU'
		elif countryNumb==5:
			country='US'
		flexibity=self.flexSet.value()
		multival=self.multiCheck.isChecked()

		AR=self.arSet.value()
		I=self.iSet.value()
		MA=self.maSet.value()

		m=self.mSet.value()
		sp=self.pSet.value()
		sd=self.dSet.value()
		sq=self.qSet.value()

		p=self.varSet.value()
		q=self.vmaSet.value()


		sales = ai_forecasting.Select_Index_Target(df,inputs[0],outputs[0])
		
		org_cols = ['0', '1', '2', 'Total']

		if model<3:
			if(len(outputs)>1):
				self.timeError()
				return
		else:
			if(len(outputs)<2):
				self.timeError()
				return		

		if model==0:
			print("Prophet")
			print(holiday,country,flexibity,multival)
			ai_forecasting.time_series_prophet(sales,inputs[0],outputs[0],period,holiday,country,flexibity,multival)

		elif model==1:
			print("ARIMA")
			print(AR,I,MA)
			ai_forecasting.Time_Series_SARIMA(sales,outputs[0],period,AR,I,MA,0,0,0,0)

		elif model==2:
			print("SARIMA")
			if self.autoCheck.isChecked():
				pdq, spdq = ai_forecasting.Find_ARIMA_Parameters(sales,outputs[0])
				AR=pdq[0]
				I=pdq[1]
				MA=pdq[2]
				sp=spdq[0]
				sd=spdq[1]
				sq=spdq[2]
				m=spdq[3]
			print(AR,I,MA,sp,sd,sq,m)
			ai_forecasting.Time_Series_SARIMA(sales,outputs[0],period,AR,I,MA,sp,sd,sq,m)

		elif model==3:
			print("VAR")
			print(p)
			ai_forecasting.Time_Series_VARMA(df[outputs].astype(float),p,0,period)

		elif model==4:
			print("VARMA")
			print(p,q)
			ai_forecasting.Time_Series_VARMA(df[outputs].astype(float),p,q,period)

		print(period)
		#self.reject()
		

	def boxlayout(self):
		periodBox=QHBoxLayout()
		periodBox.addStretch(2)
		periodBox.addWidget(self.periodLabel)
		periodBox.addWidget(self.periodSet)
		periodBox.addStretch(2)

		modelBox=QHBoxLayout()
		modelBox.addStretch(1)
		modelBox.addWidget(self.modelLabel)
		modelBox.addWidget(self.modelSet)
		modelBox.addStretch(1)

		buttonBox=QHBoxLayout()
		buttonBox.addStretch(1)
		buttonBox.addWidget(self.cancelButton)
		buttonBox.addWidget(self.forecastButton)
		buttonBox.addStretch(1)

		holidayBox=QHBoxLayout()
		holidayBox.addWidget(self.holidayCheck)
		holidayBox.addWidget(self.countryLabel)
		holidayBox.addWidget(self.countrySet)
		holidayBox.addStretch(1)
		
		weightBox=QHBoxLayout()
		weightBox.addWidget(self.weightLabel)
		weightBox.addWidget(self.weightSet)
		weightBox.addStretch(1)

		flexBox=QHBoxLayout()
		flexBox.addWidget(self.flexLabel)
		flexBox.addWidget(self.flexSet)
		flexBox.addStretch(1)

		arimaBox=QHBoxLayout()
		arimaBox.addWidget(self.arLabel)
		arimaBox.addWidget(self.arSet)
		arimaBox.addWidget(self.iLabel)
		arimaBox.addWidget(self.iSet)
		arimaBox.addWidget(self.maLabel)
		arimaBox.addWidget(self.maSet)
		arimaBox.addStretch(1)

		sarimaBox=QHBoxLayout()
		sarimaBox.addWidget(self.mLabel)
		sarimaBox.addWidget(self.mSet)
		sarimaBox.addWidget(self.pLabel)
		sarimaBox.addWidget(self.pSet)
		sarimaBox.addWidget(self.dLabel)
		sarimaBox.addWidget(self.dSet)
		sarimaBox.addWidget(self.qLabel)
		sarimaBox.addWidget(self.qSet)
		sarimaBox.addStretch(1)

		varmaBox=QHBoxLayout()
		varmaBox.addWidget(self.varLabel)
		varmaBox.addWidget(self.varSet)
		varmaBox.addWidget(self.vmaLabel)
		varmaBox.addWidget(self.vmaSet)
		varmaBox.addStretch(1)

		vbox=QVBoxLayout()
		vbox.addLayout(periodBox)
		vbox.addLayout(modelBox)
		vbox.addLayout(holidayBox)
		vbox.addLayout(weightBox)
		vbox.addLayout(flexBox)
		vbox.addWidget(self.multiCheck)
		vbox.addLayout(arimaBox)
		vbox.addLayout(sarimaBox)
		vbox.addWidget(self.autoCheck)
		vbox.addLayout(varmaBox)
		vbox.addStretch()
		vbox.addLayout(buttonBox)
		self.setLayout(vbox)

	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

if __name__=='__main__':

	fname='./Data/AirPassengers.csv'
	df=ai_forecasting.time_Read_Data2(fname)
	inputs=['Month']
	outputs=['#Passengers']

	app=QApplication(sys.argv)
	ex=TS_Forecast_Dialog(inputs,outputs,df)
	sys.exit(app.exec_())