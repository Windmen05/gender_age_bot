import torch
from torchvision import transforms
from PIL import Image


def preprocess(image):
    transformations = transforms.Compose([transforms.Resize((224, 224)),
                                          transforms.ToTensor(),
                                          transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                                               std=[0.229, 0.224, 0.225]),
                                          ])
    return transformations(image)


class NeuralNetwork:
    def __init__(self, device='cpu', path="/home/vadim/Documents/GitHub/gender_age_bot/DL_models/models/aerialmodel.pth"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.path = path
        self.model = self.load_Model()

    def load_Model(self):
        model = torch.load(self.path, map_location=self.device)
        model.eval()
        return model

    # To preprocess an image to transform it to what is required by the Neural Network

    # Given the path of an image, returns the neural network's predictions for that image
    def get_predictions(self, image_filename):
        image = Image.open(image_filename).convert('RGB')
        image_preprocessed = preprocess(image).unsqueeze(0)
        print(image_preprocessed.size())
        predicts = self.model(image_preprocessed.to(self.device)).data.cpu()
        return predicts
nn = NeuralNetwork()
print(nn.get_predictions("/home/vadim/Pictures/Wallpapers/897.jpg"))