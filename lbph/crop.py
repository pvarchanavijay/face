import cv2

# Load the input image
img = cv2.imread("photos/photo_0.jpg")

# Load the face detection classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

# Crop the face from the image
for (x, y, w, h) in faces:
    face_img = img[y:y+h, x:x+w]

# Display the cropped face image
cv2.imshow("face", face_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
