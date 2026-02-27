# Analítica Visual con Python y Bokeh

Este repositorio contiene los materiales, ejemplos interactivos y datasets del seminario de **Analítica Visual** impartido por el **Dr. Ignacio Díaz Blanco** (Universidad de Oviedo). 

El objetivo es explorar técnicas de visualización interactiva para el análisis de datos complejos, desde series temporales de motores industriales hasta demanda energética.

---

## 🚀 Contenidos del Tutorial

Los ejemplos están clasificados por niveles de complejidad técnica y funcional:

### Nivel 1: Fundamentos y Fuentes de Datos
* Demo 1a: LinePlot básico
* Demo 1b: Datos de vibraciones y corrientes (Motor)
* Demo 1c: Análisis de órbitas
* Demo 1d: ColumnDataSource y selecciones enlazadas
* Demo 1e: Visualización avanzada de datos de motor

### Nivel 2: Codificación Visual y Gráficas Coordinadas
* Demo 2a: Scatterplot básico
* Demo 2b: Scatterplot con escala de color continua
* Demo 2c: Visualización espiral de demanda eléctrica
* Demo 2d: Espiral + LinePlot (Interacción enlazada)
* Demo 2e: Matriz de demanda eléctrica (Hora vs Día)
* Demo 2f: Proyección t-SNE (Estados del motor)

### Nivel 3: Interacción Avanzada y Streaming
* Demo 3a: Callbacks de JavaScript
* Demo 3b: Bokeh Server (Callbacks en Python)
* Demo 3c: Streaming de datos en tiempo real (Santander)
* Demo 3d: Brushing de consumos
* Demo 3e: Morphing Projections

---

## 📊 Datasets Utilizados

Para reproducir los ejemplos localmente, descarga los siguientes archivos en la carpeta de trabajo:

- `iris_con_categorias.csv`: Datos de flores con categorías.
- `dataicann.mat`: Vibraciones y corrientes de motor de inducción.
- `dataicann_features.hdf`: Características extraídas del dataset de motor.
- `demanda_electrica.csv`: Histórico de consumo de un edificio.

---

## ▶️ Instrucciones para reproducir los ejemplos

Para ejecutar los scripts del repositorio en tu ordenador, sigue estos pasos:

### 1️⃣ Clonar el repositorio

```bash
git clone <URL-del-repositorio>
cd ejemplos-curso-VD
```

---

### 2️⃣ Crear un entorno virtual

Este proyecto requiere Python 3.14 o superior (según `pyproject.toml`).

```bash
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
# .venv\Scripts\activate    # Windows
```

---

### 3️⃣ Instalar dependencias

#### Opción recomendada (reproducible con uv)

Si tienes `uv` instalado:

```bash
# Instalar uv (solo la primera vez)
pip install uv

# Crear entorno y sincronizar dependencias
uv sync
```

Esto creará automáticamente el entorno virtual y instalará exactamente las versiones definidas en `pyproject.toml` y fijadas en `uv.lock`, garantizando reproducibilidad.

---

### 4️⃣ Ejecutar un ejemplo

```bash
python demo1a_lineplot.py
```

Cada script genera un archivo `.html` que se abrirá en tu navegador.