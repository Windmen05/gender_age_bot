import cv2
import os
import warnings
warnings.filterwarnings("ignore")

# Load the cascade

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
path = os.path.join(os.path.realpath('data/haarcascade_frontalface_default.xml'))
# Read the input image
path2= cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
img = cv2.imread('test.jpg')
# Convert into grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Detect faces
faces = face_cascade.detectMultiScale(gray, 1.1, 4)

# Draw rectangle around the faces
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
# Display the output
cv2.imshow('img', img)
cv2.waitKey()


class NeuralNetwork:
    def __init__(self, device='cpu', path=os.path.join(os.path.realpath('data/haarcascade_frontalface_default.xml'))):
        self.path = path
        self.model = self.load_Model()

    def load_Model(self):
        model = cv2.CascadeClassifier(self.path)
        print("load_model ")
        return model

    # Given the path of an image, returns the neural network's predictions for that image
    def get_predictions(self, image_filename):
        image = cv2.cvtColor(image_filename, cv2.COLOR_BGR2GRAY)
        predicts = self.model.detectMultiScale(image, 1.1, 4)
        return predicts
face_detection = NeuralNetwork()