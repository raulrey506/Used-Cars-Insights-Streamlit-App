# Used Cars Insights · Streamlit App

**Objetivo:** permitir a perfiles de negocio y técnicos explorar patrones de precio en autos usados (EE. UU.) y cómo varían por marca, año, tipo de carrocería y kilometraje.

> Pitch para reclutadores: Proyecto end-to-end con **Pandas + Plotly + Streamlit**, filtros interactivos, KPIs, descarga de datos filtrados y despliegue en Render. Código limpio, tests básicos y entorno reproducible.

---

## Demo
- Local: `streamlit run app.py`
- Render: al desplegar, URL pública (agregarla aquí).

## Principales funciones
- 📊 **KPIs** (promedio de precio, mediana, conteo tras filtros)
- 🧭 **Filtros** por año, marca, tipo, rango de precio y odómetro
- 🔎 **Gráficas**: dispersión (odometer vs price), boxplot por marca, histograma de modelos
- 💾 **Descarga** del subconjunto filtrado (CSV)
- ⚡ **Caching** para carga rápida

## Dataset
- Archivo: `vehicles_us.csv`
- Columnas típicas: `price`, `odometer`, `model`, `model_year`, `manufacturer`, `type`, etc.
- Fuente: dataset educativo (incluido en este repo).

## Estructura

proyecto-7/
├── app.py
├── vehicles_us.csv
├── requirements.txt
├── README.md
├── notebooks/           # análisis/EDA opcional
├── tests/
│   └── test_data.py     # smoke test de datos
├── .streamlit/
│   └── config.toml      # tema Streamlit
└── render.yaml          # despliegue en Render


## Cómo ejecutar (local)
```bash
# 1) Crear entorno (opción con venv)
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 2) Levantar la app
streamlit run app.py

Décadas de valor
	•	Modelado del proceso analítico (EDA → segmentos → señales de outliers)
	•	Trade-offs: precio vs odómetro por tipo de carrocería
	•	Uso de KPIs claros y UI simple orientada a negocio

    