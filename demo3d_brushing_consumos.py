'''
EJEMPLO: Visualización de consumos eléctricos en espiral con brushing

Ignacio Díaz Blanco, 2021. Universidad de Oviedo

'''
import pandas as pd
from bokeh.models import ColumnDataSource, LabelSet, HoverTool, CategoricalColorMapper, Div, LinearColorMapper, CustomJS
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

# fecha en formato string
df['Fecha (str)'] = df.index.strftime('%Y/%m/%d %H:%M')

# creamos columna para el tamaño
df['tam'] = (df['Activa (kW)']-min(df['Activa (kW)']))/(max(df['Activa (kW)']-min(df['Activa (kW)'])))*0.3


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




# CONTENEDOR DE LOS DESCRIPTORES AGREGADOS
divHover = Div(text='')



# FIGURA
p = figure(width=1000,height=900,output_backend='webgl')

# SCATTER PLOT DE LOS DATOS
p.scatter(x='x', y='y',
          color={'field': 'Activa (kW)', 'transform': color_map},
          source=source, radius='tam')

# MARCADO DE LOS PUNTOS SELECCIONADOS
source_sel = ColumnDataSource({'x':[],'y':[]})
p.scatter(x='x', y='y',
          color='green', source=source_sel, radius=.2,alpha=0.1)


# MARCADO DEL PUNTO MÁS CERCANO (bmu)
source_bmu = ColumnDataSource({'x':[],'y':[]})
p.scatter(x='x', y='y',
          color='red', source=source_bmu, radius=.3,alpha=0.5)


# CAPTURA DEL EVENTO MouseMove
from bokeh.events import MouseMove

callback_brush = CustomJS(args=dict(source_main = source, source_sel=source_sel, source_bmu=source_bmu, divHover=divHover), 
  code = """
// OBTENER PUNTOS EN UN ENTORNO DEL RATÓN d(mousex,mousey) < dmax
let x = cb_obj.x
let xs= source_main.data['x'];
let y = cb_obj.y
let ys= source_main.data['y'];


// DISTANCIAS d(mousex,mousey)
let dist = xs.map((d,i)=>Math.pow(xs[i]-x,2)+Math.pow(ys[i]-y,2))


// INDICES SELECCIONADOS d(mousex,mousey) < dmax
let idx = dist.map((d,i)=>d<3?i:-1).filter(d=>d>0)


// ÍNDICE DEL PUNTO MÁS CERCANO AL RATÓN
let bmu = dist.indexOf(Math.min(...dist));


// CALCULOS SOBRE LA SELECCIÓN
let demanda = idx.map(i=>source_main.data['Activa (kW)'][i])
let resultados = {}
resultados['Fecha (bmu)'] = source_main.data['Fecha (str)'][bmu]
resultados['potencia activa total (suma)'] = demanda.reduce((a, b) => a + b, 0).toFixed(2)
resultados['potencia activa promedio'] = (demanda.reduce((a, b) => a + b, 0)/demanda.length).toFixed(2)
resultados['potencia activa máxima'] = Math.max(...demanda).toFixed(2)
resultados['potencia activa mínima'] = Math.min(...demanda).toFixed(2)
resultados['potencia activa (bmu)'] = source_main.data['Activa (kW)'][bmu].toFixed(2)
resultados['potencia reactiva (bmu)'] = source_main.data['Activa (kW)'][bmu].toFixed(2)

// TABLA HTML DINÁMICA CON LOS RESULTADOS
let str = `<h2>descriptores de la selección</h2>`
str += `<table>`
for (var i in resultados)
{
    str = str + `<tr><td align='right'>${i}:</td> <td>${resultados[i]}</td></tr>`
}
str = str + `</table>`
divHover.text = str


// TRANSFERIR COORDENADAS DE LOS DATOS SELECCIONADOS AL source_sel
source_sel.data['x'] = idx.map(d=>source_main.data['x'][d])
source_sel.data['y'] = idx.map(d=>source_main.data['y'][d])


// AÑADIMOS EL PUNTO MÁS CERCANO (bmu)
source_bmu.data['x'] = [source_main.data['x'][bmu]]
source_bmu.data['y'] = [source_main.data['y'][bmu]]


// ACTUALIZAR FUENTES
source_sel.change.emit()
source_bmu.change.emit()
""")

p.js_on_event(MouseMove,callback_brush)


# añadir colorbar a la figura
from bokeh.models import ColorBar
bar = ColorBar(color_mapper=color_map, location=(0,0))
p.add_layout(bar, "left")



# ELEMENTO DE TEXTO
div = Div(text='''
	<h1>Visualización de consumos eléctricos en espiral con brushing</h1>
  <h4>Ignacio Díaz Blanco, 2021. Universidad de Oviedo</h4>
<a href="fuentes/%s">(código fuente)</a>'''%(__file__.split('.')[0]+'_codigofuente.html'),width=700)



show(layout([div,[p,divHover]]))