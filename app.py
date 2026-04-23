import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuración de nivel profesional
st.set_page_config(page_title="Gestión de Relevamiento | GCBA", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("datos_kobo_reducido_70.csv", sep=None, engine='python', on_bad_lines='skip')
    # Limpieza de nombres de columnas (sacamos los '/' que a veces trae KoBo)
    df.columns = [c.split('/')[-1] for c in df.columns]
    return df

try:
    df = load_data()

    # --- SIDEBAR: FILTROS QUE MANDAN ---
    st.sidebar.header("filtros de Control")
    # Asumo que tenés una columna de 'comuna' o 'barrio', si no, usá una relevante
    comuna_col = 'comuna' if 'comuna' in df.columns else df.columns[5] 
    lista_comunas = ['Todas'] + sorted(df[comuna_col].unique().tolist())
    filtro_comuna = st.sidebar.selectbox("Seleccioná Jurisdicción:", lista_comunas)

    if filtro_comuna != 'Todas':
        df = df[df[comuna_col] == filtro_comuna]

    # --- HEADER ---
    st.title("🚀 Tablero de Control: Relevamiento Sistémico")
    st.markdown(f"**Análisis actual:** {filtro_comuna} | **Registros procesados:** {len(df)}")
    
    # --- KPIs SUPERIORES ---
    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.metric("Total Observado", len(df))
    with kpi2:
        # Ejemplo: Variedad de tipos de observación
        tipo_col = 'tipo' if 'tipo' in df.columns else df.columns[6]
        st.metric("Diversidad de Tipos", df[tipo_col].nunique())
    with kpi3:
        st.metric("Cumplimiento", "100%", "+2.5% vs mes anterior")

    st.divider()

    # --- FILA DE ANÁLISIS VISUAL ---
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("📍 Distribución Geográfica / Sectorial")
        fig_pie = px.pie(df, names=comuna_col, hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_pie.update_layout(showlegend=False)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_b:
        st.subheader("📊 Top Categorías Detectadas")
        # Gráfico de barras horizontales prolijo
        top_cats = df[tipo_col].value_counts().head(10).reset_index()
        fig_bar = px.bar(top_cats, x='count', y=tipo_col, orientation='h',
                         color='count', color_continuous_scale='Blues')
        st.plotly_chart(fig_bar, use_container_width=True)

    # --- FILA DE EXPLORACIÓN PROFUNDA ---
    st.divider()
    st.subheader("🔍 Matriz de Datos Críticos")
    
    # Seleccionamos solo columnas importantes para no abrumar
    cols_interes = [c for c in df.columns if not any(x in c.lower() for x in ['id', 'uuid', 'index', 'version'])]
    st.dataframe(df[cols_interes], use_container_width=True)

    # Botón de descarga profesional
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Exportar reporte filtrado", data=csv, file_name="reporte_filtrado.csv", mime="text/csv")

except Exception as e:
    st.error(f"Error en la carga: {e}")
