import numpy as np
from PIL import Image
import torch
from os import getenv
import torchvision.models as models


class Model():
    def __init__(self):
        model_path = getenv('MODEL_PATH', None)
        if model_path is None:
            self.model = models.densenet161(pretrained=True)
        else:
            self.model = torch.load(model_path)
        self.width = getenv('WIDTH', 224)
        self.height = getenv('HEIGHT', 224)

    def process_image(self, img_path):
        '''
        Recieves an img_path
        Returns a proccess image for densenet 161 of pytorch
        '''
        img = Image.open(img_path)
        width, height = img.size
        img = img.resize((255, int(255*(height/width))) \
            if width < height else (int(255*(width/height)), 255))
        width, height = img.size
        left = (width - self.width)/2
        top = (height - self.height)/2
        right = (width + self.width)/2
        bottom = (height + self.height)/2
        img = img.crop((left, top, right, bottom))
        img = np.array(img)
        img = img.transpose((2, 0, 1))
        img = img/255
        img = img[np.newaxis,:]
        image = torch.from_numpy(img)
        image = image.float()
        return image
    
    def predict_classes(self, image):
        '''
        Recieves an image already proccesed
        Returns top probability and class
        '''
        output = self.model.forward(image)
        output = torch.exp(output)
        probs, classes = output.topk(1, dim=1)
        return probs.item(), classes.item()
