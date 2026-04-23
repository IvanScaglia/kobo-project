import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Tablero KoBo Pro", layout="wide")

# Estética Profesional
st.markdown("""
    <style>
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e1e4e8; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def cargar_datos():
    return pd.read_csv("datos_kobo_reducido_70.csv", sep=None, engine='python', on_bad_lines='skip')

try:
    df = cargar_datos()
    
    st.title("📊 Análisis de Relevamiento Observacional")
    st.info("Visualización profesional de datos recolectados vía KoBoCollect.")

    # 1. MÉTRICAS CLAVE
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Relevamientos", len(df))
    col2.metric("Variables", len(df.columns))
    
    # 2. FILTRADO DE COLUMNAS (Para que no aparezcan los IDs feos)
    # Solo mostramos columnas que tengan nombres descriptivos
    columnas_analisis = [c for c in df.columns if not any(x in c.lower() for x in ['id', 'uuid', 'index', 'version', 'submission', 'notes'])]
    
    st.divider()

    # 3. ANÁLISIS DINÁMICO
    c1, c2 = st.columns([1, 2])
    
    with c1:
        st.subheader("Configuración")
        opcion = st.selectbox("¿Qué pregunta querés analizar?", columnas_analisis)
        
        # Resumen rápido en texto
        top_val = df[opcion].value_counts().idxmax()
        st.write(f"**Valor más frecuente:** \n\n {top_val}")
        
    with c2:
        # Gráfico interactivo con Plotly (se ve mucho mejor que el básico)
        fig_df = df[opcion].value_counts().reset_index()
        fig_df.columns = [opcion, 'Cantidad']
        
        fig = px.bar(fig_df.head(10), x=opcion, y='Cantidad', 
                     color='Cantidad', color_continuous_scale='Viridis',
                     title=f"Distribución de: {opcion}")
        st.plotly_chart(fig, use_container_width=True)

    # 4. TABLA DE EXPLORACIÓN
    st.divider()
    st.subheader("🔍 Explorador de Datos Completo")
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Error al procesar: {e}")
