import cv2
import os

# Load pre-trained Haar cascade classifier for eye detection
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Initialize camera
camera = cv2.VideoCapture(0)

# Check if the camera is opened successfully
if not camera.isOpened():
    print("Error: Could not open camera.")
    exit()

counter = 0

# Create a folder to save the captured images
output_dir = 'captured_images'
os.makedirs(output_dir, exist_ok=True)

while counter < 50:

    # Capture frame-by-frame
    ret, frame = camera.read()

    # Convert the frame to grayscale for eye detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect eyes in the frame
    eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Crop and save each eye
    for (x, y, w, h) in eyes:
        # Draw rectangle around the eye
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        # Crop the eye region
        eye_crop = frame[y:y+h, x:x+w]

        # Save the cropped eye
        cv2.imwrite(f'{output_dir}/eye_{counter}.jpg', eye_crop)

    # Save the captured frame
    cv2.imwrite(f'{output_dir}/frame_{counter}.jpg', frame)

    # Display the captured frame
    cv2.imshow('Original', frame)

    # Increment the counter
    counter += 1

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
camera.release()
cv2.destroyAllWindows()
print(f'{counter} photos captured and saved in {output_dir}.')
