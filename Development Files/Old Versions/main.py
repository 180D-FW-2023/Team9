import os
import openai
import time
import speech_recognition as sr
import pyttsx3
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import geocoder

from picamera2 import Picamera2, Preview

# from os.path import join, dirname
# import matplotlib.pyplot as plt
# ^ matplotlib is great for visualising data and for testing purposes but usually not needed for production


openai.api_key = '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'
os.environ['OPENAI_API_KEY'] = openai.api_key
model = 'gpt-3.5-turbo'
# Set up the speech recognition and text-to-speech engines
r = sr.Recognizer()
engine = pyttsx3.init()
voice = engine.getProperty('voices')[1]
engine.setProperty('voice', 'english')
picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)



# Listen for the wake word "hey buddy"

def initial(source): 
    print("Waiting for 'hey buddy' ")
    engine.say('Say hey buddy to enter the menu')
    engine.runAndWait()
    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(text)
            if "hey buddy" in text.lower():
                print("Entering Menu")
                engine.say("Entering Menu")
                engine.runAndWait()
                menu_triggered(source)
                break
        except sr.UnknownValueError:
            pass
    

def menu_triggered(source):
    print("Menu Now Listening... ")
    engine.say("Welcome to the menu")
    engine.runAndWait()
    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(text)
            if "smart chat" in text.lower():
                print("Chat GPT Activated.")
                engine.say("Chat GPT Activated")
                engine.runAndWait()
                listen_and_respond(source)
                break
            elif "where am i" in text.lower():
                print("Finding Location")
                engine.say("Finding Location")
                engine.runAndWait()
                get_current_location()
                break
            elif "help" in text.lower():
                print("Option 1, say smart chat to trigger ChatGPT. Option 2, say where am i to find your approximate location. Option 3, say quit to exit the menu")
                engine.say("Option 1, say smart chat to trigger ChatGPT. Option 2, say where am i to find your approximate location. Option 3, say quit to exit the menu")
                engine.runAndWait()
                menu_triggered(source)
                break
            elif "quit" in text.lower():
                engine.say("Exiting Menu")
                engine.runAndWait()
                break
            elif "camera" in text.lower():
                print("Camera Activated")
                engine.say("Camera Activated")
                engine.runAndWait()
                start = time.time()
                camera_time(start)
                break
        except sr.UnknownValueError:
            pass

# Listen for input and respond with OpenAI API
def listen_and_respond(source):
    print("Listening...")
    weExit = 0

    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            if not text:
                continue

            # Send input to OpenAI API
            response = openai.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"{text}"}]) 
            response_text = response.choices[0].message.content
            print(f"OpenAI response: {response_text}")

            # Speak the response
            engine.say(response_text)
            engine.runAndWait()
            weExit = 1
            menu_triggered(source)

            if not audio:
                menu_triggered(source)
        except sr.UnknownValueError:
            print('Silence Detected')
            pass

        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            engine.say(f"Could not request results; {e}")
            engine.runAndWait()
            menu_triggered(source)
            break
        if weExit:
            break

def get_current_location():
    #geolocator = Nominatim(user_agent="my_location_app")
    #location = geolocator.geocode('')
    #print(location)
    #print(f"Your current location is: {location.address}")
    #print(f"Latitude: {location.latitude}, Longitude: {location.longitude}")
    #engine.say(location.address)
    g = geocoder.ip('me')
    str1 = g.city
    str2 = g.postal
    str3 = "You are in " + str1 + " and the zipcode is " + str2
    print(g.latlng)
    print(g.city)
    print(g.postal)
    engine.say(str3)
    engine.runAndWait()
    menu_triggered(source)

def camera_time(start):
    picam2.start_preview(Preview.QTGL)
    picam2.start()
    time.sleep(10)
    picam2.stop_preview()
    menu_triggered(source)
    
# Use the default microphone as the audio source
with sr.Microphone() as source:
    while True:
        initial(source)
