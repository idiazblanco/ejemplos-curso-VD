'''
EJEMPLO BÁSICO DE SCATTERPLOT EN BOKEH

Ignacio Díaz Blanco, 2020. Universidad de Oviedo

'''
import pandas as pd
from bokeh.models import ColumnDataSource, LabelSet, HoverTool, CategoricalColorMapper, Div, LinearColorMapper, DatetimeTickFormatter
from bokeh.palettes import d3
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.layouts import layout


# numpy + matplotlib + pandas
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd




# archivo de salida (mismo nombre, extensión html)
filename = __file__.split('.')[0]+'.html'
output_file(filename)

# leemos datos de consumos con Pandas
df = pd.read_csv('demanda_electrica.csv',parse_dates=True,index_col='Fecha')

# creamos columna con fechas en timestamps
df['Fecha (str)'] = df.index.strftime('%Y/%m/%d %H:%M')


# generamos variable índice
k = np.arange(len(df))

# creamos columnas x,y con codificación espacial específica
#   añadimos encodings de posición al dataframe 
#   espiral gira 1 vuelta por día y avanza hacia fuera
df['x'] = (k %  1440)/60.0    # el eje x se expresa en horas [0..23]
df['y'] = k // 1440           # el eje y se expresa en días


# creamos columna para el tamaño
df['tam'] = (df['Activa (kW)']-min(df['Activa (kW)']))/(max(df['Activa (kW)']-min(df['Activa (kW)'])))*0.3


# fuente de datos a partir del dataframe
source = ColumnDataSource(df)



# creamos una paleta de matplotlib
from matplotlib.cm import plasma
from matplotlib.colors import rgb2hex
mi_paleta = [rgb2hex(plasma(i)) for i in np.linspace(0,1,200)]

color_map = LinearColorMapper(palette=mi_paleta,
                  low = min(df['Activa (kW)']),
                  high= max(df['Activa (kW)']))


# CREAMOS DOS FIGURAS CON LA MISMA FUENTE (permite selecciones enlazadas)

# primera figura
p = figure(width=800,height=700,tools="box_zoom,wheel_zoom,pan,box_select,lasso_select,reset",output_backend='webgl',title='Visualización espiral')
p.scatter(x='x', y='y',
          color={'field': 'Activa (kW)', 'transform': color_map},
          source=source, radius='tam',alpha=0.2)

# añadir colorbar a la figura
from bokeh.models import ColorBar
bar = ColorBar(color_mapper=color_map, location=(0,0))
p.add_layout(bar, "left")


# configuración de los tooltips
hover = HoverTool()
hover.tooltips = [
    ('Fecha',"@{Fecha (str)}"),
    ('kW totales',"@{Activa (kW)}"),
    ('kVAR totales',"@{Reactiva (kVAR)}")
    ]
p.tools.append(hover)


# segunda figura
timeplot = figure(width=800,height=300,tools="box_zoom,xwheel_zoom,xpan,box_select,lasso_select,reset",output_backend='webgl',title='Gráfica timeplot',x_axis_type='datetime')
timeplot.scatter(x='Fecha',y='Activa (kW)',color='red',source=source)
timeplot.line(x='Fecha',y='Activa (kW)',color='blue',source=source)

# FORMATEO "A MEDIDA" DE FECHAS
# timeplot.xaxis.formatter=DatetimeTickFormatter(
#         hours=["%d %B %Y"],
#         days=["%d %B %Y"],
#         months=["%d %B %Y"],
#         years=["%d %B %Y"],
#     )



# ELEMENTO DE TEXTO
div = Div(text='''
	<h1>Visualización de consumos eléctricos en espiral</h1>
  <h4>Ignacio Díaz Blanco, 2020. Universidad de Oviedo</h4>
	<p><b>Versión con interacción: selecciones enlazadas</b>. </p>
<a href="fuentes/%s">(código fuente)</a>'''%(__file__.split('.')[0]+'_codigofuente.html'),width=700)





show(layout([div,[p,timeplot]]))