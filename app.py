import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Profesional KoBo | Gestión Pública", layout="wide")

# Estilo para tarjetas de métricas
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 28px; color: #007bff; }
    .main { background-color: #f8f9fa; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("datos_kobo_reducido_70.csv", sep=None, engine='python', on_bad_lines='skip')
    # Limpiamos nombres de columnas complejos de KoBo
    df.columns = [c.split('/')[-1] for c in df.columns]
    return df

try:
    df = load_data()

    # --- TÍTULO Y CONTEXTO ---
    st.title("🏛️ Sistema de Monitoreo: Relevamiento Territorial")
    st.caption("Análisis avanzado de datos observacionales - Gobierno de la Ciudad")

    # --- KPIs DE IMPACTO ---
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Observaciones", len(df))
    
    # Buscamos columnas clave dinámicamente
    cat_cols = [c for c in df.columns if df[c].nunique() < 15 and df[c].nunique() > 1]
    
    m2.metric("Categorías Críticas", len(cat_cols))
    m3.metric("Comunas Activas", df['comuna'].nunique() if 'comuna' in df.columns else "N/A")
    m4.metric("Estado", "Activo", delta="Actualizado")

    st.divider()

    # --- ANÁLISIS CRUZADO (Lo que te hace Pro) ---
    st.subheader("📊 Análisis de Situación por Jurisdicción")
    
    col_a, col_b = st.columns([1, 1])

    with col_a:
        # Gráfico de Barras Agrupado: Cruce de dos variables
        eje_x = st.selectbox("Elegí dimensión principal (Comuna/Zona):", cat_cols, index=0)
        eje_color = st.selectbox("Cruzar por (Estado/Tipo):", cat_cols, index=1 if len(cat_cols)>1 else 0)
        
        fig = px.histogram(df, x=eje_x, color=eje_color, barmode="group",
                           title=f"Cruce: {eje_x} vs {eje_color}",
                           color_discrete_sequence=px.colors.qualitative.Bold)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        # Treemap: Para ver dónde está el peso del relevamiento
        st.write("") # Espaciador
        fig_tree = px.treemap(df, path=[eje_x, eje_color], 
                              title="Jerarquía de Datos (Tamaño por volumen)")
        st.plotly_chart(fig_tree, use_container_width=True)

    # --- EXPLORACIÓN DE DATOS ---
    with st.expander("🔍 Auditoría de Base de Datos (Dataset Completo)"):
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Fallo en la matriz de datos: {e}")
