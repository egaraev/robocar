import speech_recognition as sr # recognise speech
import playsound # to play an audio file
from gtts import gTTS # google text to speech
import time
import random
import os  # to remove created audio files


def there_exists(terms):
    for term in terms:
        if term in voice_data:
            return True


def listen(ask=False):
    r = sr.Recognizer()  # initialise a recogniser
    # listen for audio and convert it to text:
    with sr.Microphone() as source: # microphone as source
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        if ask:
            speak(ask)
        print("Listening...")
        audio = r.listen(source)  # listen for the audio via source
        voice_data = ''
        try:
            print("Recognizing...")
            voice_data = r.recognize_google(audio)  # convert audio to text
        except sr.UnknownValueError: # error: recognizer does not understand
            speak('I did not get that')
        except sr.RequestError:
            speak('Sorry, the service is down') # error: recognizer is not connected
        print(f">> {voice_data.lower()}") # print what user said
        return voice_data.lower()


# get string and make a audio file to be played
def speak(audio_string):
    tts = gTTS(text=audio_string, lang='en') # text to speech(voice)
    r = random.randint(1,20000000)
    audio_file = 'audio' + str(r) + '.mp3'
    tts.save(audio_file) # save as mp3
    playsound.playsound(audio_file) # play the audio file
    print(f"Android: {audio_string}") # print what app said
    os.remove(audio_file) # remove audio file


def respond():
    # 1: greeting
    if there_exists(['android']):
        greetings = ["hey, how can I help you boss", "hey, what's up? boss", "I'm listening boss", "how can I help you? boss", "hello boss"]
        greet = greetings[random.randint(0, len(greetings)-1)]
        speak(greet)

    # 2: forward
    if there_exists(["forward", "go forward"]):
        speak("Going forward")

    # 3: backward
    if there_exists(["backward", "go backward", "go back", "back"]):
        speak("Going backward")

    # 4: left
    if there_exists(["left", "go left", "turn left"]):
        speak("Turning left")

    # 5: right
    if there_exists(["right", "go right", "turn right"]):
        speak("Turning right")


    # 6: finish
    if there_exists(["exit", "quit", "goodbye"]):
        speak("going offline")
        exit()


time.sleep(1)

while True:
    voice_data = listen() # get the voice input
    respond() # respond

