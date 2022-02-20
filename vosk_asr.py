from vosk import Model, KaldiRecognizer
import pyaudio
import time

model = Model('vosk-model')
recognizer = KaldiRecognizer(model, 16000)
cap = pyaudio.PyAudio()
stream = cap.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)

def vosk():
    stream.start_stream()
    while True:
        voice_data=''
        data = stream.read(4096)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            res = eval(result)
            voice_data = res['text']
            #print(voice_data)
            # if voice_data =='':
            #     exit()
        return voice_data



