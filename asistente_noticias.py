import streamlit as st
import requests
import openai
import os

# ======================
# CONFIGURACIÓN
# ======================
# Puedes dejar esta clave fija o ponerla en Secrets si lo prefieres
GNEWS_API_KEY = "20209fda6b84290a761aedcbad1e8a6f"
openai.api_key = os.getenv("OPENAI_API_KEY")  # Se recomienda usar secrets

# ======================
# INTERFAZ
# ======================
st.set_page_config(page_title="Asistente de Noticias", page_icon="📰")
st.title("📰 Asistente de Noticias")
st.write("¿Sobre qué tema quieres ver noticias?")

tema = st.text_input("Ejemplo: energías renovables")
buscar = st.button("Buscar noticias")

# ======================
# LÓGICA
# ======================
if buscar and tema:
    st.info(f"Buscando noticias sobre: **{tema}**...")

    # 🔎 Paso 1: buscar en GNews
    url = f"https://gnews.io/api/v4/search?q={tema}&lang=es&max=10&token={GNEWS_API_KEY}"
    r = requests.get(url)
    noticias = r.json().get("articles", [])

    if noticias:
        st.success("Aquí tienes las últimas noticias:")
        for i, noticia in enumerate(noticias, start=1):
            st.markdown(f"**{i}. {noticia['title']}**\n\n🔗 [Ver noticia]({noticia['url']})\n")

        # Paso 2: ¿Enviar por correo?
        enviar = st.checkbox("¿Quieres que te lo envíe por correo?")
        if enviar:
            email = st.text_input("Introduce tu email")
            if email and st.button("Enviar resumen al correo"):
                st.warning("Funcionalidad pendiente de integración de envío por email ✉️")
    else:
        st.error("No se encontraron noticias sobre ese tema.")
