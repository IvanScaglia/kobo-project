import streamlit as st
import pandas as pd

st.set_page_config(page_title="Análisis KoBo", layout="wide")
st.title("📊 Visualizador de Datos KoBo")

# Cargamos el archivo que ya tenés en GitHub
@st.cache_data
def cargar_datos():
    return pd.read_csv("datos_kobo_reducido_70.csv")

try:
    df = cargar_datos()
    st.metric("Total de Registros", len(df))

    # Mostramos un gráfico simple
    columna = st.selectbox("Seleccioná una columna para graficar:", df.columns)
    st.bar_chart(df[columna].value_counts())

    st.subheader("Vista de los datos")
    st.dataframe(df)
except Exception as e:
    st.error(f"Error: {e}")
