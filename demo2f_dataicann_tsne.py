'''
SELECCIONES ENLAZADAS ENTRE VISTAS PCA/tSNE Y PLOT EN BOKEH

Ignacio Díaz Blanco, 2020. Universidad de Oviedo

En este ejemplo, se realizan proyecciones PCA y tSNE de los datos "dataicann" (vibraciones y corrientes de un motor de inducción). El ejemplo demuestra el uso de selecciones enlazadas en las que el usuario selecciona muestras en una vista y la selección dinámicamente se muestra en otra vista diferente de los mismos datos.

'''

import pandas as pd
import numpy as np
from bokeh.plotting import figure, output_file

from bokeh.io import show, curdoc
from bokeh.models import Div, ColumnDataSource, Slider, CustomJS, Circle, LinearColorMapper
from bokeh.layouts import layout, widgetbox



# DATOS INICIALES
# cargamos datos de dataicann con extracción de características hecha
df = pd.read_hdf('dataicann_features.hdf')
J  = df.to_dict(orient='list')

# nos quedamos con 4 atributos ('ax@25Hz', 'ay@25Hz', 'ay@100Hz', 'ir@50Hz')
X  = df.iloc[:,[0,2,3,4]]



# NORMALIZACIÓN DE LOS DATOS (-1,+1)
print('normalizando datos ...')
from sklearn.preprocessing import MinMaxScaler
minmax = MinMaxScaler(feature_range=(-1,1))
Xn = minmax.fit_transform(X)



# REDUCCIÓN DE LA DIMENSIÓN (PCA o tSNE)
proyeccion = 'tsne'

if proyeccion == 'pca':
	print('calculando proyecciones PCA ...')
	import numpy as np
	from sklearn.decomposition import PCA
	pca = PCA(n_components=2)
	pr = pca.fit_transform(X)

elif proyeccion == 'tsne':
	print('calculando proyecciones tSNE ...')
	from sklearn.manifold import TSNE
	tsne = TSNE(n_components=2,perplexity=200,init = 'pca')
	pr = tsne.fit_transform(Xn)







# SOURCE: FUENTE COMÚN DE DATOS
# el source puede verse como una tabla 
# en este caso, tiene N muestras con 7 atributos (5 características + 2 coord. proyeccion)
source = ColumnDataSource(J)
source.data['pr_x'] = pr[:,0]
source.data['pr_y'] = pr[:,1]
source.data['tam'] = df['ay@25Hz']*200

# este objeto es una "fuente de datos" común
# que "sincroniza" todas las figuras
# cualquier cambio en los datos (modificación, selección)
# es inmediatamente actualizado por Boheh en 
# todas las figuras que tengan esa fuente







# FIGURA
# creamos la figura
f1 = figure(width=600,height=150,tools="crosshair,box_select,xpan,reset,xwheel_zoom",title='ax@25Hz')
p1 = f1.circle(x='t', y='ax@25Hz', source=source)
p1.selection_glyph = Circle(fill_alpha=1, fill_color="firebrick", line_color=None)

f2 = figure(width=600,height=150,tools="crosshair,box_select,xpan,reset,xwheel_zoom",title='ay@25Hz',x_range = f1.x_range)
p2 = f2.circle(x='t', y='ay@25Hz', source=source)
p2.selection_glyph = Circle(fill_alpha=1, fill_color="firebrick", line_color=None)

f3 = figure(width=600,height=150,tools="crosshair,box_select,xpan,reset,xwheel_zoom",title='ay@100Hz',x_range = f1.x_range)
p3 = f3.circle(x='t', y='ay@100Hz', source=source)
p3.selection_glyph = Circle(fill_alpha=1, fill_color="firebrick", line_color=None)

f4 = figure(width=600,height=150,tools="crosshair,box_select,xpan,reset,xwheel_zoom",title='iR@50Hz',x_range = f1.x_range)
p4 = f4.circle(x='t', y='ir@50Hz', source=source)
p4.selection_glyph = Circle(fill_alpha=1, fill_color="firebrick", line_color=None)




# Mapa de estados del motor tSNE

# escala de color generada con matplotlib
from matplotlib.cm import plasma
from matplotlib.colors import rgb2hex
paleta = [rgb2hex(plasma(x)) for x in np.linspace(0,1,100)]
color_map = LinearColorMapper(palette=paleta,
                  low = min(df['ay@100Hz']),
                  high= max(df['ay@100Hz']))
f5 = figure(width=600,height=600,tools="crosshair,box_select,lasso_select,pan,reset,wheel_zoom",match_aspect=True,title='Mapa de estados del motor (t-SNE)')
p5 = f5.circle(x='pr_x', y='pr_y', source=source,size='tam',color={'field': 'ay@100Hz', 'transform': color_map})
p5.selection_glyph = Circle(fill_alpha=1, fill_color="firebrick", line_color=None)

# añadir colorbar a la figura
from bokeh.models import ColorBar
bar = ColorBar(color_mapper=color_map, location=(0,0))
f5.add_layout(bar, "left")



# ELEMENTO DE TEXTO
div = Div(text='''
<h1>Selecciones enlazadas entre vistas PCA/tSNE y plot en Bokeh</h1>
<h4>Ignacio Díaz Blanco, 2021. Universidad de Oviedo</h4>
<p>En este ejemplo, se realizan proyecciones PCA y tSNE de los datos <i>dataicann</i> (vibraciones y corrientes de un motor de inducción). El ejemplo demuestra el uso de <b>selecciones enlazadas</b> en las que el usuario selecciona muestras en una vista y la selección dinámicamente se muestra en otra vista diferente de los mismos datos.</p>
<a href="fuentes/%s">(código fuente)</a>'''%(__file__.split('.')[0]+'_codigofuente.html'),width=700)

divhueca = Div(height=150)




# ORGANIZACIÓN DE LOS COMPONENTES: FIGURA, TEXTO
lay = layout([
	[div],
	[[f1,f2,f3,f4],[f5]]
	])

# archivo de salida (mismo nombre, extensión html)
filename = __file__.split('.')[0]+'.html'
output_file(filename)


show(lay)