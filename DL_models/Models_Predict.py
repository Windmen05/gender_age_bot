import cv2
import os
import warnings
warnings.filterwarnings("ignore")
from .sex_model import nn
import numpy as np
import torch
from torchvision import transforms
from PIL import Image
import warnings
warnings.filterwarnings("ignore")
import os
from numpy import fromstring, uint8, expand_dims
from cv2 import imdecode, COLOR_BGR2GRAY
import numpy as np
import cv2
from PIL import Image


class Models_Predict:
    def __init__(self, device='cpu',
                 path_face=os.path.join(os.path.realpath('data/haarcascade_frontalface_default.xml')),
                 path_sex=os.path.join(os.path.realpath('data/aerialmodel.pth')),
                 path_age=os.path.join(os.path.realpath('data/age_model.pth'))
                 ):
        self.path_face = path_face
        self.path_sex = path_sex
        self.path_age = path_age
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_face, self.model_sex, self.model_age = self.load_Models()


    def load_Models(self):
        model_face = cv2.CascadeClassifier(self.path_face)
        model_sex = torch.load(self.path_sex, map_location=self.device)
        model_sex.eval()
        model_age = torch.load(self.path_age, map_location=self.device)
        model_age.eval()
        print("load_model cv")
        return model_face, model_sex, model_age


    def preprocess(self, image):
        transformations = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225]),
        ])
        return transformations(image)


    def get_predictions(self, img_str, text):
        nparr = np.fromstring(img_str, np.uint8)
        img = cv2.imdecode(nparr, cv2.COLOR_BGR2GRAY)
        predicts = self.model_face.detectMultiScale(img, 1.2, 4)
        for (x, y, w, h) in predicts:
            image = Image.fromarray(img[y:y+h, x:x+w])
            image_preprocessed = self.preprocess(image).unsqueeze(0).to(self.device)

            predicts_sex = self.model_sex(image_preprocessed).data.cpu()
            predicts_age = self.model_age(image_preprocessed).data.cpu()
            text_1 = ((int(1 - bool(predicts_sex.argmax())) * 'fe' + 'male: ')
                    + str(round(float(predicts_sex[0][predicts_sex.argmax()]), 2) * 100) + "%")
            cv2.putText(img, text_1, (x, y-5),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        2)
            text_2 = "age: " + str(round(float(predicts_age), 1))
            cv2.putText(img, text_2 , (x, y-30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        2)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

        return img
models_predict = Models_Predict()