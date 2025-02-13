import os
import pygame
from gtts import gTTS
import streamlit as st
import speech_recognition as sr
from googletrans import LANGUAGES, Translator

# Initialize
translator = Translator()
pygame.mixer.init()
isTranslateOn = False

# Language mapping
language_mapping = {name: code for code, name in LANGUAGES.items()}

def get_language_code(language_name):
    return language_mapping.get(language_name, language_name)

def translator_function(text, from_language, to_language):
    return translator.translate(text, src=from_language, dest=to_language).text

def text_to_voice(text_data, to_language):
    myobj = gTTS(text=text_data, lang=to_language, slow=False)
    myobj.save("cache_file.mp3")
    audio = pygame.mixer.Sound("cache_file.mp3")  
    audio.play()
    os.remove("cache_file.mp3")

def main_process(output_placeholder, from_language, to_language):
    global isTranslateOn
    rec = sr.Recognizer()

    while isTranslateOn:
        with sr.Microphone() as source:
            output_placeholder.markdown("🎤 **Listening...**", unsafe_allow_html=True)
            rec.pause_threshold = 1
            audio = rec.listen(source, phrase_time_limit=10)

        try:
            output_placeholder.markdown("⏳ **Processing...**", unsafe_allow_html=True)
            spoken_text = rec.recognize_google(audio, language=from_language)
            
            output_placeholder.markdown(f"🗣 **Detected:** `{spoken_text}`", unsafe_allow_html=True)
            translated_text = translator_function(spoken_text, from_language, to_language)

            output_placeholder.markdown(f"🌍 **Translated:** `{translated_text}`", unsafe_allow_html=True)
            text_to_voice(translated_text, to_language)

        except Exception as e:
            output_placeholder.error(f"⚠️ Error: {e}")

# Streamlit UI
st.set_page_config(page_title="Real-Time Translator", page_icon="🌍", layout="wide")

st.sidebar.title("🌐 Language Settings")
from_language_name = st.sidebar.selectbox("Select Source Language:", list(LANGUAGES.values()))
to_language_name = st.sidebar.selectbox("Select Target Language:", list(LANGUAGES.values()))

from_language = get_language_code(from_language_name)
to_language = get_language_code(to_language_name)

st.title("🗣️ Real-Time Language Translator")

# Voice Translation Section
st.subheader("🎤 Voice Translation")
col1, col2 = st.columns(2)

with col1:
    start_button = st.button("▶️ Start Listening", use_container_width=True)

with col2:
    stop_button = st.button("⏹ Stop Listening", use_container_width=True)

output_placeholder = st.empty()

if start_button:
    if not isTranslateOn:
        isTranslateOn = True
        main_process(output_placeholder, from_language, to_language)

if stop_button:
    isTranslateOn = False

# Text Translation Section
st.subheader("📝 Text Translation")
text_input = st.text_area("Type text to translate:")
translate_button = st.button("🔄 Translate Text")

if translate_button and text_input:
    translated_text = translator_function(text_input, from_language, to_language)
    st.markdown(f"✅ **Translated:** `{translated_text}`", unsafe_allow_html=True)
    text_to_voice(translated_text, to_language)
