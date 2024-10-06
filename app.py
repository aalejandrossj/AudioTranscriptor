import streamlit as st
import whisper
import os
import tempfile

# Función para añadir CSS personalizado
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Saira:wght@100;300;400;500;600;700&family=Ubuntu:wght@300;400;500;700&display=swap');

    /* Título del sitio */
    .css-18e3th9 {
        font-family: 'Saira', sans-serif;
        font-weight: 500; /* Medium */
        font-size: 30px;
    }

    /* Fuente del cuerpo */
    .css-1d391kg {
        font-family: 'Ubuntu', sans-serif;
        font-weight: 400; /* Regular */
        font-size: 16px;
    }

    /* Fuente H1 */
    h1 {
        font-family: 'Saira', sans-serif;
        font-weight: 400; /* Regular */
        font-size: 36px;
    }

    /* Fuente H2 */
    h2 {
        font-family: 'Saira', sans-serif;
        font-weight: 400; /* Regular */
        font-size: 26px;
    }

    /* Fuente H3 */
    h3 {
        font-family: 'Saira', sans-serif;
        font-weight: 400; /* Regular */
        font-size: 22px;
    }

    /* Fuente H4 */
    h4 {
        font-family: 'Saira', sans-serif;
        font-weight: 400; /* Regular */
        font-size: 18px;
    }

    /* Fuente H5 */
    h5 {
        font-family: 'Saira', sans-serif;
        font-weight: 400; /* Regular */
        font-size: 16px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.title("Transcripción de Audio")

# Función para marcar los tiempos en la transcripción
def mark_times(result):
    marked_transcription = ""
    for segment in result["segments"]:
        start_time = segment["start"]
        minutes = int(start_time // 60)
        seconds = int(start_time % 60)
        timestamp = f"{minutes:02}:{seconds:02}"
        marked_transcription += f" {timestamp}: {segment['text']}\n"
    return marked_transcription

# Función para ejecutar la transcripción
def run_transcription(audio_filename, model):
    try:
        result = model.transcribe(audio_filename)
        return mark_times(result)
    except Exception as e:
        return f"Ocurrió un error durante la transcripción: {e}"

# Función para cargar el modelo Whisper
def load_whisper_model():
    return whisper.load_model("small")

# Interfaz de usuario
uploaded_file = st.file_uploader("Suba un archivo de audio", type=["mp3", "wav", "m4a"])

# Botón para transcribir
if st.button("Transcribir"):
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.read())
            audio_filename = tmp_file.name

        with st.spinner("Transcribiendo..."):
            model = load_whisper_model()
            transcription = run_transcription(audio_filename, model)
        
        st.subheader("Transcripción:")
        st.text_area("", value=transcription, height=300)

        # Limpieza de archivos temporales
        os.remove(audio_filename)
    else:
        st.warning("Por favor, suba un archivo de audio")
