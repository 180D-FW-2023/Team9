import time
import torch
import cv2
from transformers import YolosImageProcessor, YolosForObjectDetection
from PIL import Image
from picamera2 import Picamera2
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging    
import time
import traceback
from waveshare_OLED import OLED_1in51
from PIL import Image,ImageDraw,ImageFont
logging.basicConfig(level=logging.DEBUG)


picam2 = Picamera2()
picam2.start()
# Load the pre-trained YOLOS model
model = YolosForObjectDetection.from_pretrained('hustvl/yolos-tiny')
image_processor = YolosImageProcessor.from_pretrained("hustvl/yolos-tiny")


# Define the object class you want to detect
objclass = 'cell phone'
try:
    disp = OLED_1in51.OLED_1in51()
    disp.Init()
    disp.clear()
    image1 = Image.new('1', (disp.width, disp.height), "WHITE")
    font1 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
    draw = ImageDraw.Draw(image1)
    while objclass != None:
        image1 = Image.new('1', (disp.width, disp.height), "WHITE")
        draw = ImageDraw.Draw(image1)
        frame = picam2.capture_array()
        #cv2.rectangle(frame, (0,0), (640,480), (0, 255, 0), 2)
        
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
                #cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 255, 0), 2)
                #cv2.putText(frame, f"{class_name} {round(score.item(), 2)}", (int(box[0]), int(box[1]) - 10),
                #            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                lengthy = box[3] - box[1]
                lengthx = box[2] - box[0]
                mx = box[2] - lengthx
                my = box[3] - lengthy
                print(mx,my)
                if (my > 230 and my < 250 and mx < 334 and mx > 306):
                    #Middle
                    
                    draw.line([(0,0),(127,0)], fill = 0)
                    draw.line([(0,0),(0,63)], fill = 0)
                    draw.line([(127,0),(127,63)], fill = 0)
                    draw.line([(0,63),(127,63)], fill = 0)
                   # print(1)
                elif (my > 0 and my <= 160 and mx > 0 and mx <= 306):
                    #Top Right
                    draw.line([(106,0),(127,0)], fill = 0)
                    draw.line([(127,0),(127,21)], fill = 0)
                    #print(2)
                elif (my > 160 and my <= 320 and mx > 0 and mx <= 306):
                    #Middle Right
                    draw.line([(127,22),(127,43)], fill = 0)
                    #print(3)
                elif (my > 320 and my <= 480 and mx > 0 and mx <= 306):
                    #Bottom Right
                    draw.line([(127,44),(127,63)], fill = 0)
                    draw.line([(106,63),(127,63)], fill = 0)
                   # print(4)
                elif (my > 0 and my <= 230 and mx > 306 and mx < 334):
                    #Top Middle
                    draw.line([(54,0),(74,0)], fill = 0)
                   # print(5)
                elif (my >= 250 and my <= 480 and mx > 306 and mx < 334):
                    #Bottom Middle
                    draw.line([(54,63),(74,63)], fill = 0)
                    #print(6)
                elif (my > 0 and my <= 160 and mx >= 334 and mx <= 640):
                    #Top Left
                    draw.line([(0,0),(21,0)], fill = 0)
                    draw.line([(0,0),(0,21)], fill = 0)
                   # print(7)
                elif (my > 160 and my <= 320 and mx >= 334 and mx <= 640):
                    #Middle Left
                    draw.line([(0,22),(0,43)], fill = 0)
                    #print(8)
                elif (my > 320 and my <= 480 and mx >= 334 and mx <= 640):
                    #Bottom Left
                    draw.line([(0,43),(0,63)], fill = 0)
                    draw.line([(0,63),(21,63)], fill = 0)
                    #print(9)
                image1 = image1.rotate(180) 
                disp.ShowImage(disp.getbuffer(image1))
                time.sleep(2)
                disp.clear()
                
            #cv2.imshow('Object Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
                break
except IOError as e:
    logging.info(e)
    picam2.close()
    #cv2.destroyAllWindows()
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    disp.module_exit()
    picam2.close()
    #cv2.destroyAllWindows()
    exit()
        
            
picam2.close()
#cv2.destroyAllWindows()
