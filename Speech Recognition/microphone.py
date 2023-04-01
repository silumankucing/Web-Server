import speech_recognition as sr
r = sr.Recognizer()

with sr.Microphone() as source:
    print('Say something into the microphone')
    audio = r.listen(source)