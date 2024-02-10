# Potrebno je unijeti sljedece komande u konzolu:
# pip install SpeechRecognition
# pip install pyaudio
# pip install pyttsx3

import speech_recognition as sr
import pyttsx3
import random as rd
import time as t
import wave
import numpy as np
import matplotlib.pyplot as plt


#Funkcija za speech recognition
def prepozGovor(recognizer,microphone,i):
    TRY=["none","first","second","third"]
    if not isinstance(recognizer,sr.Recognizer):
        raise TypeError("Instance 'recognizer' must be 'Recognizer' type")
    if not isinstance(microphone,sr.Microphone):
        raise TypeError("Instance 'microphone' must be 'Microphone' type")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio=recognizer.listen(source)
        with open(TRY[i+1]+"-guess-microphone-result.wav", "wb") as f:
            f.write(audio.get_wav_data())
            
    response={"success":True,"error":None,"transcription":None}
    
    try:
        response["transcription"]=recognizer.recognize_google(audio,language="en-US",show_all=False)
    except sr.RequestError:
        response["success"]=False
        response["error"]="API was unreachable"
    except sr.UnknownValueError:
        response["error"]="Unable to recognize speech"
        
    return response

#Funkcija za konvertovanje teksta u govor
def tekstUGovor(tekst):
    eng=pyttsx3.init()
    eng.setProperty('rate',160)
    eng.say(tekst)
    eng.runAndWait()
    
recognizer=sr.Recognizer()
microphone=sr.Microphone()

NUM_GUESS=3
PROMPT_LIM=5
TRY=["none","first","second","third"]
WORDS=["White","Yellow","Green","Blue","Orange","Black","Red","Purple","Gray","Brown"]
word=rd.choice(WORDS)
words=" ".join(WORDS)
print(words);
instructions="I'm thinking about one of these colors:{words}, You have 3 tries to guess which one".format(words=words)
tekstUGovor(instructions);
t.sleep(1);

for i in range(NUM_GUESS):
    for j in range(PROMPT_LIM):
        tekstUGovor("{num} guess. Speak!".format(num=TRY[i+1]))
        guess=prepozGovor(recognizer,microphone,i);
        if guess["transcription"]:
            break
        if guess["error"]=="Unable to recognize speech":
            tekstUGovor("I didn't quite catch that. What did you say?")
    if guess["error"]=="API was unreachable":
        tekstUGovor("ERROR, API not available for use")
        break;
    tekstUGovor("You said: {}".format(guess["transcription"]))
    s=wave.open(TRY[i+1]+"-guess-microphone-result.wav","r")
    signal=s.readframes(-1)
    signal=np.fromstring(signal,"int16")
    fs=s.getframerate()
    ti=np.linspace(0,len(signal)/fs,num=len(signal))
    plt.subplots_adjust(left=0.1,bottom=0.1,right=0.9,top=0.9,wspace=0.7,hspace=1.2)
    plt.subplot(3,1,i+1)
    plt.xlabel("Duzina signala")
    plt.ylabel("Frekvencija signala")
    plt.stem(ti,signal)
    plt.grid()
    if guess["transcription"]==word:
        tekstUGovor("Correct, you win")
        break;
    elif i<2:
        tekstUGovor("Incorrect, try again!")
    else:
        tekstUGovor("Sorry, you lose, i was thinking of the color {}".format(word))
    
    
