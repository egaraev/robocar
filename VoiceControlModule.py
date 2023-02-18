import speech_recognition as sr # recognise speech
import playsound # to play an audio file
from gtts import gTTS # google text to speech
import time
from time import sleep
import random
import os  # to remove created audio files
import requests
import pyttsx3
import paho.mqtt.client as mqtt
import sys
from vosk import Model, KaldiRecognizer
import pyaudio
model = Model('vosk-model')
recognizer = KaldiRecognizer(model, 16000)
cap = pyaudio.PyAudio()
stream = cap.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)



def check_internet():
    url = "http://www.google.com"
    timeout = 5
    try:
        request = requests.get(url, timeout=timeout)
        if request.status_code == 200:
            return 'online'
    except:
        pass
    return 'offline'


def there_exists(terms):
    for term in terms:
        if term in voice_data:
            return True


def recognize():
    if check_internet() == 'online':
        voice_data=listen()
    else:
        voice_data = offline_listen()
        print(f"Offline>> {voice_data.lower()}")  # print what user said
    return voice_data


def listen():
    speak("Listening to your order")
    r = sr.Recognizer()  # initialise a recogniser
    # listen for audio and convert it to text:
    with sr.Microphone() as source: # microphone as source

        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        print("Online Listening...")
        audio = r.listen(source)  # listen for the audio via source
        voice_data = ''

        try:
            print("Online Recognizing...")
            voice_data = r.recognize_google(audio)  # convert audio to text
        except sr.UnknownValueError: # error: recognizer does not understand
            speak('I did not get that')
        except sr.RequestError:
            speak('Sorry, the service is down') # error: recognizer is not connected
        print(f"Online>> {voice_data.lower()}") # print what user said
        return voice_data.lower()

def offline_speak(str):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 150)
    engine.say(str)
    time.sleep(1)
    engine.runAndWait()




def offline_listen():
    stream.start_stream()
    while True:
        voice_data=''
        data = stream.read(4096, exception_on_overflow = False)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            res = eval(result)
            voice_data = res['text']
        return voice_data



# get string and make a audio file to be played
def speak(audio_string):
    if check_internet() == 'online':
        tts = gTTS(text=audio_string, lang='en')  # text to speech(voice)
        r = random.randint(1,20000000)
        audio_file = 'audio' + str(r) + '.mp3'
        tts.save(audio_file) # save as mp3
        playsound.playsound(audio_file) # play the audio file
        print(f"Android: {audio_string}") # print what app said
        os.remove(audio_file) # remove audio file
    else:
        print ("We are offline")
        offline_speak(audio_string)
        print(f"Android: {audio_string}")  # print what app said


def respond():
    # 1: greeting
    if there_exists(['android']):
        greetings = ["hey, how can I help you boss", "hey, what's up? boss", "I'm listening boss", "how can I help you? boss", "hello boss"]
        greet = greetings[random.randint(0, len(greetings)-1)]
        speak(greet)

    # 2: forward
    if there_exists(["forward", "go forward"]):
        speak("Going forward")
        return "forward"


    # 3: backward
    if there_exists(["backward", "go backward", "go back", "back", "beck"]):
        speak("Going backward")
        return 'backward'


    # 4: left
    if there_exists(["left", "go left", "turn left"]):
        speak("Turning left")
        return 'left'


    # 5: right
    if there_exists(["right", "go right", "turn right"]):
        speak("Turning right")
        return 'right'


    # 6: stop
    if there_exists(["stop", "finish"]):
        speak("Stopping")
        return 'stop'

    # 7: line following
    if there_exists(["enable line", "line follow"]):
        speak("Enabling line follow")
        return 'line_on'

    if there_exists(["voice", "disable line", "line unfollow"]):
        speak("Disabling line follow")
        return 'line_off'


    # 8: finish
    if there_exists(["exit", "quit", "goodbye"]):
        speak("going offline")
        sys.exit()


time.sleep(1)

client = mqtt.Client()
client.connect("test.mosquitto.org", 1883, 60)


while True:
    voice_data = recognize() # get the voice input
    message = respond()
    print (message)
    if message=='line_on' or message=='line_off':
        client.publish("pibot/line", str(message), qos=1)
    else:
        client.publish("pibot/move", str(message), qos=1)