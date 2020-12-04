from torch import cuda, load, device
import torchvision
from PIL import Image
import numpy as np
import os


class NeuralNetwork:
    def __init__(self, device='cpu', path=os.path.join(os.path.realpath('data/aerialmodel.pth'))):
        self.device = device("cuda" if cuda.is_available() else "cpu")
        self.path = path
        self.model = self.load_Model()

    def load_Model(self):
        model = load(self.path, map_location=self.device)
        model.eval()
        print("load_model ")
        return model

    # To preprocess an image to transform it to what is required by the Neural Network

    def preprocess(self, image):
        transformations = torchvision.transforms.Compose([torchvision.transforms.Resize((224, 224)),
                                                          torchvision.transforms.ToTensor(),
                                                          torchvision.transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                                                                           std=[0.229, 0.224, 0.225]),
                                                          ])
        return transformations(image)
    # Given the path of an image, returns the neural network's predictions for that image
    def get_predictions(self, image_filename):
        image = Image.open(image_filename).convert('RGB')
        image_preprocessed = self.preprocess(image).unsqueeze(0)
        predicts = self.model(image_preprocessed.to(self.device)).data.cpu()
        return (int(1 - predicts.argmax()) * 'fe' + 'male with chanse: ') + str(round(float(predicts[0][predicts.argmax()]),3)*100) + "%"

nn = NeuralNetwork()