import streamlit as st
import pandas as pd

# 1. Configuración de la página (esto siempre arriba de todo)
st.set_page_config(
    page_title="Tablero de Control KoBo - Iván Scaglia",
    page_icon="📊",
    layout="wide"
)

# Estilo personalizado para que se vea más pro
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Función para cargar los datos con "escudo" contra errores
@st.cache_data
def cargar_datos():
    # El parámetro 'on_bad_lines' hace que si la fila 16 está rota, la salte y siga
    # El parámetro 'sep=None' detecta automáticamente si es , o ;
    df = pd.read_csv(
        "datos_kobo_reducido_70.csv", 
        sep=None, 
        engine='python', 
        on_bad_lines='skip',
        encoding='utf-8'
    )
    return df

# 3. Títulos y presentación
st.title("📊 Monitor de Relevamiento Observacional")
st.markdown("---")

try:
    df = cargar_datos()

    # 4. Indicadores clave (KPIs)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total de Registros", f"{len(df):,}")
    
    with col2:
        # Intentamos contar comunas si la columna existe
        if 'comuna' in df.columns:
            st.metric("Comunas Cubiertas", df['comuna'].nunique())
        else:
            st.metric("Columnas Detectadas", len(df.columns))
            
    with col3:
        st.success("Base de datos conectada")

    st.markdown("---")

    # 5. Gráficos interactivos
    st.subheader("📈 Análisis por Categoría")
    
    # Filtramos columnas que no sirven para graficar (como IDs o fechas largas)
    columnas_utiles = [c for c in df.columns if not c.startswith('_')]
    
    seleccion = st.selectbox("Elegí una categoría para visualizar el gráfico:", columnas_utiles)

    if seleccion:
        datos_grafico = df[seleccion].value_counts().head(15)
        st.bar_chart(datos_grafico)

    # 6. Tabla de datos para el portfolio
    st.markdown("---")
    st.subheader("🔍 Explorador de Datos")
    with st.expander("Hacé clic para ver la tabla completa"):
        st.write("Podés ordenar las columnas haciendo clic en los encabezados.")
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error("⚠️ Hubo un problema al cargar el archivo.")
    st.info("Asegurate de que el archivo 'datos_kobo_reducido_70.csv' esté en la carpeta raíz de GitHub.")
    st.write(f"Detalle del error: {e}")

# 7. Créditos (opcional para tu portfolio)
st.sidebar.markdown("### Desarrollado por:")
st.sidebar.write("Iván Scaglia")
st.sidebar.write("Data Analyst")
