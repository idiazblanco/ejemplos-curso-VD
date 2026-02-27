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


# importamos datos de aceleraciones y corrientes de motor
from scipy.io import loadmat
print('cargando datos ...')
d = loadmat('dataicann.mat')

'''
DESCRIPCIÓN DE LOS ENSAYOS
	ensayo 0: asimetría mecánica
	ensayo 1: asimetría eléctrica + mecánica
	ensayo 2: normal
	ensayo 3: asimetría eléctica 10 ohm
	ensayo 4: asimetría eléctica 15 ohm
	ensayo 5: asimetría eléctica 20 ohm
	ensayo 6: asimetría eléctica 5 ohm
	ensayo 7: fallo eléctrico gradual (sube y baja)
	ensayo 8: fallo eléctrico gradual (sube)
'''


# obtener ensayo 2
datos = d['z'][0][2]

# frecuencia de muestreo y periodo de muestreo
fm = 5000.0
tm = 1/fm


N  = datos.shape[0]

# vector de tiempos
t  = np.arange(0,N)*tm

# datos a visualizar
ax  = datos[:,1]			# aceleración ax
iR  = datos[:,3]			# corriente iR
iS  = datos[:,4]			# corriente iS

print('visualizando ...')



# FIGURA
# creamos figura en Bokeh
fig1 = figure(width=800,height=300,tools="crosshair,xpan,reset,xwheel_zoom",title='Vibraciones',x_axis_label='tiempo (s)')

# añadimos elementos a la figura (plot tipo línea)
p1 = fig1.line(t,ax,line_width=3,line_alpha=0.5,legend_label='ax(t)')


# creamos figura en Bokeh
fig2 = figure(width=800,height=300,tools="crosshair,xpan,reset,xwheel_zoom",x_range=fig1.x_range, title='Corrientes',x_axis_label='tiempo (s)')
p2 = fig2.line(t,iR,line_width=3,line_alpha=0.5,color='red',legend_label='iR(t)')
p3 = fig2.line(t,iS,line_width=5,line_alpha=0.5,color='green',legend_label='iS(t)')


# ELEMENTO DE TEXTO
div = Div(text='''
	<h1>Plot básico: visualización de datos de motor de inducción</h1>
	<h4>Ignacio Díaz Blanco, 2021. Universidad de Oviedo</h4>
	<p>Visualización de datos de corrientes y aceleraciones de un motor de inducción. Incorpora:
	</p>
	<ul>
		<li>Visualización de datos reales de un motor de inducción (corrientes y vibraciones)</li>
		<li>Restricción horizontal de zoom y desplazamiento</li>
		<li>Ejes enlazados: los ejes x de ambas figuras están coordinados entre sí</li>
	</ul>

	<a href="fuentes/%s">(código fuente)</a>'''%(__file__.split('.')[0]+'_codigofuente.html'),width=600)

# ORGANIZACIÓN DE LOS COMPONENTES: FIGURA, TEXTO
lay = layout([div,fig1,fig2])


show(lay)