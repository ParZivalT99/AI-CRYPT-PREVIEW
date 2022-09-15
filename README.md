# AI CRYPT PREVIEW
[Read in English](#english-version)

Este proyecto es una version diferente al proyecto original.

**Proyecto original  (AI CRYPT) - privado:**
	- Autores: [Marcos Montes](https://github.com/ParZivalT99) - [Alexander Pabon](https://github.com/Warriors2021)
	
	Algoritmo predictivo de la tendencia del Bitcoin 
	con visualización en una aplicación web,desarrollado 
	en Django y usando MongoDB como base de datos.

**Este proyecto (AI CRYPT PREVIEW)  :**

	Es igual en todos los aspectos al proyecto original,
	a excepción que NO hace uso de un algoritmo predictivo, 
	en cambio, se simula una predicción ficticia con el fin
	de poder usar y mostrar la Aplicación Web.

**Ambos proyectos se desarrollaron con fines de aprendizaje**
## Requisitos
1. Tener MongoDB instalado 
2. Tener una api key en [cryptowat.ch](cryptowat.ch) 

## Funcionamiento
1.  Instalar el archivo local.txt que esta en la carpeta requemients, para instalar los package que usa el proyecto.
2. Hacer las migraciones
3. En el archivo secret.json agregar la siguiente url ``https://api.cryptowat.ch/markets/coinbase-pro/btcusd/ohlc?apikey=API_KEY`` en el campo que se llama ``API_CONECTION_URL``

4. abrir el shell de Django y escribir lo siguiente:
	```
	>>>from data_test.MLdata import MLData
	>>>data = MLData()

	#llenar la base de datos con los datos historicos del BTC
	>>>data.insert_data()
	```
5. Usar la Aplicación Web

## Resumen técnico
- Python
- Django
- MongoDB
- HTML
- CSS
- Bootstrap
- JavaScript

## Autor
- [Marcos Montes](https://www.github.com/https://github.com/ParZivalT99)

# English version

This project is a different version of the original project.

**Original Project (AI CRYPT) - private :**
		- Authors: [Marcos Montes](https://github.com/ParZivalT99) - [Alexander Pabon](https://github.com/Warriors2021)
	
	Bitcoin trend predictive algorithm with visualization in a 
	web application, developed in Django and using MongoDB as
	database.

**This project (AI CRYPT PREVIEW) :**

	It is the same in all aspects as the original project,
	except that it does NOT make use of a predictive algorithm, 
	instead it simulates a fictitious prediction in order to be 
	able to use and display the Web Application.

**Both projects were developed for learning purposes**
## Requirements
1. Have MongoDB installed .
2. Have an api key in [cryptowat.ch](cryptowat.ch) .

## Run Locally
1.  Install the local.txt file that is in the requirements folder, to install the packages used by the project.
2. To make the migrations.
3. In the secret.json file add the following url ``https://api.cryptowat.ch/markets/coinbase-pro/btcusd/ohlc?apikey=API_KEY`` in the field named ``API_CONECTION_URL``.

4. Open the Django shell and type the following:
	```
	>>>from data_test.MLdata import MLData
	>>>data = MLData()

	#fill the database with the historical data of the BTC.
	>>>data.insert_data()
	```
5. Use the Web Application.

## Technical summary
- Python
- Django
- MongoDB
- HTML
- CSS
- Bootstrap
- JavaScript

## Author
- [Marcos Montes](https://github.com/ParZivalT99)
