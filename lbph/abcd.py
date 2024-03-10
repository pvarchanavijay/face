import cv2
import os

cap = cv2.VideoCapture(1)

label = input("Enter the name: ")

dirname = "photos\\" + label

if not os.path.exists(dirname):
    os.mkdir(dirname)

cv2.namedWindow("camera", cv2.WINDOW_NORMAL)
cv2.resizeWindow("camera", 640, 480)

count = 0

while count < 50:
    ret, frame = cap.read()
    cv2.imshow("camera", frame)

    filename = os.path.join(dirname, f"img_{len(os.listdir(dirname))}.jpg")
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        face_img = frame[y:y+h, x:x+w]
        cv2.imwrite(filename, face_img)
        print(f"Photo saved: {filename}")
        count += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
        break

cap.release()
cv2.destroyAllWindows()
