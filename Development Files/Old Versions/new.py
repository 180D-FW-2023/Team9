import os
import openai
import time
import speech_recognition as sr
import pyttsx3
import serial
import tweepy
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import geocoder
import cv2
import torch
from transformers import YolosImageProcessor, YolosForObjectDetection
from PIL import Image

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

model = YolosForObjectDetection.from_pretrained('hustvl/yolos-tiny')
image_processor = YolosImageProcessor.from_pretrained("hustvl/yolos-tiny")
objclass = ''

consumer_key = 'u6QyY8KUBGtxQoL0dddghrso9'
consumer_secret = 'HCLFXxqe3iS8qySLyNNPWS8Jg9cqt9WV947RKWySvsC8h2fqQN'
access_token = '1752849859114311680-tyJ3QZ6XztjtDO4f5vYhTbxQnPyWpx'
access_token_secret = 'oyFTNIL0wNyLvyVIwHB3slkDXSEgDjPPFmzbfOisGbcpw'



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
    global objclass
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
                engine.say("Camera Activated Say Object")
                engine.runAndWait()
                while True:
                    print(1)
                    audio = r.listen(source)
                    print(2)
                    try:
                        print(3)
                        text = r.recognize_google(audio)
                        print(4)
                        engine.say("Looking for" + text)
                        objclass = text
                        start = time.time()
                        camera_time(start)
                        break
                    except sr.UnknownValueError:
                        pass
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
    
    #Below Here is OG Code
    #g = geocoder.ip('me')
    #str1 = g.city
    #str2 = g.postal
    #str3 = "You are in " + str1 + " and the zipcode is " + str2
    #print(g.latlng)
    #print(g.city)
    #print(g.postal)
    #engine.say(str3)
    #engine.runAndWait()
    #menu_triggered(source)
    gps_serial = serial.Serial('/dev/ttyUSB0', baudrate = 9600, timeout = 1)

    geolocator = Nominatim(user_agent = "gps_example")

    try:
        while True:
            gps_data = gps_serial.readline().decode('utf-8', errors='ignore').strip()
		
            if 'GPGGA' in gps_data or 'GNGGA' in gps_data:
			
                fields = gps_data.split(',')
                
                if fields[2][:2] == '':
                    print("No connection")
                    engine.say("No Connection")
                    engine.runAndWait()
                    break
			
                latitude = float(fields[2][:2]) + float(fields[2][2:]) / 60.0
                longitude = float(fields[4][:3]) + float(fields[4][3:]) / 60.0
                longitude = -longitude
			
                if -90 <= latitude <= 90 and -180 <= longitude <= 180:
				
                    location = geolocator.reverse((latitude, longitude), language = 'en')
				
                    address = location.address
                    city = location.raw.get('address', {}).get('city', 'N/A')
				
                    #print(f"Latitude: {latitude}, Longitude: {longitude}")
                    print(f"Address: {address}")
                    print(f"City: {city}")
                    engine.say(address)
                    engine.runAndWait()
                    break
    except KeyboardInterrupt:
        print("Program terminated by Jarbisss")
	
    finally:
        gps_serial.close()
				
                    #time.sleep(5)
                #print(f"GPS Data: {gps_data}")

def camera_time(start):
  
    picam2.start()
    time.sleep(10)

    while objclass != None:
        print(objclass)
        frame = picam2.capture_array()
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_frame)
        inputs = image_processor(images=pil_image, return_tensors="pt")
        outputs = model(**inputs)
        target_sizes = torch.tensor([pil_image.size[::-1]])
        results = image_processor.post_process_object_detection(outputs, threshold=0.5, target_sizes=target_sizes)[0]
        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            box = [round(i, 2) for i in box.tolist()]
            class_name = model.config.id2label[label.item()]
            if class_name.lower() == objclass and score.item() > 0.5:  # Adjust threshold as needed
                cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 255, 0), 2)
                cv2.putText(frame, f"{class_name} {round(score.item(), 2)}", (int(box[0]), int(box[1]) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow('Object Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    print("3")
    # Release the capture
    client.loop_stop()
    client.disconnect()

    cap.release()
    cv2.destroyAllWindows()
    
    
    menu_triggered(source)
# Use the default microphone as the audio source
with sr.Microphone() as source:
    while True:
        initial(source)
