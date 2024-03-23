import time
import torch
import cv2
from transformers import YolosImageProcessor, YolosForObjectDetection
from PIL import Image
from picamera2 import Picamera2

# Initialize the camera
picam2 = Picamera2()
picam2.start()

# Load the pre-trained YOLOS model
model = YolosForObjectDetection.from_pretrained('hustvl/yolos-tiny')
image_processor = YolosImageProcessor.from_pretrained("hustvl/yolos-tiny")

# Define the object class you want to detect
objclass = 'cell phone'

while True:
    # Capture a frame from the camera
    frame = picam2.capture_array()
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(rgb_frame)

    # Perform object detection
    inputs = image_processor(images=pil_image, return_tensors="pt")
    outputs = model(**inputs)
    target_sizes = torch.tensor([pil_image.size[::-1]])
    results = image_processor.post_process_object_detection(outputs, threshold=0.5, target_sizes=target_sizes)[0]

    # Print the four points of the bounding box for each detected object
    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        box = [round(i, 2) for i in box.tolist()]
        class_name = model.config.id2label[label.item()]
        if class_name.lower() == objclass and score.item() > 0.5:  
            # Print the four points of the bounding box
            print(f"Top left: ({box[0]}, {box[1]})")
            print(f"Top right: ({box[2]}, {box[1]})")
            print(f"Bottom right: ({box[2]}, {box[3]})")
            print(f"Bottom left: ({box[0]}, {box[3]})")
    
    # Wait for a key press to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera resources
picam2.close()
