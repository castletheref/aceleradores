import streamlit as st
import pandas as pd
import openpyxl

# Configuración del dashboard (Debe ir antes que cualquier otro comando de Streamlit)
st.set_page_config(page_title="Dashboard de Aceleradores", layout="wide")

# Cargar datos
@st.cache_data
def load_data():
    file_path = 'https://raw.githubusercontent.com/castletheref/aceleradores/master/dataaceleradores.xlsx'
    df = pd.read_excel(file_path, sheet_name="Hoja1", engine='openpyxl')
    return df

df = load_data()

st.title("📊 Dashboard de Aceleradores")

# Filtros
zona_seleccionada = st.selectbox("Selecciona una Zona", df["zona_campo"].unique())
gestor_seleccionado = st.selectbox("Selecciona un Gestor", df[df["zona_campo"] == zona_seleccionada]["name"].unique())

df_filtrado = df[(df["zona_campo"] == zona_seleccionada) & (df["name"] == gestor_seleccionado)]

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Cuentas Asignadas", df_filtrado["cuentas_asig"].sum())
col2.metric("Cuentas Contenidas", df_filtrado["cuentas_cont"].sum())
col3.metric("Flujo DOMI", f"${df_filtrado['Flujo_DOMI'].sum():,.2f}")
# Calcular la suma de la columna 'acelerador' para la zona seleccionada
suma_acelerador = df_filtrado["acelerador"].sum()

# Mostrar el insight adicional
#col4 = st.columns(1)[0]
col4.metric("Suma Aceleradores", f"{suma_acelerador:,.2f}")


# Tabla de datos
st.subheader("📌 Datos Detallados")
st.dataframe(df_filtrado)

