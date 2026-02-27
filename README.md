# Analítica Visual con Python y Bokeh

Este repositorio contiene los materiales, ejemplos interactivos y datasets del seminario de **Analítica Visual** impartido por el **Dr. Ignacio Díaz Blanco** (Universidad de Oviedo). 

El objetivo es explorar técnicas de visualización interactiva para el análisis de datos complejos, desde series temporales de motores industriales hasta demanda energética.

---

## 🚀 Contenidos del Tutorial

Los ejemplos están clasificados por niveles de complejidad técnica y funcional:

### Nivel 1: Fundamentos y Gestión de Datos
* [Demo 1a: LinePlot básico](http://isa.uniovi.es/~idiaz/master_uv/archivos/demo1a_plot_basico.html) — Código: [demo1a_plot_basico.py](demo1a_plot_basico.py)
* [Demo 1b: Datos de vibraciones y corrientes (Motor)](http://isa.uniovi.es/~idiaz/master_uv/archivos/demo1b_plot_basico_dataicann.html) — Código: [demo1b_plot_basico_dataicann.py](demo1b_plot_basico_dataicann.py)
* [Demo 1c: Análisis de órbitas](http://isa.uniovi.es/~idiaz/master_uv/archivos/demo1c_plot_basico_dataicann_orbitas.html) — Código: [demo1c_plot_basico_dataicann_orbitas.py](demo1c_plot_basico_dataicann_orbitas.py)
* [Demo 1d: ColumnDataSource y selecciones enlazadas](http://isa.uniovi.es/~idiaz/master_uv/archivos/demo1d_plot_basico_source.html) — Código: [demo1d_plot_basico_source.py](demo1d_plot_basico_source.py)
* [Demo 1e: Visualización avanzada de datos de motor](http://isa.uniovi.es/~idiaz/master_uv/archivos/demo1e_plot_basico_source_dataicann.html) — Código: [demo1e_plot_basico_source_dataicann.py](demo1e_plot_basico_source_dataicann.py)

### Nivel 2: Codificación Visual y Gráficas Coordinadas
* [Demo 2a: Scatterplot básico](http://isa.uniovi.es/~idiaz/master_uv/archivos/demo2a_scatter_basico.html) — Código: [demo2a_scatter_basico.py](demo2a_scatter_basico.py)
* [Demo 2b: Scatterplot con escala de color continua](http://isa.uniovi.es/~idiaz/master_uv/archivos/demo2b_scatter_basico_escala_continua.html) — Código: [demo2b_scatter_basico_escala_continua.py](demo2b_scatter_basico_escala_continua.py)
* [Demo 2c: Visualización espiral de demanda eléctrica](http://isa.uniovi.es/~idiaz/master_uv/archivos/demo2c_scatter_espiral_consumos.html) — Código: [demo2c_scatter_espiral_consumos.py](demo2c_scatter_espiral_consumos.py)
* [Demo 2d: Espiral + LinePlot (Interacción enlazada)](http://isa.uniovi.es/~idiaz/master_uv/archivos/demo2d_scatter_espiral_consumos_interactiva.html) — Código: [demo2d_scatter_espiral_consumos_interactiva.py](demo2d_scatter_espiral_consumos_interactiva.py)
* [Demo 2e: Matriz de demanda eléctrica (Hora vs Día)](http://isa.uniovi.es/~idiaz/master_uv/archivos/demo2e_scatter_matricial_consumos_interactiva.html) — Código: [demo2e_scatter_matricial_consumos_interactiva.py](demo2e_scatter_matricial_consumos_interactiva.py)
* [Demo 2f: Proyección t-SNE (Estados del motor)](http://isa.uniovi.es/~idiaz/master_uv/archivos/demo2f_dataicann_tsne.html) — Código: [demo2f_dataicann_tsne.py](demo2f_dataicann_tsne.py)

### Nivel 3: Interacción Avanzada y Streaming
* [Demo 3a: Callbacks de JavaScript](http://isa.uniovi.es/~idiaz/master_uv/archivos/demo3a_interaccion_callback_javascript.html) — Código: [demo3a_interaccion_callback_javascript.py](demo3a_interaccion_callback_javascript.py)
* [Demo 3b: Bokeh Server (Callbacks en Python)](http://isa.uniovi.es/~idiaz/master_uv/archivos/fuentes/demo3b_interaccion_callback_python_codigofuente.html) — Código: [demo3b_interaccion_callback_python.py](demo3b_interaccion_callback_python.py)
* [Demo 3c: Streaming de datos en tiempo real (Santander)](http://isa.uniovi.es/~idiaz/master_uv/archivos/fuentes/demo3c_streaming_codigofuente.html) — Código: [demo3c_streaming.py](demo3c_streaming.py)
* [Demo 3d: Brushing de consumos](http://isa.uniovi.es/~idiaz/master_uv/archivos/demo3d_brushing_consumos.html) — Código: [demo3d_brushing_consumos.py](demo3d_brushing_consumos.py)
* [Demo 3e: Morphing Projections](http://isa.uniovi.es/~idiaz/master_uv/archivos/demo3e_morphing_consumos.html) — Código: [demo3e_morphing_consumos.py](demo3e_morphing_consumos.py)

---

## 📊 Datasets Utilizados

Para reproducir los ejemplos localmente, descarga los siguientes archivos en una carpeta `datasets/`:

| Dataset | Formato | Descripción |
| :--- | :--- | :--- |
| [Iris Dataset](http://isa.uniovi.es/~idiaz/master_uv/archivos/datasets/iris_con_categorias.csv) | CSV | Datos de flores con categorías. |
| [Dataicann Motor](http://isa.uniovi.es/~idiaz/master_uv/archivos/datasets/dataicann.mat) | MAT | Vibraciones y corrientes de motor de inducción. |
| [Dataicann Features](http://isa.uniovi.es/~idiaz/master_uv/archivos/datasets/dataicann_features.hdf) | HDF | Características extraídas del dataset de motor. |
| [Demanda Eléctrica](http://isa.uniovi.es/~idiaz/master_uv/archivos/datasets/demanda_electrica.csv) | CSV | Histórico de consumo de un edificio. |

---

## 🛠️ Requisitos Técnicos

Se recomienda utilizar un entorno de **Anaconda** con Python 3.8+:

```bash
# Instalación de librerías base
conda install ipython numpy matplotlib pandas bokeh scikit-learn pytables requests