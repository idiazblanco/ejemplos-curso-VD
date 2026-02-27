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

# generamos los datos
N = 1000
t = np.linspace(0,10,N)
x = np.cos(t)
y = np.sin(t)
z = np.sin(t+1)*0.5 + np.sin(3*t)*0.1 + np.sin(5*t)*0.1



# SOURCE: FUENTE COMÚN DE DATOS
# el source puede verse como una tabla 
# en este caso, tiene N muestras y atributos 'x', 'y', 'z'
datos = {
	'x': x,
	'y': y,
	'z': z
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
f1 = figure(width=300,height=300,tools="crosshair,box_select,pan,reset,wheel_zoom")
p1 = f1.circle(x='x', y='y', source=source,radius=.02,line_width=0,line_alpha=0.5,legend_label='x-y')

f2 = figure(width=300,height=300,tools="crosshair,box_select,pan,reset,wheel_zoom")
p2 = f2.circle(x='x', y='z', source=source,radius=.02,line_width=0,line_alpha=0.5,legend_label='x-z')

f3 = figure(width=300,height=300,tools="crosshair,box_select,pan,reset,wheel_zoom")
p3 = f3.circle(x='y', y='z', source=source,radius=.02,line_width=0,line_alpha=0.5,legend_label='y-z')


# ELEMENTO DE TEXTO
div = Div(text='''
<h1>Ejemplo de selecciones enlazadas</h1>
<h4>Ignacio Díaz Blanco, 2021. Universidad de Oviedo</h4>
<table>
<td valign="top">
<p>En este ejemplo, utilizamos una fuente de datos
mediante el objeto <i>source</i>. El objeto <i>source</i> puede verse como una tabla 
en este caso, tiene <i>N</i> muestras y atributos <i>'x', 'y', 'z'</i>
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