import streamlit as st
import pandas as pd
import openpyxl

# Configuración del dashboard (Debe ir antes que cualquier otro comando de Streamlit)
st.set_page_config(page_title="Aceleradores Campo", layout="wide")

# Cargar datos
@st.cache_data
def load_data():
    file_path = 'https://raw.githubusercontent.com/castletheref/aceleradores/master/dataaceleradores.xlsx'
    df = pd.read_excel(file_path, sheet_name="Hoja1", engine='openpyxl')
    return df

df = load_data()

st.title("📊 Aceleradores Campo")

# Filtro de Distrito
distrito_seleccionado = st.selectbox("Selecciona un Distrito", ["Todos"] + df["Distrito"].unique().tolist())

# Filtrar las zonas basadas en el distrito seleccionado
if distrito_seleccionado == "Todos":
    zonas_disponibles = df["Zona"].unique()
else:
    zonas_disponibles = df[df["Distrito"] == distrito_seleccionado]["Zona"].unique()

# Filtro de Zona
zona_seleccionada = st.selectbox("Selecciona una Zona", zonas_disponibles)

# Obtener el nombre del gestor correspondiente a la zona seleccionada
gestor_seleccionado = df[df["Zona"] == zona_seleccionada]["Nombre del gestor"].unique()

# Asegurar que hay un gestor para la zona seleccionada
if len(gestor_seleccionado) > 0:
    gestor_seleccionado = gestor_seleccionado[0]  # Tomar el primer gestor encontrado
else:
    gestor_seleccionado = "No disponible"  # Mensaje si no hay gestor en la zona

# Mostrar el nombre del gestor en un campo de solo lectura
st.text_input("Nombre del gestor", value=gestor_seleccionado, disabled=True)

# Filtrar el DataFrame según la zona y el gestor seleccionado
df_filtrado = df[(df["Zona"] == zona_seleccionada) & (df["Nombre del gestor"] == gestor_seleccionado)]


# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Cuentas Asignadas", df_filtrado["Cuentas Asignadas"].sum())
col2.metric("Cuentas Contenidas", df_filtrado["Cuentas Contenidas"].sum())
col3.metric("Flujo domiciliacion", f"${df_filtrado['Flujo Domiciliacion'].sum():,.2f}")
suma_acelerador = df_filtrado["Monto Acelerador"].sum()
col4.metric("Monto Aceleradores", f"${suma_acelerador:,.2f}")


# Tabla de datos
st.subheader("📌 Datos Detallados")
st.dataframe(df_filtrado)

