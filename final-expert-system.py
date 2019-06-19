##########################################
###			Title: Super-inversionista MX
###			Author: Raúl González Cruz
##########################################
# API requests library
import requests
# Get actual date library
from datetime import date, timedelta
# Objects for sklearn
import numpy as np
# Plot a graph, show information
import matplotlib.pyplot as plt
from mpldatacursor import datacursor
# Linear regression libraries
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score

"""
This method allows us to get the data we require for predicting the price of dollar using
simple linear regression and mean squared error
"""
def get_prediction():
	# Get data from Banxico API
	# See token info at: https://www.banxico.org.mx/SieAPIRest/service/v1/token
	token = '152166c93cce260ee33662848411df5499a210215165a605734382241ba73c95'
	# Get actual date and set the historial period 
	today = date.today()
	start_day = today - timedelta(days=55)
	data_price = []
	#print(type(today))
	#print(start_day)
	print("\nObteniendo datos del tipo de cambio FIX proporcionado por Banxico...")
	url = 'https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF63528/datos/'+start_day.strftime("%Y-%m-%d")+'/'+today.strftime("%Y-%m-%d")+'?token='+token
	response = requests.get(url).json()
	print(response)

	# Clean data and obtain FIX data
	for element in response["bmx"]["series"]:
		for data in element["datos"]:
			data_price.append(float(data["dato"]))
	#print(len(data_price))

	# Lineal regression
	print("\nComenzando predicción del tipo de cambio para los siguientes dos días...")
	# assign training and test data
	index = [days for days in range(len(data_price))]
	future = [days for days in range(len(data_price),len(data_price)*2)]
	X_train = np.array(index).reshape((len(index), 1))
	y_train = np.array(data_price).reshape((len(data_price), 1))
	X_test = np.array(future).reshape((len(future), 1))

	# Create the object for lineal regression
	regr = linear_model.LinearRegression()

	# train the model
	regr.fit(X_train, y_train)

	# Make the prediction
	y_pred = regr.predict(X_test)

	# Show stadistics results
	print('\nPredicción finalizada. Se ha obtenido lo siguiente:')
	precision = regr.score(X_train, y_train)
	mean_error = mean_squared_error(y_train, y_pred)
	print('\nPrecisión del modelo: %.5f' % precision)
	print("Error cuadrático medio: %.2f" % mean_error)

	# Show algebraic model
	print('\nValor de la pendiente o coeficiente "a": \n', regr.coef_)
	# Este es el valor donde corta el eje Y (en X=0)
	print('Valor de la intersección o coeficiente "b": \n', regr.intercept_)
	print('La ecuación del modelo es igual a:')
	print('y = ', regr.coef_, 'x +', regr.intercept_)

	get_recommendations(precision,mean_error,y_pred)

	return X_train,y_train,X_test,y_pred,regr.coef_,regr.intercept_

"""
This method allows us to plot the model and the results
"""
def plot_results(X_train,y_train,X_test,y_pred,m,b):
	days = 3
	# Plot results: Model and prediction
	plt.scatter(X_train, y_train, label="Datos por FIX-Banxico")
	# Add prediction
	plt.scatter(X_test[0:days], y_pred[0:days], label="Datos por predicción")
	plt.legend()
	plt.grid(True)

	# Plot better regression line fit
	y = m*X_train + b
	plt.plot(X_train, y, color='red', linewidth=3, label='Línea de regresión')

	# Add more information
	plt.title('Serie histórica del tipo de cambio FIX peso-dólar')
	plt.xlabel('Día')
	plt.ylabel('Precio del dólar')

	# Allow hover information
	datacursor()
	plt.show()

"""
This method allows us to establish some recomendations for the users
"""
def get_recommendations(precision,mean_error,y_pred):
	print("\nCon base en los resultados, establezco lo siguiente:")
	# Get real-time price of dollar
	url = 'https://free.currconv.com/api/v7/convert?q=USD_MXN&compact=ultra&apiKey=2b7853bf32f13babcf52'
	response = requests.get(url).json()
	print(response["USD_MXN"])
	actual_value = response["USD_MXN"]

	# Rule checker
	#Precisión dudosa, buen rango de variación
	if precision.item() < 0.4:
		if (actual_value - y_pred[0]) <= mean_error.item() or (actual_value - y_pred[1]) <= mean_error.item():
			print("Dado que la precisión fue menor al 50%, es recomendable que evalue más días para asegurarte una compra.")
		else:
			print("Dado que la precisión fue menor al 50% y no se obtuvo un buen valor estimado al real, es recomendable que me preguntes mañana.")
	else:
		if (actual_value - y_pred[0]) <= mean_error.item():
			if (actual_value - y_pred[0]) < (actual_value - y_pred[1]):
				print("Es recomendable comprar ahora.")
			elif (actual_value - y_pred[0]) > (actual_value - y_pred[1]) and (actual_value - y_pred[1]) <= mean_error.item():
				print("Es recomendable comprar mañana.")
		
		elif (actual_value - y_pred[1]) <= mean_error.item():
			if (actual_value - y_pred[0]) > (actual_value - y_pred[1]):
				print("Es recomendable comprar mañana.")
			elif (actual_value - y_pred[0]) < (actual_value - y_pred[1]) and (actual_value - y_pred[0]) <= mean_error.item():
				print("Es recomendable comprar hoy.")	
		else:
			print("No es recomendable comprar en estos dos días. Vuelve a preguntar mañana.")



"""
Main function of the program. Starts the execution of our expert system
"""
if __name__ == "__main__":
	# Welcome message
	print("\n¡Bienvenido! Mi nombre es Superin MX y le aconsejaré oportunidades de trading de la divisa USD-MXN")
	# Execute prediction
	X_train,y_train,X_test,y_pred,m,b = get_prediction()
	# Plot results
	plot_results(X_train,y_train,X_test,y_pred,m,b)



