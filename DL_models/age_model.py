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



class NeuralNetwork:
    def __init__(self, device='cpu', path=os.path.join(os.path.realpath('data/age_model.pth'))):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.path = path
        self.model = self.load_Model()

    def load_Model(self):
        model = torch.load(self.path, map_location=self.device)
        model.eval()
        print("load_model ")
        return model

    # To preprocess an image to transform it to what is required by the Neural Network

    def preprocess(self, image):
        transformations = transforms.Compose([#transforms.ToTensor(),
                                              transforms.Resize((224, 224)),

                                              transforms.ToTensor(),
                                              #transforms.Resize((224, 224)),
                                              transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                                                   std=[0.229, 0.224, 0.225]),
                                              ])
        return transformations(image)
    # Given the path of an image, returns the neural network's predictions for that image
    def get_predictions(self, img_str):
        nparr = fromstring(img_str, uint8)
        image1 = imdecode(nparr, cv2.IMREAD_ANYCOLOR)       #Need fix /
        temp = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)      #         \

        image2 = Image.fromarray(temp)

        image_preprocessed = self.preprocess(image2).unsqueeze(0)

        predicts = self.model(image_preprocessed.to(self.device)).data.cpu()
        return predicts

am = NeuralNetwork()