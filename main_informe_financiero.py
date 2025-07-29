import streamlit as st
from PIL import Image

# Configuración de la página
st.set_page_config(
    page_title="Informe Financiero PyME",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título
st.title("📊 Sistema de Informes Financieros para PYMEs")
st.markdown("Generador de informes ejecutivos de alta calidad especializado en PYMEs españolas.")

# Menú de navegación
opcion = st.sidebar.selectbox(
    "Selecciona el informe que deseas visualizar:",
    [
        "🔎 Ratios Financieros",
        "💸 Flujo de Caja",
        "📈 Evolución Histórica",
        "📊 Cuenta de Resultados",
        "📚 Balance de Situación"
    ]
)

# Mostrar gráficos según selección
if opcion == "🔎 Ratios Financieros":
    st.subheader("Ratios Financieros Clave")
    st.image("ratios_financieros.png", use_column_width=True)

elif opcion == "💸 Flujo de Caja":
    st.subheader("Flujo de Caja")
    st.image("flujo_caja.png", use_column_width=True)

elif opcion == "📈 Evolución Histórica":
    st.subheader("Evolución Histórica")
    st.image("evolucion_historica.png", use_column_width=True)

elif opcion == "📊 Cuenta de Resultados":
    st.subheader("Cuenta de Resultados")
    st.image("cuenta_resultados.png", use_column_width=True)

elif opcion == "📚 Balance de Situación":
    st.subheader("Balance de Situación")
    st.image("balance_situacion.png", use_column_width=True)

# Pie de página
st.markdown("---")
st.caption("Desarrollado por Mi Empresa S.L. | Análisis financiero personalizado para pymes.")
