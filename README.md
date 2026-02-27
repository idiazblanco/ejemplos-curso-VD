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

#### Opción rápida (manual)

```bash
pip install bokeh ipython matplotlib pandas requests scikit-learn tables
```

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