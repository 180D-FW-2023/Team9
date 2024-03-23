import os
import openai
import time
import speech_recognition as sr
import pyttsx3
import serial
import smtplib
import tweepy
import numpy as np
from geopy.geocoders import Nominatim
import geocoder
import cv2
import sys
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
import logging 
from waveshare_OLED import OLED_1in51
from PIL import Image,ImageDraw,ImageFont
logging.basicConfig(level=logging.DEBUG)
import pygame
import threading
import config



openai.api_key = config.open_api_key
os.environ['OPENAI_API_KEY'] = openai.api_key
model = 'gpt-3.5-turbo'
global reset
reset = False
r = sr.Recognizer()
r.energy_threshold = 950
engine = pyttsx3.init()
voice = engine.getProperty('voices')[1]
engine.setProperty('voice', 'english')
#Thread Setup

# Thread-safe event object to control execution of the object detection thread
object_detection_event = threading.Event()
object_detection_event.set()  # Set the event to initially allow execution



# Twitter API
consumer_key = config.twitter_consumer_key
consumer_secret = config.twitter_consumer_secret
access_token = config.twitter_access_token
access_token_secret = config.twitter_access_token_secret
client = tweepy.Client(
    consumer_key=consumer_key, consumer_secret=consumer_secret,
    access_token=access_token, access_token_secret=access_token_secret
)

# Ding Sounds
def play_ding_sound():
    pygame.init()
    pygame.mixer.init()
    ding_sound = pygame.mixer.Sound("/home/pi/Desktop/chat/ding2.wav")  # Replace "/path/to/your/ding_sound.wav" with the actual path to your ding sound file
    ding_sound.play()
    while pygame.mixer.get_busy() == True:
        continue
    pygame.quit()


# Intro Wakeup
def initial(source): 
    print("Waiting for 'hey buddy' ")
    engine.say('Say hey buddy to enter the menu')
    engine.runAndWait()
    temp = time.time()
    while True:
        audio = r.listen(source)
        try:
            play_ding_sound()
            text = r.recognize_google(audio)
            print(text)
            if "hey buddy" in text.lower():
                print(time.time() - temp)
                print("Entering Menu")
                engine.say("Entering Menu")
                engine.runAndWait()
                menu_triggered(source)
                break
        except sr.UnknownValueError:
            pass
    
# Main Menu
def menu_triggered(source):
    global objclass
    print("Menu Now Listening... ")
    engine.say("Welcome to the menu")
    engine.runAndWait()
    while True:
        audio = r.listen(source)
        try:
            play_ding_sound()
            text = r.recognize_google(audio)
            time.sleep(1)
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
            elif "twitter" in text.lower():
                
                print("What would you like to Tweet")
                engine.say("What would you like to Tweet")
                engine.runAndWait()
                twitter(source)
                break
            elif "car detect on" in text.lower():
                print("Activating Rear-View Car Detection Camera")
                engine.say("Activating Car Detection")
                engine.runAndWait()
                behindOn(source)
                break
            elif "car detect off" in text.lower():
                print("Deactivating Rear-View Car Detection Camera")
                engine.say("Deactivating Car Detection")
                engine.runAndWait()
                behindOff(source)
                break
        except sr.UnknownValueError:
            pass

# Listen for input and respond with OpenAI API
def listen_and_respond(source):
    print("Listening...")
    weExit = 0

    while True:
        audio = r.listen(source)
        time.sleep(1)
        try:
            play_ding_sound()
            text = r.recognize_google(audio)
            time.sleep(1)
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

def twitter(source):
    print("Listening...")
    
    while True:
        audio = r.listen(source)
        time.sleep(1)
        try:
            play_ding_sound()
            text = r.recognize_google(audio)
            time.sleep(1)
            print(f"You said: {text} , would you like to tweet this? Say yes to tweet your message or no to cancel")
            engine.say(f"You said: {text} , would you like to tweet this? Say yes to tweet your message or no to cancel")
            engine.runAndWait()
            twitter_confirmation(source,text)
            break
            if not text:
                continue
            if not audio:
                menu_triggered(source)
        except sr.UnknownValueError:
            print('Silence Detected')
            pass
            
def twitter_confirmation(source,message):
    print("Listening...")
    
    while True:
        audio = r.listen(source)
        time.sleep(1)
        try:
            play_ding_sound()
            texttwo = r.recognize_google(audio)
            time.sleep(1)
            print(message)
            if "yes" in texttwo.lower():
                print("Tweeting your message")
                engine.say("Tweeting your message")
                engine.runAndWait()
                response = client.create_tweet(text=message)
                print("Message Tweeted")
                engine.say("Message Tweeted")
                engine.runAndWait()
                menu_triggered(source)
                break
            elif "no" in texttwo.lower():
                print("Tweet Cancelled, Returning to Menu")
                engine.say("Tweet Cancelled, Returning to Menu")
                engine.runAndWait()
                menu_triggered(source)
                break
            if not message:
                continue
            if not audio:
                menu_triggered(source)
        except sr.UnknownValueError:
            print('Silence Detected')
            pass

def back_up_location():
    g = geocoder.ip('me')
    str1 = g.city
    str2 = g.postal
    str3 = " " + str1
    print(g.latlng)
    print(g.city)
    print(g.postal)
    engine.say("You are around" + str3)
    engine.runAndWait()
    menu_triggered(source)

    
    
            
def get_current_location():

    gps_serial = serial.Serial('/dev/ttyUSB0', baudrate = 9600, timeout = 1)

    geolocator = Nominatim(user_agent = "gps_example")

    try:
        while True:
            gps_data = gps_serial.readline().decode('utf-8', errors='ignore').strip()
            print("ERROR")
            if 'GPGGA' in gps_data or 'GNGGA' in gps_data:
			
                fields = gps_data.split(',')
                
                if fields[2][:2] == '':
                    print("No connection Running backup wifi location")
                    engine.say("No connection Running backup wifi location")
                    engine.runAndWait()
                    back_up_location()
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
        print("Program terminated")
	
    finally:
        gps_serial.close()
        print("Program terminated by j")
				

def calculate_size(x, y, x_max, y_max):
    return (x_max - x) * (y_max - y)

def behindOn(source):
    global reset
    global object_detection_event
    object_detection_event.set()
    reset = True
    menu_triggered(source)

def display(mx,my):
    disp = OLED_1in51.OLED_1in51()
    disp.Init()
    disp.clear()
    image1 = Image.new('1', (disp.width, disp.height), "WHITE")
    font1 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
    draw = ImageDraw.Draw(image1)
    if (mx <= 150):
        draw.line([(127,0),(127,63)], fill = 0)
        print("left")
        
    else:
        draw.line([(0,0),(0,63)], fill = 0)
        print("right")

    image1 = image1.rotate(180) 
    disp.ShowImage(disp.getbuffer(image1))
    time.sleep(2)
    disp.clear()
    


def behindOff(source):
    global object_detection_event
    object_detection_event.clear()
    menu_triggered(source)


def send_message():

    
    CARRIER = "verizon"
    MESSAGE = "Your loved one Hamza had a car get too close to him and he may have been hit."



    EMAIL = "helmetbuddy7@gmail.com"
    PASSWORD = "tfdz xmzq tigr katv"

    CARRIERS = {
    "att": "@mms.att.net",
    "tmobile": "@tmomail.net",
    "verizon": "@vtext.com",
    "sprint": "@messaging.sprintpcs.com"
    }

    recipient = "5307151598@vtext.com"
    auth = (EMAIL, PASSWORD)
 
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(auth[0], auth[1])
 
    server.sendmail(auth[0], recipient, MESSAGE)


def calculate_size(x, y, x_max, y_max):
    return (x_max - x) * (y_max - y)

def behind():
    global reset
    print(reset)
    if object_detection_event.wait():
    # Load MobileNet SSD model and configuration
    # Set your video capture device (0 for default camera)
        net = cv2.dnn.readNetFromCaffe('mobilenet_ssd.prototxt', 'mobilenet_ssd.caffemodel')
        if reset:
            cap = cv2.VideoCapture(-1)

        # Set the threshold size for triggering the message
        threshold_size = 44000  
        emergency_size = 61000
        cur_time = time.time()
        prev_time = cur_time - 600

        while True:

            ret, frame = cap.read()
            if not ret:
                break
            # Convert the frame to a blob to pass through the network
            blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)
            
            # Set the blob as input to the network
            net.setInput(blob)

            # Obtain detections
            detections = net.forward()
            
            for i in range(detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > 0.2:  
                    class_id = int(detections[0, 0, i, 1])
                    
                    
                    if class_id == 7:
                        print("Detected")
                        
                        
                        box = detections[0, 0, i, 3:7] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
                        x, y, x_max, y_max = box.astype('int')

                        lengthy = y_max - y
                        lengthx = x_max - x
                        mx = x_max - lengthx
                        my = y_max - lengthy


                        # Calculate the size of the bounding box
                        box_size = calculate_size(x, y, x_max, y_max)
                        
                        # Check if the car size has passed the threshold
                        if (box_size > threshold_size) & (box_size < emergency_size):
                            print("car is close")
                            display(mx,my)
                            #play_ding_sound()
                            
                        if (box_size > threshold_size) & (box_size > emergency_size):
                            if (cur_time -  prev_time >= 600):
                                prev_time = cur_time
                                print("you might be dead")
                                send_message()
            cur_time = time.time()
    else:
        if reset:
            cap.release()
            reset = False
        pass
                    
'''
        #cv2.imshow('Object Detection', frame)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
 '''           
    #Release the video capture object
    #cv2.destroyAllWindows()

    
# Use the default microphone as the audio source
with sr.Microphone() as source:
    while True:
        #m#ain_thread = threading.Thread(target=initial(source))
        object_detection_thread = threading.Thread(target=behind)
        # Thread-safe event object to control execution of the object detection thread
        object_detection_thread.start()
        object_detection_event.clear()
        ##main_thread.start()
        initial(source)
