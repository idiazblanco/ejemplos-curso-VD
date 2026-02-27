'''
EJEMPLO BÁSICO DE FUENTES DE DATOS EN BOKEH

Ignacio Díaz Blanco, 2020. Universidad de Oviedo

'''
import pandas as pd
import numpy as np
from bokeh.plotting import figure, output_file

from bokeh.io import show
from bokeh.models import Div, ColumnDataSource, RangeTool, CustomJS, Circle
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

# vector de tiempos
N  = datos.shape[0]
t  = np.arange(0,N)*tm

# variables a visualizar
ax  = datos[:,1]
ay  = datos[:,2]
iR  = datos[:,3]
iS  = datos[:,4]
calculada = np.sin(datos[:,3]*datos[:,4])


# SOURCE: FUENTE COMÚN DE DATOS

# el source puede generarse con un dataframe (muy cómodo)
datos = pd.DataFrame(np.array([t,ax,ay,iR,iS,calculada]).T,columns=['t','ax','ay','iR','iS','calculada'])

# generamos el objeto "source" a partir del dataframe
source = ColumnDataSource(datos)

# este objeto es una "fuente de datos" común
# que "sincroniza" todas las figuras
# cualquier cambio en los datos (modificación, selección)
# es inmediatamente actualizado por Boheh en 
# todas las figuras que tengan esa fuente


# FIGURA
# creamos la figura
f1 = figure(width=300,height=300,tools="crosshair,box_select,pan,reset,wheel_zoom")
p1 = f1.circle(x='ax', y='ay', source=source,radius=.02,line_width=0,line_alpha=0.5,legend_label='ax(t) vs. ay(t)')

f2 = figure(width=300,height=300,tools="crosshair,box_select,pan,reset,wheel_zoom")
p2 = f2.circle(x='iR', y='iS', source=source,radius=.02,line_width=0,line_alpha=0.5,legend_label='ir(t) vs. is(t)')

f3 = figure(width=600,height=300,tools="xbox_zoom,crosshair,xbox_select,xpan,reset,xwheel_zoom")
p3 = f3.circle(x='t', y='calculada', source=source,size=1,legend_label='variable calculada')
p4 = f3.line(x='t', y='calculada', source=source,line_width=1,line_color='red',line_alpha=0.5)



# # HERRAMIENTA RANGETOOL X (permite hacer drag en selección)
# range_tool = RangeTool(x_range=Range1d(4,4))
# range_tool.overlay.fill_color = "navy"
# range_tool.overlay.fill_alpha = 0.1
# callback = CustomJS(args=dict(source=source),code=
# 	"""
# 	source.selected.indices = []
# 	for (var i=0; i<source.data.index.length; i++)
# 		{
# 		if (source.data['t'][i]>cb_obj.start & source.data['t'][i]<cb_obj.end)
# 			source.selected.indices.push(i)
# 		}
# 	""")
# range_tool.x_range.js_on_change('start',callback)
# range_tool.x_range.js_on_change('end',callback)
# f3.add_tools(range_tool)



# # HERRAMIENTA RANGETOOL Y (permite hacer drag en selección)
# range_tool = RangeTool(y_range=Range1d(0,0))
# range_tool.overlay.fill_color = "navy"
# range_tool.overlay.fill_alpha = 0.1
# callback = CustomJS(args=dict(source=source),code=
# 	"""
# 	source.selected.indices = []
# 	for (var i=0; i<source.data.index.length; i++)
# 		{
# 		if (source.data['calculada'][i]>cb_obj.start & source.data['calculada'][i]<cb_obj.end)
# 			source.selected.indices.push(i)
# 		}
# 	""")
# range_tool.y_range.js_on_change('start',callback)
# range_tool.y_range.js_on_change('end',callback)
# f3.add_tools(range_tool)



selected_circle = Circle(fill_alpha=1, fill_color="firebrick", line_color=None)
nonselected_circle = Circle(fill_alpha=0.2, fill_color="blue", line_color=None)
p1.selection_glyph = selected_circle
p1.nonselection_glyph = nonselected_circle

p2.selection_glyph = selected_circle
p2.nonselection_glyph = nonselected_circle

p3.selection_glyph = selected_circle
p3.nonselection_glyph = nonselected_circle

# p4.selection_glyph = selected_circle
# p4.nonselection_glyph = nonselected_circle



# ELEMENTO DE TEXTO
div = Div(text='''
<h1>Uso de un dataframe como fuente de datos</h1>
<h4>Ignacio Díaz Blanco, 2021. Universidad de Oviedo</h4>
<table>
<td valign="top">
<p>En este ejemplo usamos un <i>dataframe</i> como fuente de datos</p>

%s

<p>El objeto <i>source</i> es una "fuente de datos" común
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
<a href="fuentes/%s">(código fuente)</a>'''%(datos.head().to_html(border=0),__file__.split('.')[0]+'_codigofuente.html'),width=700)

# ORGANIZACIÓN DE LOS COMPONENTES: FIGURA, TEXTO
lay = layout([
	[div],
	[f1,f2,f3]
	])


show(lay)