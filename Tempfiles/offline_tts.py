import pyttsx3
import time
#engine.runAndWait()


def offline_speak(str):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 150)
    engine.say(str)
    engine.runAndWait()
