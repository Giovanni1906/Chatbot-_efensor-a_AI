import streamlit as st
from PIL import Image
import time
from dotenv import load_dotenv
import os
from utils import run_excecuter
from openai import OpenAI

load_dotenv()

# Configuración general
st.set_page_config(page_title="Asistente Defensoría Universitaria - UNJBG", page_icon="🎓")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
assistant_id = os.getenv("ASSISTANT_ID")
print("assistant id: ", assistant_id)

# Logo institucional
image = Image.open('src/images/defensoria-unjbg.png')
st.image(image, use_container_width=True)

# Título
st.markdown(
    "<h2 style='text-align: center; color: #f2f2f2;'>Asistente Virtual - Defensoría Universitaria UNJBG - Jorge Velásquez</h2>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center; color: #f2f2f2;'>Este asistente te ayudará a resolver consultas relacionadas a la ley universitaria 30220.</p>",
    unsafe_allow_html=True
)

# Inicializar sesión
if "thread_id" not in st.session_state:
    st.session_state.thread_id = client.beta.threads.create().id
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial de mensajes
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Efecto máquina de escribir
def typewriter(text: str, speed: int):
    tokens = text.split()
    container = st.empty()
    for index in range(len(tokens) + 1):
        container.markdown(" ".join(tokens[:index]))
        time.sleep(1 / speed)

# Entrada del usuario
if prompt := st.chat_input("Escribe tu consulta..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_box = client.beta.threads.messages.create(thread_id=st.session_state.thread_id, role="user", content=prompt)

        run = client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=assistant_id
        )

        with st.spinner('La Defensoría está procesando tu mensaje...'):
            st.toast('Gracias por tu confianza. Pronto recibirás una respuesta.', icon='📨')
            run_excecuter(run)
            message_assistant = client.beta.threads.messages.list(thread_id=st.session_state.thread_id).data[0].content[0].text.value

        typewriter(message_assistant, 50)

    st.session_state.messages.append({"role": "assistant", "content": message_assistant})