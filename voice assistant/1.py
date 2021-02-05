import os
import time
import playsound
import pyaudio
from gtts import gTTS

def speak(text):
    tts = gTTS(text = text, lang = "en-in")
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)

#speak("Hey!! i'm scratches! मेँ आपको चोदना चाहता हूँ")
#speak("aap kaise hai")
speak("Hey!! i'm scratches, nice to meet you")
