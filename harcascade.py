import cv2
import os

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Error: Could not open camera.")
    exit()

output_dir = 'captured_images'
os.makedirs(output_dir, exist_ok=True)

counter = 0

while counter < 50:

    ret, frame = camera.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:

        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        face_crop = frame[y:y+h, x:x+w]

        output_path = os.path.join(output_dir, f'face_{counter}.jpg')
        cv2.imwrite(output_path, face_crop)

        counter += 1
        if counter >= 50:
            break

    cv2.imshow('Capturing Faces', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()

print(f'{counter} photos captured and saved in {output_dir}.')
