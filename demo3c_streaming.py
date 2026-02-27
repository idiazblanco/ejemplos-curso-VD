'''
Visualización en streaming

Ignacio Díaz Blanco, 2020. Universidad de Oviedo

- Se define el objeto "source" con datos, vinculados a una figura tipo plot
- Se define un evento periódico (add_periodic_callback)
- en ese evento se ejecuta una callback (update) que añade, uno a uno, registros a "source"

Notas:
En la callback update se incluye acceso a datos opendata en 
streaming para añadir datos "al vuelo" (ej. datos de contaminación en 
datos.gijon.es, que son actualizados cada hora)
'''

import pandas as pd
import numpy as np
from bokeh.io import curdoc
from bokeh.server.server import Server
from bokeh.application import Application
from bokeh.application.handlers.function import FunctionHandler
from bokeh.plotting import figure, ColumnDataSource
from bokeh.layouts import layout
from bokeh.models import Div


# Creamos un dataframe con los datos que vamos a analizar (columna de tiempo y dos variables, v1 y v2)
N  = 100
tm = 0.1
t  = np.arange(0,N)*tm
x  = np.random.randn(N)
y  = np.random.randn(N)
z  = np.random.randn(N)
df = pd.DataFrame({'x':x, 'y':y, 'z':z},t)

df.index.name = 't'

i = t[-1]

# varible global que indica la muestra actual


# definimos la estructura de datos ("source") que estará vinculada a las gráficas:
# ... si esta estructura cambia, la gráfica cambia
source = ColumnDataSource(df)

# función por evento: en este caso, evento periódico cada 10ms
# esta función cambia "source", lo que motivará que se actualicen las gráficas
def update():
	global i
	i = i + tm
	t = i
	x = np.sin(t)
	y = np.cos(t)
	z = np.sin(t) + 0.3*np.sin(3*t) + 0.5*np.cos(5*t+1)

	import requests
	import json


	# http://datos.santander.es/api/datos/sensores_smart_env_monitoring/400.json
	# http://datos.santander.es/api/datos/sensores_smart_env_monitoring/250.json
	# datos = json.loads(requests.get('http://datos.santander.es/api/datos/sensores_smart_env_monitoring/250.json').text)

	print('cargando datos de ayto Santander ...')
	# datos = json.loads(requests.get('http://datos.santander.es/api/rest/datasets/sensores_smart_mobile.json').text)
	datos1 = json.loads(requests.get('http://datos.santander.es/api/datos/sensores_smart_env_monitoring/400.json').text)
	datos2 = json.loads(requests.get('http://datos.santander.es/api/datos/sensores_smart_env_monitoring/250.json').text)

	x = float(datos1['resources'][0]['ayto:temperature'])
	y = float(datos1['resources'][0]['ayto:light'])
	z = float(datos2['resources'][0]['ayto:temperature'])

	print(x)

	new = {'t': [t],  'x': [x], 'y': [y], 'z': [z]}
	# new = {'t': [t],  'x': [x], 'y': [y], 'z': [z]}
	source.stream(new,rollover=N)


# definimos el evento periódico cada 10ms y utilizamos la función update() como callback
curdoc().add_periodic_callback(update, 2000)

# definimos la figura y gráficas que serán vinculadas a "source" 
fig1 = figure(width=900,height=200,title='NO2',tools="crosshair,box_select,pan,reset,xwheel_zoom")
fig1.line(source=source, x='t', y='x')
fig2 = figure(width=900,height=200,title='Ozono', x_range = fig1.x_range,tools="crosshair,box_select,pan,reset,xwheel_zoom")
fig2.line(source=source, x='t', y='y')
fig3 = figure(width=900,height=200,title='Temperatura', x_range = fig1.x_range,tools="crosshair,box_select,pan,reset,xwheel_zoom")
fig3.line(source=source, x='t', y='z')


# ELEMENTO DE TEXTO
div = Div(text='''
<h1>Visualización en streaming
</h1>
<h4>Ignacio Díaz Blanco, 2020. Universidad de Oviedo</h4>

<ul>
<li>Se define el objeto "source" con datos, vinculados a una figura tipo plot</li>
<li>Se define un evento periódico (add_periodic_callback)</li>
<li>en ese evento se ejecuta una callback (update) que añade, uno a uno, registros a "source"</li>
</ul>

<p>Notas:
En la callback update se incluye acceso a datos opendata en 
streaming para añadir datos "al vuelo" (ej. datos de contaminación en 
datos.gijon.es, que son actualizados cada hora)</p>
<a href="fuentes/%s">(código fuente)</a>'''%(__file__.split('.')[0]+'_codigofuente.html'),width=700)


# título del documento
curdoc().title = "actualización online"

# añadimos la figura al documento
curdoc().add_root(layout([fig1,fig2,fig3]))