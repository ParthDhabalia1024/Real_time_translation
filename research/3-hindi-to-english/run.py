from gtts import gTTS
import speech_recognition as sr
from googletrans import Translator
import playsound
import os

# Initialize the Translator
translator = Translator()

# Function to translate from Hindi to English
def translator_fun(text):
    return translator.translate(text, src='hi', dest='en')

# Function to convert text to speech and play it
def text_to_voice(text_data):
    myobj = gTTS(text=text_data, lang='en', slow=False)
    myobj.save("cache_file.mp3")
    playsound.playsound("cache_file.mp3")
    os.remove("cache_file.mp3")  # Remove the file after playing

# Main loop to continuously listen, translate, and speak
while True:
    rec = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        rec.pause_threshold = 1  # Adjust for a slight pause before stopping
        audio = rec.listen(source, phrase_time_limit=10)  # Limit the listening to 10 seconds

    try:
        print("Processing...")
        # Recognize the spoken text (assumed to be in Hindi)
        spoken_text = rec.recognize_google(audio, language='hi')
        print(f"Recognized (Hindi): {spoken_text}")

        # Translate the recognized text to English
        print("Translating to English...")
        translated_text = translator_fun(spoken_text)
        print(f"Translation (English): {translated_text.text}")

        # Convert the translated English text to speech
        print("Converting text to speech...")
        text_to_voice(translated_text.text)

    except sr.UnknownValueError:
        print("Could not understand the audio")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
