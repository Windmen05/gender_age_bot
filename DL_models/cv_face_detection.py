import cv2
import os
import warnings
warnings.filterwarnings("ignore")
from .sex_model import nn

class Face_Detection:
    def __init__(self, device='cpu', path=os.path.join(os.path.realpath('data/haarcascade_frontalface_default.xml'))):
        self.path = path
        self.model = self.load_Model()

    def load_Model(self):
        model = cv2.CascadeClassifier(self.path)
        print("load_model cv")
        return model

    '''
    # Given the path of an image, returns the neural network's predictions for that image
    ###Process photo with save on disk
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
    '''

    ###Process photo without save on disk // bytes
    def get_predictions(self, img_str, text):
        import numpy as np
        nparr = np.fromstring(img_str, np.uint8)
        img = cv2.imdecode(nparr, cv2.COLOR_BGR2GRAY)
        predicts = self.model.detectMultiScale(img, 1.1, 4)
        #size=predicts.shape[0]
        #img_ = img.copy()
        from PIL import Image
        for (x, y, w, h) in predicts:
            image = Image.fromarray(img[y:y+h, x:x+w])
            #nn.preprocess()
            #import torch
            image_preprocessed = nn.preprocess(image).unsqueeze(0)
            #raise IOError(image_preprocessed)
            #device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            predicts = nn.model(image_preprocessed.to(nn.device)).data.cpu()
            text = ((int(1 - bool(predicts.argmax())) * 'fe' + 'male : ') + str(round(float(predicts[0][predicts.argmax()]), 2) * 100) + "%")
            #img_crop = img[y:y+h, x:x+w]
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(img, text, (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (255, 0, 0),
                        2)
        return img#, img_crop
face_detection = Face_Detection()