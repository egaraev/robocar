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
import subprocess, signal

camera = ["python", "VideoStream.py"]
regular_camera = subprocess.Popen(camera)


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



def start_face_tracking_subprocess():
    # start the subprocess
    subprocess_args = ["python", "FaceTrackingFunction.py"]
    face_tracking_obj = subprocess.Popen(subprocess_args)
    return face_tracking_obj


def start_obstacle_avoid_subprocess():
    # start the subprocess
    subprocess_args = ["python", "ObstacleAvoidanceFunction.py"]
    obstacle_avoidance_obj = subprocess.Popen(subprocess_args)
    return obstacle_avoidance_obj


def start_line_follow_subprocess():
    # start the subprocess
    subprocess_args = ["python", "LineFollowFunction.py"]
    line_follow_obj = subprocess.Popen(subprocess_args)
    return line_follow_obj


def start_lane_follow_subprocess():
    # start the subprocess
    subprocess_args = ["python", "LaneFollowFunction.py"]
    lane_follow_obj = subprocess.Popen(subprocess_args)
    return lane_follow_obj


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

    # 7: Line following
    if there_exists(["enable line", "line follow"]):
        speak("Enabling line follow")
        return 'line_on'

    if there_exists(["disable line", "line unfollow"]):
        speak("Disabling line follow")
        return 'line_off'

    # 8: Lane following
    if there_exists(["enable lane", "lane follow"]):
        speak("Enabling lane follow")
        return 'lane_on'

    if there_exists(["disable lane", "lane unfollow"]):
        speak("Disabling lane follow")
        return 'lane_off'

    # 9: Obstacle Avoidance
    if there_exists(["enable ultrasonic", "ultrasonic on"]):
        speak("Enabling ultrasonic")
        return 'ultrasonic_on'

    if there_exists(["disable ultrasonic", "ultrasonic unfollow"]):
        speak("Disabling ultrasonic")
        return 'ultrasonic_off'

    # 10: Face tracking
    if there_exists(["face", "face tracking"]):
        speak("Face tracking")
        return "face_on"

    if there_exists(["no tracking"]):
        speak("Stopping Face tracking")
        return "face_off"

    # 11: wait
    if there_exists(["wait", "hold on"]):
        speak("waiting")
        time.sleep(60)

    # 12: finish
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
    if message == "face_on":
        regular_camera.terminate()
        face_track = start_face_tracking_subprocess()
    elif message == "face_off":
        face_track.send_signal(signal.SIGTERM)
    elif message == "line_on":
        regular_camera.terminate()
        line_follow = start_line_follow_subprocess()
    elif message == "line_off":
        line_follow.send_signal(signal.SIGTERM)
    elif message == "ultrasonic_on":
        regular_camera.terminate()
        obstacle_avoid = start_obstacle_avoid_subprocess()
    elif message == "ultrasonic_off":
        obstacle_avoid.send_signal(signal.SIGTERM)
    elif message == "lane_on":
        regular_camera.terminate()
        lane_follow = start_lane_follow_subprocess()
    elif message == "lane_off":
        lane_follow.send_signal(signal.SIGTERM)
    else:
        client.publish("pibot/move", str(message), qos=1)