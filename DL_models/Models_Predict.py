import torch
from torchvision import transforms
import warnings
import os
import numpy as np
import cv2
from PIL import Image
warnings.filterwarnings("ignore")


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

    def get_predictions(self, img_str):
        nparr = np.fromstring(img_str, np.uint8)
        img = cv2.imdecode(nparr, cv2.COLOR_BGR2GRAY)
        predicts_coordinates = self.model_face.detectMultiScale(img, 1.2, 4)

        face_numbers = predicts_coordinates.shape[0]
        preds_sex_chance = np.zeros(face_numbers)
        preds_sex = np.zeros(face_numbers)
        preds_age = np.zeros(face_numbers)

        for i, (x, y, w, h) in enumerate(predicts_coordinates):
            face = Image.fromarray(img[y:y + h, x:x + w])  # Took face only
            face_preprocessed = self.preprocess(face).unsqueeze(0).to(self.device)

            raw_sex = self.model_sex(face_preprocessed).data.cpu()
            raw_age = self.model_age(face_preprocessed).data.cpu()

            preds_sex_chance[i] = round(float(raw_sex[0][raw_sex.argmax()]), 2) * 100
            preds_sex[i] = raw_sex.argmax()
            preds_age[i] = int(round(float(raw_age), 1) * 10)

            text_1 = ((int(1 - preds_sex[i]) * 'fe' + 'male: ')
                      + str(preds_sex_chance[i]) + "%")
            cv2.putText(img, text_1, (x - 2, y - 7),
                        fontFace=cv2.FONT_HERSHEY_DUPLEX,
                        fontScale=1,
                        color=(0, 0, 0),
                        lineType=2
                        )
            cv2.putText(img, text_1, (x, y - 5),
                        fontFace=cv2.FONT_HERSHEY_DUPLEX,
                        fontScale=1,
                        color=(255, 255, 255),
                        lineType=2
                        )

            text_2 = "age: " + str(preds_age[i] / 10)
            cv2.putText(img, text_2, (x - 2, y - 32),
                        fontFace=cv2.FONT_HERSHEY_DUPLEX,
                        fontScale=1,
                        color=(0, 0, 0),
                        lineType=2
                        )
            cv2.putText(img, text_2, (x, y - 30),
                        fontFace=cv2.FONT_HERSHEY_DUPLEX,
                        fontScale=1,
                        color=(255, 255, 255),
                        lineType=2
                        )
            color = [255, 0, int(1-preds_sex[i])*255] #

            cv2.rectangle(img, (x, y), (x + w, y + h), (color), 2)
        return img, preds_sex_chance, preds_sex, preds_age


models_predict = Models_Predict()
