import streamlit as st
import pandas as pd
import openpyxl

# Configuración del dashboard
st.set_page_config(page_title="Dashboard PF", page_icon=":smiley:", layout='wide')


# CSS para ocultar la sidebar después de la selección
hide_sidebar_style = """
    <style>
        [data-testid="stSidebar"] {display: none;}
    </style>
"""

# Sidebar para seleccionar el reporte
st.sidebar.title("Selecciona un Reporte")
reporte_seleccionado = st.sidebar.radio("Reportes", ["Resumen", "Aceleradores Campo"])

# Si el usuario selecciona un reporte, ocultar el sidebar
st.markdown(hide_sidebar_style, unsafe_allow_html=True)

# Función para cargar datos
@st.cache_data
def load_data(file_path, sheet_name):
    df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')
    return df

# Definir la fuente de datos según el reporte seleccionado
if reporte_seleccionado == "Aceleradores Campo":
    file_path = 'https://raw.githubusercontent.com/castletheref/aceleradores/master/dataaceleradores.xlsx'
    sheet_name = "Hoja1"
    df = load_data(file_path, sheet_name)
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
    gestor_seleccionado = gestor_seleccionado[0] if len(gestor_seleccionado) > 0 else "No disponible"

    # Mostrar el nombre del gestor en un campo de solo lectura
    st.text_input("Nombre del gestor", value=gestor_seleccionado, disabled=True)

    # Filtrar el DataFrame según la zona y el gestor seleccionado
    df_filtrado = df[(df["Zona"] == zona_seleccionada) & (df["Nombre del gestor"] == gestor_seleccionado)]

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Cuentas Asignadas", df_filtrado["Cuentas Asignadas"].sum())
    col2.metric("Cuentas Contenidas", df_filtrado["Cuentas Contenidas"].sum())
    col3.metric("Flujo domiciliacion", f"${df_filtrado['Flujo Domiciliacion'].sum():,.2f}")
    col4.metric("Monto Aceleradores", f"${df_filtrado['Monto Acelerador'].sum():,.2f}")

    # Tabla de datos
    st.subheader("📌 Datos Detallados")
    st.dataframe(df_filtrado)

elif reporte_seleccionado == "Resumen":
    file_path = 'https://raw.githubusercontent.com/castletheref/aceleradores/master/Resumen.xlsx'
    sheet_name = "Hoja1"
    df = load_data(file_path, sheet_name)
    st.title("📊 Resumen General")
    
    # Mostrar la tabla de datos completa
    st.subheader("📌 Datos del Resumen")
    st.dataframe(df)
