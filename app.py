# app.py
"""
Streamlit app for exploring used car data.
Features:
- Dynamic filtering by manufacturer, type, price, odometer, and model year.
- Visualizations including scatter plots, box plots, and histograms.
- Data download functionality.
"""

import io
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Used Cars Insights", page_icon="🚗", layout="wide")

# -----------------------------
# Data loading with cache
# -----------------------------
@st.cache_data(show_spinner=False)
def load_data(file: io.BytesIO | str = "vehicles_us.csv") -> pd.DataFrame:
    df = pd.read_csv(file)
    # Limpieza mínima y nombres consistentes
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    # Coerción de numéricos comunes
    for col in ["price", "odometer", "model_year"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    # Drop duplicados triviales
    df = df.drop_duplicates()
    return df

# -----------------------------
# Sidebar: carga/archivo y filtros
# -----------------------------
st.sidebar.header("Filtros")

uploaded = st.sidebar.file_uploader("Sube un CSV alternativo (opcional)", type=["csv"])
if uploaded:
    data = load_data(uploaded)
else:
    try:
        data = load_data()
    except FileNotFoundError:
        st.error("No se encontró `vehicles_us.csv`. Sube un archivo CSV mediante el panel lateral.")
        st.stop()

# Filtros dinámicos
manufacturers = sorted([m for m in data.get("manufacturer", pd.Series()).dropna().unique()])
types = sorted([t for t in data.get("type", pd.Series()).dropna().unique()])

min_price, max_price = float(data["price"].min()), float(data["price"].clip(upper=data["price"].quantile(0.99)).max())
price_range = st.sidebar.slider("Rango de precio", min_price, max_price, (min_price, max_price), step=1000.0)

min_odo, max_odo = float(data["odometer"].min()), float(data["odometer"].clip(upper=data["odometer"].quantile(0.99)).max())
odo_range = st.sidebar.slider("Rango de odómetro", min_odo, max_odo, (min_odo, max_odo), step=1000.0)

years = data["model_year"].dropna().astype(int) if "model_year" in data else pd.Series([], dtype=int)
year_min, year_max = (int(years.min()), int(years.max())) if not years.empty else (2000, 2024)
year_range = st.sidebar.slider("Rango de año (model_year)", year_min, year_max, (year_min, year_max))

manu_sel = st.sidebar.multiselect("Fabricante", options=manufacturers, default=manufacturers[:5] if manufacturers else [])
type_sel = st.sidebar.multiselect("Tipo de vehículo", options=types, default=types if types else [])

log_price = st.sidebar.checkbox("Usar escala log en precio", value=False)

# Aplicar filtros
df = data.copy()
if manu_sel:
    df = df[df["manufacturer"].isin(manu_sel)]
if type_sel:
    df = df[df["type"].isin(type_sel)]
df = df[(df["price"].between(price_range[0], price_range[1], inclusive="both")) &
        (df["odometer"].between(odo_range[0], odo_range[1], inclusive="both"))]
if "model_year" in df.columns:
    df = df[df["model_year"].between(year_range[0], year_range[1], inclusive="both")]

# -----------------------------
# Header + KPIs
# -----------------------------
st.title("Used Cars Insights")
st.caption("Explora cómo el precio varía por odómetro, marca, año y tipo.")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Registros filtrados", f"{len(df):,}")
with c2:
    st.metric("Precio promedio", f"${df['price'].mean():,.0f}" if "price" in df else "N/A")
with c3:
    st.metric("Mediana precio", f"${df['price'].median():,.0f}" if "price" in df else "N/A")
with c4:
    st.metric("Odómetro promedio", f"{df['odometer'].mean():,.0f} mi" if "odometer" in df else "N/A")

# -----------------------------
# Visualizaciones
# -----------------------------
tab1, tab2, tab3 = st.tabs(["Dispersión", "Boxplot por marca", "Modelos populares"])

with tab1:
    if {"odometer", "price"} <= set(df.columns):
        fig = px.scatter(
            df, x="odometer", y="price",
            color=df["type"] if "type" in df else None,
            hover_data=[c for c in ["manufacturer", "model", "model_year"] if c in df.columns],
            title="Precio vs. Odómetro"
        )
        if log_price:
            fig.update_yaxes(type="log")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Faltan columnas `odometer` y/o `price` para esta vista.")

with tab2:
    if {"price", "manufacturer"} <= set(df.columns):
        top_manu = df["manufacturer"].value_counts().head(12).index
        dfx = df[df["manufacturer"].isin(top_manu)]
        fig = px.box(dfx, x="manufacturer", y="price", points="suspectedoutliers", title="Distribución de precio por fabricante (Top 12)")
        if log_price:
            fig.update_yaxes(type="log")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Faltan columnas `manufacturer` y/o `price` para esta vista.")

with tab3:
    if "model" in df.columns:
        counts = df["model"].value_counts()
        popular = counts[counts >= 1000] if (counts >= 1000).any() else counts.head(20)
        dfx = df[df["model"].isin(popular.index)]
        fig = px.histogram(dfx, x="model", title="Modelos con más listados")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No se encontró la columna `model`.")

# -----------------------------
# Data Preview + Download
# -----------------------------
st.subheader("Datos filtrados")
st.dataframe(df.head(1000))
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("📥 Descargar CSV filtrado", data=csv, file_name="used_cars_filtered.csv", mime="text/csv")

st.markdown("---")
st.caption("Hecho con ❤️ por Raul Rey — Pandas · Plotly · Streamlit")