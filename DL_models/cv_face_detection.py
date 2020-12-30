import cv2
import os
import warnings
warnings.filterwarnings("ignore")


class Face_Detection:
    def __init__(self, device='cpu', path=os.path.join(os.path.realpath('data/haarcascade_frontalface_default.xml'))):
        self.path = path
        self.model = self.load_Model()

    def load_Model(self):
        model = cv2.CascadeClassifier(self.path)
        print("load_model cv")
        return model

    # Given the path of an image, returns the neural network's predictions for that image
    def get_predictions(self, image_filename, text):
        img = cv2.imread(image_filename)
        image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        predicts = self.model.detectMultiScale(image, 1.1, 4)
        for (x, y, w, h) in predicts:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(img, text, (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 0, 0),
                    2)
        return img
face_detection = Face_Detection()