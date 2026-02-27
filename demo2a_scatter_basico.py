'''
EJEMPLO BÁSICO DE SCATTERPLOT EN BOKEH

Ignacio Díaz Blanco, 2020. Universidad de Oviedo

'''
import pandas as pd
from bokeh.models import ColumnDataSource, LabelSet, HoverTool, CategoricalColorMapper, Div
from bokeh.palettes import d3
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.layouts import layout

# archivo de salida (mismo nombre, extensión html)
filename = __file__.split('.')[0]+'.html'
output_file(filename)

# cargamos los datos de iris (obtenidos de wikipedia y adaptados a formato csv)
df = pd.read_csv('iris_con_categorias.csv')



source = ColumnDataSource(df)

# usar la paleta que se quiera, en formato ['#ff0000', '#ffaa13', ...]
# hay muchas formas de generarla (ej: usando matploblib.cm.PuBu + matplotlib.color.rgb2hex)
paleta = d3['Category10'][len(df['especie'].unique())]

# mapeador de color: categoría --> color de la paleta
color_map = CategoricalColorMapper(factors=df['especie'].unique(),
                                   palette=paleta)

# crear figura y plot
# en el campo color se usa color_map para mapear "categoría --> color" en cada muestra
p = figure()
p.circle(
    x='Largo de sépalo',
    y='Largo de pétalo',
    color={'field': 'especie', 'transform': color_map},
    legend_group='especie',
    source=source,
    radius=0.02
)

# tooltips
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
  <h4>Ignacio Díaz Blanco, 2020. Universidad de Oviedo</h4>
	<p><b>Ejemplo básico de scatterplot en Bokeh</b>. <br> En este ejemplo se muestra cómo hacer un scatterplot en Bokeh, incluyendo el coloreado de variables categóricas con <i>CategoricalColormapper</i> y la visualización de información de contexto mediante "tooltips" activados con eventos <i>hover</i>.</p>
<a href="fuentes/%s">(código fuente)</a>'''%(__file__.split('.')[0]+'_codigofuente.html'),width=700)

print(__file__)

show(layout([div,p]))