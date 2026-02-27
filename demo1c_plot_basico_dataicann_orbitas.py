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

# frecuencia y periodo de muestreo
fm = 5000.0
tm = 1/fm
N  = datos.shape[0]
t  = np.arange(0,N)*tm


# datos de un ensayo
ensayo = 2
ax1 = d['z'][0][ensayo][:15000,1]
ay1 = d['z'][0][ensayo][:15000,2]
iR1 = d['z'][0][ensayo][:15000,3]
iS1 = d['z'][0][ensayo][:15000,4]

# datos de otro ensayo
ensayo = 0
ax2 = d['z'][0][ensayo][:5000,1]
ay2 = d['z'][0][ensayo][:5000,2]
iR2 = d['z'][0][ensayo][:5000,3]
iS2 = d['z'][0][ensayo][:5000,4]

# ponemos los dos ensayos uno después del otro
ax = np.hstack((ax1,ax2))
ay = np.hstack((ay1,ay2))
iR = np.hstack((iR1,iR2))
iS = np.hstack((iS1,iS2))


# filtro pasabanda de vibraciones a frecuencia 25 Hz
from scipy.signal import firwin, lfilter
b = firwin(501,[25-5,25+5],fs=5000, pass_zero='bandpass')
ax = lfilter(b,1,ax)
ay = lfilter(b,1,ay)



print('visualizando ...')


# FIGURA
# creamos la figura
fig1 = figure(width=400,height=400,x_axis_label='ax(t)',y_axis_label='ay(t)')

# añadimos elementos a la figura
p1 = fig1.line(ax,ay,line_width=1,line_alpha=0.5,legend_label='órbita de aceleraciones')


# creamos la figura
fig2 = figure(width=400,height=400,x_axis_label='iR(t)',y_axis_label='iS(t)')
p2 = fig2.line(iR,iS,alpha=0.5,legend_label='órbita de corrientes')


# ELEMENTO DE TEXTO
div = Div(text='''
	<h1>Plot básico: análisis de órbitas</h1>
	<h4>Ignacio Díaz Blanco, 2020. Universidad de Oviedo</h4>
	<p>Visualización x-y de trayectoria de aceleraciones y corrientes en un motor de inducción. Incluye:
	</p>
	<ul>
		<li>Órbita de aceleraciones: (ax, ay)</li>
		<li>Órbita de corrientes (iR,iS)</li>
		<li>Filtrado FIR pasabanda para las órbitas de aceleraciones. Permite visualizar la órbita de un armónico de vibración dado.</li>
	</ul>

	<a href="fuentes/%s">(código fuente)</a>'''%(__file__.split('.')[0]+'_codigofuente.html'),width=600)

# ORGANIZACIÓN DE LOS COMPONENTES: FIGURA, TEXTO
lay = layout([div,[fig1,fig2]])


show(lay)