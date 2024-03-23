import cv2
from transformers import YolosImageProcessor, YolosForObjectDetection
from PIL import Image
import torch

# Load YOLO model and image processor
model = YolosForObjectDetection.from_pretrained('hustvl/yolos-tiny')
image_processor = YolosImageProcessor.from_pretrained("hustvl/yolos-tiny")

# OpenCV setup for webcam
cap = cv2.VideoCapture(0)  # Use 0 for default webcam, change accordingly

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert OpenCV BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Convert to PIL Image
    pil_image = Image.fromarray(rgb_frame)

    # Perform object detection
    inputs = image_processor(images=pil_image, return_tensors="pt")
    outputs = model(**inputs)

    # Post-process the results
    target_sizes = torch.tensor([pil_image.size[::-1]])
    results = image_processor.post_process_object_detection(outputs, threshold=0.5, target_sizes=target_sizes)[0]

    # Draw bounding boxes for phones on the frame
    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        box = [round(i, 2) for i in box.tolist()]
        class_name = model.config.id2label[label.item()]

        # Filter for phones only
        if class_name.lower() == 'person' and score.item() > 0.5:  # Adjust threshold as needed
            cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 255, 0), 2)
            cv2.putText(frame, f"{class_name} {round(score.item(), 2)}", (int(box[0]), int(box[1]) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Object Detection', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture
cap.release()
cv2.destroyAllWindows()
