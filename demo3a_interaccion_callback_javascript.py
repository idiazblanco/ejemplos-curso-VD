'''
EJEMPLO DE INTERACTIVIDAD EN BOKEH (CALLBACKS JAVASCRIPT)

Ignacio Díaz Blanco, 2020. Universidad de Oviedo
'''

import pandas as pd
import numpy as np
from bokeh.plotting import figure, output_file

from bokeh.io import show
from bokeh.models import Div, ColumnDataSource, Slider, CustomJS
from bokeh.layouts import layout

# archivo de salida (mismo nombre, extensión html)
filename = __file__.split('.')[0]+'.html'
output_file(filename)



# DATOS INICIALES
N = 1000
t = np.linspace(0,100,N)
x = np.sin(t)
y = np.sin(2*t)
z = np.sin(3*t)


# SOURCE: FUENTE COMÚN DE DATOS
# el source puede verse como una tabla 
# en este caso, tiene N muestras y atributos 'x', 'y', 'z'
datos = {
	't': t,
	'x': x,
	'y': y,
	'z':z
}

# generamos el objeto "source"
source = ColumnDataSource(datos)

# este objeto es una "fuente de datos" común
# que "sincroniza" todas las figuras
# cualquier cambio en los datos (modificación, selección)
# es inmediatamente actualizado por Boheh en 
# todas las figuras que tengan esa fuente





# ELEMENTOS INTERACTIVOS
# SLIDERS y su función callback
slider1 = Slider(start=-5, end=5, value=0, step=.01, title="a")
slider2 = Slider(start=-5, end=5, value=1, step=.01, title="b")
slider3 = Slider(start=-5, end=5, value=0, step=.01, title="c")


callback = CustomJS(args=dict(source=source, s1=slider1, s2=slider2, s3=slider3),
                    code="""
    const data = source.data;
    const a = s1.value;
    const b = s2.value;
    const c = s3.value;
    const t = data['t']
    const x = data['x']
    const y = data['y']
    const z = data['z']
    for (var i = 0; i < t.length; i++) {
        x[i] = Math.sin(1*t[i] + a);
        y[i] = b*Math.sin(2*t[i]);
        z[i] = Math.sin(3*t[i] + c);
    }
    console.log([a,b,c])
    source.change.emit();
""")

slider1.js_on_change('value',callback)
slider2.js_on_change('value',callback)
slider3.js_on_change('value',callback)






# FIGURA
# creamos la figura
f1 = figure(width=400,height=400,tools="crosshair,box_select,pan,reset,wheel_zoom",y_range=(-2,2),x_range=(-2,2))
p1 = f1.line(x='x', y='y', source=source,line_width=2,line_alpha=0.5,legend_label='y(t)')

f2 = figure(width=400,height=400,tools="crosshair,box_select,pan,reset,wheel_zoom",y_range=(-2,2),x_range=(-2,2))
p2 = f2.line(x='y', y='z', source=source,line_width=2,line_alpha=0.5,legend_label='z(t)')




# ELEMENTO DE TEXTO

div = Div(text='''
<h1>Interactividad con sliders en Bokeh</h1>
<h2>callbacks en javascript</h2>
<i>Ignacio Díaz Blanco, 2020. Universidad de Oviedo</i>
<table cellpadding=5>
<td valign="top">
<p>En este ejemplo se utilizan widgets de tipo <i>slider</i>. Cuando cualquiera de los sliders cambia, se ejecuta una <i>callback</i> en javascript. Las callbacks en javascript pueden ser integradas en un html autónomo (<i>standalone</i>), que no requiere de servidor python para su ejecución</p> 
</td>
<td valign="top">
<p>La callback modifica los datos de <code>source</code>, resultando en una actualización "inmediata" y en tiempo real de las gráficas</p></td>
</table>
<a href="fuentes/%s">(código fuente)</a>'''%(__file__.split('.')[0]+'_codigofuente.html'),width=700)


divhueca = Div(height=100)




# ORGANIZACIÓN DE LOS COMPONENTES: FIGURA, TEXTO
lay = layout([
	[div,[divhueca,slider1,slider2,slider3]],
	[f1,f2],
	
	])


show(lay)