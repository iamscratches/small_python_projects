import os
import time
import playsound
import pyaudio
from gtts import gTTS
import speech_recognition as sr
import random


voice = 0
def speak(text):
    tts = gTTS(text = text, lang = "en-in")
    global voice
    print(voice)
    filename = str(voice )+ ".mp3"
    voice = voice +1
    tts.save(filename)
    playsound.playsound(filename)

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print("Exception: " + str(e))
    return said
#speak("Hey!! i'm scratches, nice to meet you")
print('listening...')
#speak(get_audio())

while(True):
    text =get_audio()
    if "hello" in text:
        speak("hello, how are u?")
    elif "your name" in text:
        speak("My name is Scratches")
    elif "bye bye" in text:
        speak("ok! bye bye!, nice to meet you")
        break
print("over")































              
