'''
EJEMPLO BÁSICO DE FUENTES DE DATOS EN BOKEH

Ignacio Díaz Blanco, 2020. Universidad de Oviedo

'''
import pandas as pd
import numpy as np
from bokeh.plotting import figure, output_file

from bokeh.io import show
from bokeh.models import Div, ColumnDataSource
from bokeh.layouts import row, column, layout

# archivo de salida (mismo nombre, extensión html)
filename = __file__.split('.')[0]+'.html'
output_file(filename)




from scipy.io import loadmat
print('cargando datos ...')
d = loadmat('dataicann.mat')

# obtener ensayo 2
datos = d['z'][0][7]

# frecuencia y periodo de muestreo
fm = 5000.0
tm = 1/fm

# número de muestras
N  = datos.shape[0]

# vector de tiempos
t  = np.arange(0,N)*tm

# corrientes y aceleraciones
ax  = datos[:,1]
ay  = datos[:,2]
iR  = datos[:,3]
iS  = datos[:,4]


# SOURCE: FUENTE COMÚN DE DATOS
# el source puede verse como una tabla 
# en este caso, tiene N muestras y atributos 'x', 'y', 'z'
datos = {
	't': t,
	'ax': ax,
	'ay': ay,
	'iR': iR,
	'iS': iS
}

# generamos el objeto "source"
source = ColumnDataSource(datos)

# este objeto es una "fuente de datos" común
# que "sincroniza" todas las figuras
# cualquier cambio en los datos (modificación, selección)
# es inmediatamente actualizado por Boheh en 
# todas las figuras que tengan esa fuente


# FIGURA
# creamos la figura
f1 = figure(width=300,height=300
			,tools="crosshair,box_select,pan,reset,wheel_zoom,lasso_select"
			,x_axis_label='ax(t)',y_axis_label='ay(t)')
p1 = f1.circle(x='ax', y='ay', source=source,radius=.02,line_width=0,line_alpha=0.5)

f2 = figure(width=300,height=300,
		tools="crosshair,box_select,pan,reset,wheel_zoom"
		,x_axis_label='iR(t)',y_axis_label='iS(t)')
p2 = f2.circle(x='iR', y='iS', source=source,radius=.02,line_width=0,line_alpha=0.5)

f3 = figure(width=600,height=300,tools="crosshair,box_select,pan,reset,wheel_zoom"
			,x_axis_label='t',y_axis_label='iR(t)')
p3 = f3.circle(x='t', y='iR', source=source,radius=.02,line_width=0,line_alpha=0.5)


# ELEMENTO DE TEXTO
div = Div(text='''
<h1>Ejemplo básico de plot → variante "dataicann"</h1>
<h4>Ignacio Díaz Blanco, 2021. Universidad de Oviedo</h4>
<b>Uso de fuentes de datos (source)</b>
<table>
<td valign="top">
<p>En este ejemplo, utilizamos una fuente de datos
mediante el objeto <i>source</i>. El objeto <i>source</i> puede verse como una tabla 
en este caso, tiene <i>N</i> muestras y atributos <i>'t', 'ax', 'ay','ir','is'</i>
</p>
<p>Este objeto es una "fuente de datos" común
que "sincroniza" todas las figuras
cualquier cambio en los datos (modificación, selección)
es inmediatamente actualizado por Boheh en 
todas las figuras que tengan esa fuente</p>
</td>

<td valign="top">
<p>Prueba a seleccionar una parte en una de las figuras. 
Verás que en el resto de las figuras quedan los elementos 
seleccionados consistentemente. Esto se llama en interacción "linking"</p>	
</td>
</table>
<a href="fuentes/%s">(código fuente)</a>'''%(__file__.split('.')[0]+'_codigofuente.html'),width=700)

# ORGANIZACIÓN DE LOS COMPONENTES: FIGURA, TEXTO
lay = layout([
	[div],
	[f1,f2,f3]
	])


show(lay)