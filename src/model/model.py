import torch
import torch.nn as nn
from torchvision import models


class BaseCustomResNet(nn.Module):
    def __init__(self, n_classes, use_sigmoid=False):
        super(BaseCustomResNet, self).__init__()
        self.use_sigmoid = use_sigmoid
        resnet = models.resnet50(pretrained=True)

        # Freeze all layers in the network
        for param in resnet.parameters():
            param.requires_grad = False

        # Replace the last fully connected layer with the appropriate number of output classes
        num_ftrs = resnet.fc.in_features
        resnet.fc = nn.Linear(num_ftrs, n_classes)

        self.resnet = resnet

    def forward(self, x):
        x = self.resnet(x)
        if self.use_sigmoid:
            return torch.sigmoid(x)
        return x


class CustomResNet(BaseCustomResNet):
    def __init__(self):
        super(CustomResNet, self).__init__(n_classes=1, use_sigmoid=True)


class CustomMultiClassResNet(BaseCustomResNet):
    def __init__(self, n_classes):
        super(CustomMultiClassResNet, self).__init__(n_classes=n_classes)
