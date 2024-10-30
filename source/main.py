import os
import time
import pygame
from gtts import gTTS
import streamlit as st
import speech_recognition as sr
from googletrans import LANGUAGES, Translator

# Initialize global variables
isTranslateOn = False

translator = Translator()  # Initialize the translator module.
pygame.mixer.init()  # Initialize the mixer module.

# Create a mapping between language names and language codes
language_mapping = {name: code for code, name in LANGUAGES.items()}

def get_language_code(language_name):
    """Get the language code from the language name."""
    return language_mapping.get(language_name, language_name)

def translator_function(spoken_text, from_language, to_language):
    """Translate spoken text from one language to another."""
    try:
        translation = translator.translate(spoken_text, src=from_language, dest=to_language)
        if translation is None or translation.text is None:
            raise ValueError("Translation returned None.")
        return translation
    except Exception as e:
        print(f"Error in translation: {e}")
        return None

def text_to_voice(text_data, to_language):
    """Convert text to speech using gTTS."""
    myobj = gTTS(text=text_data, lang=to_language, slow=False)
    myobj.save("cache_file.mp3")
    audio = pygame.mixer.Sound("cache_file.mp3")  # Load a sound.
    audio.play()
    os.remove("cache_file.mp3")  # Remove the audio file after playing.

def main_process(output_placeholder, from_language, to_language):
    """Main process for continuous speech recognition and translation."""
    global isTranslateOn
    
    while isTranslateOn:
        rec = sr.Recognizer()
        with sr.Microphone() as source:
            output_placeholder.text("Listening...")
            rec.pause_threshold = 1
            audio = rec.listen(source, phrase_time_limit=10)
        
        try:
            output_placeholder.text("Processing...")
            spoken_text = rec.recognize_google(audio, language=from_language)
            
            if spoken_text:  # Check if spoken_text is not None
                output_placeholder.text("Translating...")
                translated_text = translator_function(spoken_text, from_language, to_language)

                if translated_text:
                    text_to_voice(translated_text.text, to_language)
                else:
                    output_placeholder.text("Translation failed.")
            else:
                output_placeholder.text("Could not understand audio.")
        
        except sr.UnknownValueError:
            output_placeholder.text("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            output_placeholder.text("Could not request results from Google Speech Recognition service; {0}".format(e))
        except Exception as e:
            print(e)
            output_placeholder.text("An error occurred: {}".format(e))

# Streamlit UI layout
st.title("Language Translator")
st.title("Hi Parth ...what would you like to translate today..? ")

# Dropdowns for selecting languages
from_language_name = st.selectbox("Select Source Language:", list(LANGUAGES.values()))
to_language_name = st.selectbox("Select Target Language:", list(LANGUAGES.values()))

# Convert language names to language codes
from_language = get_language_code(from_language_name)
to_language = get_language_code(to_language_name)

# Buttons to control the translation process
start_button = st.button("Start")
stop_button = st.button("Stop")

# Check if "Start" button is clicked
if start_button:
    if not isTranslateOn:
        isTranslateOn = True
        output_placeholder = st.empty()
        main_process(output_placeholder, from_language, to_language)

# Check if "Stop" button is clicked
if stop_button:
    isTranslateOn = False


# # Console interface to select languages and start/stop translation
# if __name__ == "__main__":

#     # Select source language
#     print("Available languages: ")
#     for name in LANGUAGES.values():
#         print(name, end=", ")
#     print("\n")

#     from_language_name = input("Select source language: ")
#     to_language_name = input("Select target language: ")

#     # Convert language names to language codes
#     from_language = get_language_code(from_language_name)
#     to_language = get_language_code(to_language_name)

#     # Main process loop
#     while True:
#         user_input = input("Type 'start' to begin translation or 'stop' to exit: ").lower()
#         if user_input == "start":
#             isTranslateOn = True
#             main_process(from_language, to_language)
#         elif user_input == "stop":
#             isTranslateOn = False
#             print("Translation stopped.")
#             break
#         else:
#             print("Invalid command, please type 'start' or 'stop'.")





