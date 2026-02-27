'''
EJEMPLO BÁSICO DE SCATTERPLOT EN BOKEH

Ignacio Díaz Blanco, 2020. Universidad de Oviedo

'''
import numpy as np
import pandas as pd
from bokeh.models import ColumnDataSource, LabelSet, HoverTool, CategoricalColorMapper, Div, LinearColorMapper
from bokeh.palettes import d3
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.layouts import layout

# archivo de salida (mismo nombre, extensión html)
filename = __file__.split('.')[0]+'.html'
output_file(filename)

# cargamos los datos de iris (obtenidos de wikipedia y adaptados a formato csv)
df = pd.read_csv('iris_con_categorias.csv')

source = ColumnDataSource(df)


# LinearColorMapper = mapeador de color: interpolación lineal a tramos dada escala


# # usando escala de color propia de Bokeh
# color_map = LinearColorMapper(palette='Viridis256',
#                   low = min(df['Largo de sépalo']),
#                   high= max(df['Largo de sépalo']))

# escala de color generada con matplotlib
from matplotlib.cm import plasma
from matplotlib.colors import rgb2hex
paleta = [rgb2hex(plasma(x)) for x in np.linspace(0,1,7)]
color_map = LinearColorMapper(palette=paleta,
                  low = min(df['Largo de sépalo']),
                  high= max(df['Largo de sépalo']))

# # usando escala de color hecha "a mano"
# color_map = LinearColorMapper(palette=['#ff0000','#00ff00','#0000ff'],
#                   low = min(df['Largo de sépalo']),
#                   high= max(df['Largo de sépalo']))



# figure + plot
p = figure()
p.scatter(x='Largo de sépalo', y='Largo de pétalo',
          color={'field': 'Largo de sépalo', 'transform': color_map},
          source=source, radius=.02)

# añadir colorbar a la figura
from bokeh.models import ColorBar
bar = ColorBar(color_mapper=color_map, location=(0,0))
p.add_layout(bar, "left")


hover = HoverTool()
hover.tooltips = [
    ('Largo pétalo',"@{Largo de pétalo}"),
    ('Ancho pétalo',"@{Ancho de pétalo}"),
    ('Largo sépalo',"@{Largo de sépalo}"),
    ('Ancho sépalo',"@{Ancho de sépalo}"),
    ('Especie',"@especie")]
p.tools.append(hover)


# ELEMENTO DE TEXTO
div = Div(text='''
	<h1>Ejemplo básico de scatterplot</h1>
  <h4>Ignacio Díaz Blanco, 2021. Universidad de Oviedo</h4>
	<p><b>Ejemplo básico de scatterplot en Bokeh</b>. <br> En este ejemplo se muestra cómo hacer un scatterplot en Bokeh, incluyendo el coloreado de variables continuas con <i>LinearColormapper</i> y la visualización de información de contexto mediante "tooltips" activados con eventos <i>hover</i>.</p>
  <b>Posibles ampliaciones o variaciones</b>
  <ul>
    <li>Cambiar el número de "saltos" de color (ej. hacerlo continuo)</li>
    <li>Usar otra escala de color de matploblib (ver <a href="https://matplotlib.org/stable/tutorials/colors/colormaps.html">colormaps de matplotlib</a>)</li>
    <li>Utilizar el tamaño para codificar otra variable</li>
  </ul>
<a href="fuentes/%s">(código fuente)</a>'''%(__file__.split('.')[0]+'_codigofuente.html'),width=700)





show(layout([div,p]))