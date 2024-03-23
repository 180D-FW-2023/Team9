import cv2
import numpy as np

# Load MobileNet SSD model and configuration
net = cv2.dnn.readNetFromCaffe('mobilenet_ssd.prototxt', 'mobilenet_ssd.caffemodel')

# Set your video capture device (0 for default camera)
cap = cv2.VideoCapture(0)

# Set the threshold size for triggering the message (you may need to adjust this based on your setup)
threshold_size = 44000  # Example value, adjust as needed

def calculate_size(x, y, x_max, y_max):
    return (x_max - x) * (y_max - y)

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
        if confidence > 0.2:  # Adjust confidence threshold based on your requirements
            class_id = int(detections[0, 0, i, 1])

            if class_id == 7:  # Assuming class_id 7 corresponds to 'car'
                box = detections[0, 0, i, 3:7] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
                x, y, x_max, y_max = box.astype('int')

                # Calculate the size of the bounding box
                box_size = calculate_size(x, y, x_max, y_max)

                # Check if the car size has passed the threshold
                if box_size > threshold_size:
                    #cv2.putText(frame, "Car Too Close!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    print("pina colada")
                # Draw bounding box
                #cv2.rectangle(frame, (x, y), (x_max, y_max), (0, 255, 0), 2)

    #cv2.imshow('Object Detection', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object
#cap.release()
#cv2.destroyAllWindows()
