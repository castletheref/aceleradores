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
#Zona	Nombre del gestor	Bucket Inicial	Cuentas Asignadas	Cuentas Contenidas	Flujo Domiciliacion	Porcentaje de contencion	Arancel	Monto Acelerador	Distrito

st.title("📊 Dashboard Aceleradores Campo")

# Filtros
zona_seleccionada = st.selectbox("Selecciona una Zona", df["Zona"].unique())
gestor_seleccionado = st.selectbox("Selecciona un Gestor", df[df["Zona"] == zona_seleccionada]["Nombre del gestor"].unique())

df_filtrado = df[(df["Zona"] == zona_seleccionada) & (df["Nombre del Gestor"] == gestor_seleccionado)]

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Cuentas Asignadas", df_filtrado["Cuentas Asignadas"].sum())
col2.metric("Cuentas Contenidas", df_filtrado["Cuentas Contenidas"].sum())
col3.metric("Flujo domiciliacion", f"${df_filtrado['Flujo Domiciliacion'].sum():,.2f}")
# Calcular la suma de la columna 'acelerador' para la zona seleccionada
suma_acelerador = df_filtrado["Monto Acelerador"].sum()

# Mostrar el insight adicional
#col4 = st.columns(1)[0]
col4.metric("Monto Aceleradores", f"{suma_acelerador:,.2f}")


# Tabla de datos
st.subheader("📌 Datos Detallados")
st.dataframe(df_filtrado)

