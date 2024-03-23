import time
import torch
import cv2
from transformers import YolosImageProcessor, YolosForObjectDetection
from PIL import Image
from picamera2 import Picamera2


picam2 = Picamera2()
picam2.start()
# Load the pre-trained YOLOS model
model = YolosForObjectDetection.from_pretrained('hustvl/yolos-tiny')
image_processor = YolosImageProcessor.from_pretrained("hustvl/yolos-tiny")


# Define the object class you want to detect
objclass = 'person'

while objclass != None:
	
	frame = picam2.capture_array()
	cv2.rectangle(frame, (0,0), (10,10), (0, 255, 0), 2)
	cv2.rectangle(frame, (0,0), (640,480), (0, 255, 0), 2)
	'''
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
			y = box[3] - box[1]
			x = box[2] - bo
			cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 255, 0), 2)
			print(f"({box[0]}, {box[1]}, {box[2]}, {box[3]})")
   
	'''
	cv2.imshow('Object Detection', frame)
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
picam2.close()
cv2.destroyAllWindows()
