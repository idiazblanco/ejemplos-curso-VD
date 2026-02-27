'''
EJEMPLO BÁSICO DE SCATTERPLOT EN BOKEH

Ignacio Díaz Blanco, 2020. Universidad de Oviedo

'''
import pandas as pd
from bokeh.models import ColumnDataSource, LabelSet, HoverTool, CategoricalColorMapper, Div, LinearColorMapper
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


# leemos datos de demanda eléctrica
df = pd.read_csv('demanda_electrica.csv',parse_dates=True,index_col='Fecha')
df['Fecha (str)'] = df.index.strftime('%Y/%m/%d %H:%M')

# variable índice [0, ..., n-1]
k = np.arange(len(df))

# añadimos encodings de posición al dataframe 
# espiral gira 1 vuelta por día y avanza hacia fuera
df['x'] = np.cos(2*np.pi/(1440)*k)*10*(1 + k/40000)
df['y'] = np.sin(2*np.pi/(1440)*k)*10*(1 + k/40000)

# creamos un source con el dataframe
source = ColumnDataSource(df)


# creamos una paleta de color con matplotlib
from matplotlib.cm import plasma
from matplotlib.colors import rgb2hex
mi_paleta = [rgb2hex(plasma(i)) for i in np.linspace(0,1,200)]

color_map = LinearColorMapper(palette=mi_paleta,
                  low = min(df['Activa (kW)']),
                  high= max(df['Activa (kW)']))


# figura + scatter
p = figure(width=1000,height=900)
p.scatter(x='x', y='y',
          color={'field': 'Activa (kW)', 'transform': color_map},
          source=source, radius=.05)

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


# ELEMENTO DE TEXTO
div = Div(text='''
	<h1>Visualización de consumos eléctricos en espiral</h1>
  <h4>Ignacio Díaz Blanco, 2021. Universidad de Oviedo</h4>
  <p>En este scatterplot se incorpora una <i>codificación espacial</i> específica de los datos. Las codificaciones espaciales permiten de forma implícita incorporar periodicidades, patrones o regularidades conocidas que facilitan el análisis. En este caso se codifica la hora del día mediante el giro (24 horas = 1 vuelta) y el día mediante el radio (hacia fuera)</p>

  <h4>Posibles variaciones</h4>
  <ul>
    <li>Utilizar una periodicidad semanal en lugar de diaria</li>
    <li>Codificación matricial (hora del día vs. día de la semana)</li>
    <li><i>Small multiples 1</i>: cada día un círculo de 1440 min</li>
    <li><i>Small multiples 2</i>: cada semana una matriz de 7 días x 1440 min</li>
  </ul>

<a href="fuentes/%s">(código fuente)</a>'''%(__file__.split('.')[0]+'_codigofuente.html'),width=700)



show(layout([div,p]))