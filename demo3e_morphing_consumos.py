'''
EJEMPLO BÁSICO DE MORPHING

Ignacio Díaz Blanco, 2020. Universidad de Oviedo

'''
import pandas as pd
from bokeh.models import ColumnDataSource, LabelSet, HoverTool, CategoricalColorMapper, Div, LinearColorMapper, DatetimeTickFormatter, Slider, CustomJS
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
df['Fecha']=df.index

# indices con timestamps
df.index = df['Fecha'].values

# generamos columnas hora, día de la semana
df['hora'] = df.index.hour
df['diasemana'] = df.index.weekday


# creamos columna para el tamaño
df['tam'] = (df['Activa (kW)']-min(df['Activa (kW)']))/(max(df['Activa (kW)']-min(df['Activa (kW)'])))*0.05

# remuestreamos a 15 min
df = df.resample('15min',on='Fecha').mean()
minutos = (df.index - df.index[0]).total_seconds()/60;
df['Fecha (str)'] = df.index.strftime('%Y/%m/%d %H:%M')

df.reset_index(inplace=True)



# generamos variable índice
k = np.arange(len(df))

# creamos encodings

E0 = np.array([
                np.cos(2*np.pi/(1440)*minutos)*(20+minutos/1440),
                np.sin(2*np.pi/(1440)*minutos)*(20+minutos/1440)])
E1 = np.array([
                (minutos %  1440)/60.0,
                minutos // 1440])
E2 = np.array([
                np.cos(df['hora']*2*np.pi/24),
                np.sin(df['hora']*2*np.pi/24)])


Encodings = [E0, E1, E2]



# normalizamos los encodings al rango (-1,1)
for i,E in enumerate(Encodings):
    Encodings[i][0,:] = 2*(E[0,:]-E[0,:].min())/(E[0,:].max()-E[0,:].min())-1
    Encodings[i][1,:] = 2*(E[1,:]-E[1,:].min())/(E[1,:].max()-E[1,:].min())-1



# columna con el encoding mezcla (inicializamos con de un encoding)
df['x'] = Encodings[0][0,:]
df['y'] = Encodings[0][1,:]




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
p = figure(width=800,height=700,tools="box_zoom,wheel_zoom,pan,box_select,lasso_select,reset",output_backend='webgl'
          ,title='Visualización espiral'
          ,x_range=(-2,2),y_range=(-2,2))
p.circle(x='x', y='y',
          color={'field': 'Activa (kW)', 'transform': color_map},
          source=source, radius='tam',alpha=0.5)

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



slider = Slider(start=0, end=1, value=0.7, step=.01, title='lambda',width=500)

callback_slider=CustomJS(args=dict(source=source, E=Encodings),
                    code="""
                    var L = cb_obj.value                    
                    var x1 = E[0][0]
                    var y1 = E[0][1]
                    var x2 = E[1][0]
                    var y2 = E[1][1]
                    source.data['x'] = x1.map((d,i)=>L*x1[i] + (1-L)*x2[i])
                    source.data['y'] = y1.map((d,i)=>L*y1[i] + (1-L)*y2[i])
                    source.change.emit()
                    """)
slider.js_on_change('value',callback_slider)


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
	<h1>Ejemplo basico de Morphing Projections</h1>
  <h4>Ignacio Díaz Blanco, 2021. Universidad de Oviedo</h4>
  <p>Morphing projections es una técnica de interacción desarrollada por el grupo GSDPI de UniOvi, que permite visualizar datos multivía mediante transiciones animadas entre vistas base. Puedes ver información relacionada en la <a href="http://isa.uniovi.es/GSDPI/morphingProjections.html">página de Morphing Projections</a> de GSDPI y en el <a href="https://youtu.be/Y9X35CdcC6U"> vídeo de YouTube</a></p>
  <ul>
  <li>Ignacio Díaz, José M Enguita, Ana González, Diego García, Abel A Cuadrado, María D Chiara, and Nuria Valdés, "Morphing Projections: a new visual technique for fast and interactive large-scale analysis of biomedical datasets". <em>Bioinformatics</em>. 11, 2020 <a href=" https://doi.org/10.1093/bioinformatics/btaa989">[→ web]</a><a href="http://isa.uniovi.es/GSDPI/demoMP.html">[demo version to reproduce paper results]</a><a href="https://gitlab.com/idiazblanco/morphing-projections-demo-and-dataset-preparation">[source code (gitlab)]</a></li>    
  <li>Ignacio Díaz, Manuel Domínguez, Abel A. Cuadrado, Alberto B. Diez, and Juan J. Fuertes &quot;MorphingProjections: Interactive Visualization of Electric Power Demand Time Series&quot;. In Eurographics Conference on Visualization (EuroVis) (2012), Viena (Austria). pp. 121-125. Jun, 2012</li>  
  </ul>


<a href="fuentes/%s">(código fuente)</a>'''%(__file__.split('.')[0]+'_codigofuente.html'),width=700)





show(layout([div,[p,timeplot],slider]))