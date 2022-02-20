import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)
engine.runAndWait()

def offline_speak(str):
    engine.say(str)
    engine.runAndWait()