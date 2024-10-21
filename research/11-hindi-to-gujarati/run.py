from gtts import gTTS
import speech_recognition as sr
from googletrans import Translator
import playsound
import os

translator = Translator()

def translator_fun(text):
    return translator.translate(text, src='hi', dest='gu')

def text_to_voice(text_data):
    myobj = gTTS(text=text_data, lang='gu', slow=False)
    myobj.save("cache_file.mp3")
    playsound.playsound("cache_file.mp3")
    os.remove("cache_file.mp3")

while True:
    rec = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        rec.pause_threshold = 1
        audio = rec.listen(source, phrase_time_limit=10)
    try:
        print("Processing...")
        spoken_text = rec.recognize_google(audio, language='hi')
        
        print("Translating...")
        gujarati_version = translator_fun(spoken_text)

        print("Text to Speech...")
        text_to_voice(gujarati_version.text)
   
    except sr.UnknownValueError:
        print("Could not understand the audio")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
