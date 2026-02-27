'''
EJEMPLO BÁSICO DE PLOT EN BOKEH

Ignacio Díaz Blanco, 2020. Universidad de Oviedo

'''
import pandas as pd
import numpy as np
from bokeh.plotting import figure, output_file

from bokeh.io import show
from bokeh.models import Circle, Div, Paragraph, PreText, Range1d
from bokeh.layouts import row, column, layout

# archivo de salida (mismo nombre, extensión html)
filename = __file__.split('.')[0]+'.html'
output_file(filename)

# generamos los datos
t = np.linspace(0,10,1000)
x = np.cos(t)
y = np.sin(t)
z = np.sin(t+1)*0.5 + np.sin(3*t)*0.1 + np.sin(5*t)*0.1

# FIGURA
# creamos la figura
fig = figure(width=800,height=300)

# añadimos elementos a la figura
p1 = fig.line(t,x,line_width=3,line_alpha=0.5,legend_label='sin(t)')
p2 = fig.line(t,y,line_width=3,line_alpha=0.5,color='red',legend_label='cos(t)')
p3 = fig.line(t,z,line_width=5,line_alpha=0.5,color='green',legend_label='varios armónicos')


# ELEMENTO DE TEXTO
div = Div(text='''
	<h1>Ejemplo básico de plot</h1>
	<h4>Ignacio Díaz Blanco, 2020. Universidad de Oviedo</h4>
	<p><b>Ejemplo básico de plot en Bokeh</b>. Visualiza tres gráficas tipo <i>lineplot</i> con funciones básicas de interacción (zoom, pan, selección, etc.). Se ilustra la forma de mostrar texto html en un contenedor "div" y una figura interactiva de Bokeh
	</p>

	<a href="fuentes/%s">(código fuente)</a>'''%(__file__.split('.')[0]+'_codigofuente.html'),width=600)

# ORGANIZACIÓN DE LOS COMPONENTES: FIGURA, TEXTO
lay = layout([div,fig])


show(lay)