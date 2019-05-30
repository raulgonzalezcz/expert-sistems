# Final project: Superinversionista MX
# API requests library
import requests
# Get actual date library
from datetime import date, timedelta
import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
from mpldatacursor import datacursor
# Linear regression libraries
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score

# Get data
# See token info at: https://www.banxico.org.mx/SieAPIRest/service/v1/token
token = '152166c93cce260ee33662848411df5499a210215165a605734382241ba73c95'
today = date.today()
start_day = today - timedelta(days=30)
data_price = []
#print(type(today))
#print(start_day)
url = 'https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF63528/datos/'+start_day.strftime("%Y-%m-%d")+'/'+today.strftime("%Y-%m-%d")+'?token='+token
response = requests.get(url).json()
print(response)

# Clean data and obtain FIX data
for element in response["bmx"]["series"]:
	for data in element["datos"]:
		data_price.append(float(data["dato"]))
#print(len(data_price))

# Lineal regression

# Asignamos nuestra variable de entrada X para entrenamiento y las etiquetas Y.
index = [days for days in range(len(data_price))]
X_train = np.array(index).reshape((len(index), 1))
y_train = np.array(data_price).reshape((len(data_price), 1))

# Creamos el objeto de Regresión Linear
regr = linear_model.LinearRegression()

# Entrenamos nuestro modelo
regr.fit(X_train, y_train)

# Hacemos las predicciones que en definitiva una línea (en este caso, al ser 2D)
y_pred = regr.predict(y_train)


# Veamos los coeficienetes obtenidos, En nuestro caso, serán la Tangente
print()
print('DATOS DEL MODELO REGRESIÓN LINEAL SIMPLE')
print('Valor de la pendiente o coeficiente "a": \n', regr.coef_)
# Este es el valor donde corta el eje Y (en X=0)
print('Valor de la intersección o coeficiente "b": \n', regr.intercept_)
# Error Cuadrado Medio
print("Error cuadrático medio: %.2f" % mean_squared_error(y_train, y_pred))
# Puntaje de Varianza. El mejor puntaje es un 1.0
print('Varianza: %.2f' % r2_score(y_train, y_pred))
print('La ecuación del modelo es igual a:')
print('y = ', regr.coef_, 'x +', regr.intercept_)
print()
print('Precisión del modelo:')
print(regr.score(X_train, y_train))

# Graficar resultados
#Graficamos los datos junto con el modelo
fig, ax = plt.subplots()
ax.scatter(X_train, y_pred)
ax.set_title('Serie histórica del tipo de cambio FIX peso-dólar')
crs = mplcursors.cursor(ax,hover=True)

crs.connect("add", lambda sel: sel.annotation.set_text(
    'Point {},{}'.format(sel.target[0], sel.target[1])))


plt.xlabel('Día')
plt.ylabel('Precio del dólar')
plt.show()



