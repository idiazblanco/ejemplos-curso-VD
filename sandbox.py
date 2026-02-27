'''
EJEMPLO BÁSICO DE FUENTES DE DATOS EN BOKEH
Compatible con Bokeh 3.x

Ignacio Díaz Blanco, 2020–2026. Universidad de Oviedo
'''

import pandas as pd
import numpy as np
from scipy.io import loadmat

from bokeh.plotting import figure, output_file
from bokeh.io import show
from bokeh.models import Div, ColumnDataSource
from bokeh.layouts import layout


# ------------------------------------------------------------
# ARCHIVO DE SALIDA
# ------------------------------------------------------------

filename = __file__.split('.')[0] + '.html'
output_file(filename)


# ------------------------------------------------------------
# CARGA DE DATOS
# ------------------------------------------------------------

print('cargando datos ...')
d = loadmat('dataicann.mat')

# obtener ensayo 2
datos_raw = d['z'][0][7]

fm = 5000.0
tm = 1 / fm

N = datos_raw.shape[0]
t = np.arange(0, N) * tm

ax = datos_raw[:, 1]
ay = datos_raw[:, 2]
iR = datos_raw[:, 3]
iS = datos_raw[:, 4]

calculada = np.sin(iR * iS)


# ------------------------------------------------------------
# DATAFRAME + COLUMNDATASOURCE
# ------------------------------------------------------------

df = pd.DataFrame({
    "t": t,
    "ax": ax,
    "ay": ay,
    "iR": iR,
    "iS": iS,
    "calculada": calculada
})

source = ColumnDataSource(df)


# ------------------------------------------------------------
# FIGURAS
# ------------------------------------------------------------

# --- Scatter ax vs ay ---
f1 = figure(
    width=300,
    height=300,
    tools="crosshair,box_select,pan,reset,wheel_zoom"
)

p1 = f1.circle(
    x='ax',
    y='ay',
    source=source,
    radius=0.02,
    line_width=0,
    fill_alpha=0.5,
    legend_label='ax(t) vs ay(t)'
)


# --- Scatter iR vs iS ---
f2 = figure(
    width=300,
    height=300,
    tools="crosshair,box_select,pan,reset,wheel_zoom"
)

p2 = f2.circle(
    x='iR',
    y='iS',
    source=source,
    radius=0.02,
    line_width=0,
    fill_alpha=0.5,
    legend_label='iR(t) vs iS(t)'
)


# --- Señal temporal ---
f3 = figure(
    width=600,
    height=300,
    tools="xbox_zoom,crosshair,xbox_select,xpan,reset,xwheel_zoom"
)

p3 = f3.scatter(
    x='t',
    y='calculada',
    source=source,
    size=3,
    fill_alpha=0.6,
    legend_label='variable calculada'
)

p4 = f3.line(
    x='t',
    y='calculada',
    source=source,
    line_width=1,
    line_color='red',
    line_alpha=0.5
)


# ------------------------------------------------------------
# GLYPHS DE SELECCIÓN (ROBUSTO PARA BOKEH 3.x)
# ------------------------------------------------------------

p1.selection_glyph = p1.glyph.clone(fill_color="firebrick", fill_alpha=1)
p1.nonselection_glyph = p1.glyph.clone(fill_color="blue", fill_alpha=0.2)

p2.selection_glyph = p2.glyph.clone(fill_color="firebrick", fill_alpha=1)
p2.nonselection_glyph = p2.glyph.clone(fill_color="blue", fill_alpha=0.2)

p3.selection_glyph = p3.glyph.clone(fill_color="firebrick", fill_alpha=1)
p3.nonselection_glyph = p3.glyph.clone(fill_color="blue", fill_alpha=0.2)


# ------------------------------------------------------------
# TEXTO EXPLICATIVO
# ------------------------------------------------------------

div = Div(
    text=f"""
<h1>Uso de un DataFrame como fuente de datos</h1>
<h4>Ignacio Díaz Blanco, 2026. Universidad de Oviedo</h4>

<table>
<td valign="top">
<p>En este ejemplo usamos un <i>DataFrame</i> como fuente de datos.</p>

{df.head().to_html(border=0)}

<p>El objeto <i>ColumnDataSource</i> sincroniza todas las figuras.
Cualquier selección se refleja automáticamente en todas ellas.
Esto se conoce como <b>linking</b>.</p>
</td>

<td valign="top">
<p>Prueba a seleccionar puntos en cualquiera de las figuras
y observa cómo la selección se propaga al resto.</p>
</td>
</table>

<a href="fuentes/{__file__.split('.')[0]}_codigofuente.html">(código fuente)</a>
""",
    width=700
)


# ------------------------------------------------------------
# LAYOUT FINAL
# ------------------------------------------------------------

lay = layout([
    [div],
    [f1, f2, f3]
])

show(lay)