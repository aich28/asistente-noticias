import streamlit as st
import requests
import openai

# --- Configura tus claves aquí ---
GNEWS_API_KEY = "20209fda6b84290a761aedcbad1e8a6f"
OPENAI_API_KEY = "aquí_tu_api_key_de_openai"

# --- Interfaz con Streamlit ---
st.set_page_config(page_title="Asistente de Noticias", page_icon="📰")
st.title("📰 Asistente de Noticias")

tema = st.text_input("¿Sobre qué tema quieres ver noticias?", placeholder="Ejemplo: energías renovables")
buscar = st.button("Buscar noticias")

if buscar and tema:
    # 1. Buscar noticias en GNews
    url = f"https://gnews.io/api/v4/search?q={tema}&lang=es&max=10&apikey={GNEWS_API_KEY}"
    response = requests.get(url)
    datos = response.json()

    # 2. Preparar texto para OpenAI
    noticias = datos.get("articles", [])
    lista = ""
    for i, noticia in enumerate(noticias, 1):
        lista += f"{i}. {noticia['title']}\n{noticia['url']}\n\n"

    prompt = f"""El usuario ha solicitado noticias sobre "{tema}". Estas son las noticias reales encontradas:

{lista}

Organízalas en una lista clara con títulos y enlaces, sin resúmenes ni explicaciones. Formato limpio y listo para mostrar en pantalla o correo.
"""

    # 3. Llamada a OpenAI
    openai.api_key = OPENAI_API_KEY
    respuesta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Eres un asistente de noticias. Devuelve solo una lista clara con titulares y enlaces."},
            {"role": "user", "content": prompt}
        ]
    )

    resultado = respuesta["choices"][0]["message"]["content"]
    st.markdown("### ✅ Resultados:")
    st.markdown(resultado)