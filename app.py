import streamlit as st
import speech_recognition as sr
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import tempfile
import os

# Initial Setup
translator = Translator()
recognizer = sr.Recognizer()

# Page Config
st.set_page_config(page_title="🌍 AI Speech Translator", layout="centered")
st.markdown("""
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 500px;
            margin: auto;
        }
        .stButton > button {
            width: 100%;
            padding: 0.75em;
            font-size: 1.1em;
            border-radius: 10px;
        }
        .stSelectbox > div {
            font-size: 1.1em;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🎙️ Real-Time AI Translator")
st.write("Break language barriers with voice!")

# Theme Switch
dark_mode = st.toggle("🌙 Dark Mode")
if dark_mode:
    st.markdown("""
        <style>
            html, body, [class*="css"] {
                background-color: #0e1117 !important;
                color: white !important;
            }
        </style>
    """, unsafe_allow_html=True)

# Languages
langs = list(LANGUAGES.values())
lang_codes = list(LANGUAGES.keys())
lang_map = dict(zip(langs, lang_codes))

# Auto-detect or manual source?
auto_detect = st.toggle("🧠 Auto-Detect Input Language", value=True)

if not auto_detect:
    from_lang = st.selectbox("🎧 Speak in", langs, index=langs.index("english"))
else:
    from_lang = 'auto'

to_lang = st.selectbox("🎯 Translate to", langs, index=langs.index("french"))

# Start Button
if st.button("🎤 Start Recording"):
    with sr.Microphone() as source:
        st.info("🎙 Listening... Speak clearly!")
        try:
            audio = recognizer.listen(source, timeout=5)
            raw_text = recognizer.recognize_google(audio)
            st.success(f"🗣 You said: {raw_text}")

            translated = translator.translate(raw_text, src=from_lang, dest=lang_map[to_lang])
            st.success(f"🌐 Translation ({to_lang}): {translated.text}")

            tts = gTTS(translated.text, lang=lang_map[to_lang])
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
                tts.save(tmpfile.name)
                audio_file = open(tmpfile.name, "rb")
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format="audio/mp3")

        except sr.WaitTimeoutError:
            st.warning("⏰ You didn’t speak in time.")
        except sr.UnknownValueError:
            st.error("🙉 Couldn’t understand your voice.")
        except Exception as e:
            st.error(f"❌ Something went wrong: {e}")
