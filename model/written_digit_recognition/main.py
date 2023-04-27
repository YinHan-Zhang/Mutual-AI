# -*- coding = utf-8 -*-
# @Time: 2023/04/27
# @Author:MoyiTech
# @Software: PyCharm
from PIL import Image, ImageEnhance
import torch
from torchvision import transforms
import time
from torch import nn
import os
import pickle


class VGGNet(nn.Module):
    def __init__(self, in_dim, n_hidden_1, n_hidden_2, out_dim):
        super().__init__()  # 1 28 28

        self.layer1 = nn.Sequential(
            nn.Conv2d(1, 32, 3, 1, padding=1),  # 32 28 28
            nn.BatchNorm2d(32),
            nn.ReLU(True),
            nn.MaxPool2d(2, 2)  # 32 14 14
        )

        self.layer2 = nn.Sequential(
            nn.Conv2d(32, 64, 3, 1, padding=1),  # 64 14 14
            nn.BatchNorm2d(64),
            nn.ReLU(True),
            nn.MaxPool2d(2, 2)  # 64 7 7
        )

        self.layer3 = nn.Sequential(
            nn.Conv2d(64, 128, 3, 1, padding=1),  # 128 7 7
            nn.BatchNorm2d(128),
            nn.ReLU(True),
            nn.MaxPool2d(2, 2)  # 128 3 3
        )

        self.layer4 = nn.Sequential(
            nn.Conv2d(128, 256, 3, 1, padding=1),  # 256 3 3
            nn.BatchNorm2d(256),
            nn.ReLU(True),
            nn.MaxPool2d(2, 2)  # 256 1 1
        )

        self.layer5 = nn.Sequential(
            nn.Flatten(),
            nn.Linear(256 * 1 * 1, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(True),
            nn.Linear(512, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(True),
            nn.Linear(128, out_dim)
        )

        self.layers = nn.Sequential(
            self.layer1,
            self.layer2,
            self.layer3,
            self.layer4,
            self.layer5
        )

    def forward(self, x):
        out = self.layers(x)
        return out


model = VGGNet(28 * 28, 300, 100, 10)
model.load_state_dict(torch.load(os.path.join(os.path.dirname(__file__), 'model.pth'), map_location='cpu'))

if torch.cuda.is_available():
    model.to('cuda')

model.eval()
start = time.time()


def recognize(img):
    img = Image.open(img)
    img = img.resize((28, 28)).convert('L')

    # 亮度增强
    enh_bri = ImageEnhance.Brightness(img)
    brightness = 1
    img = enh_bri.enhance(brightness)

    # 色度增强(饱和度↑)
    enh_col = ImageEnhance.Color(img)
    color = 2
    img = enh_col.enhance(color)

    # 对比度增强
    enh_con = ImageEnhance.Contrast(img)
    contrast = 2
    img = enh_con.enhance(contrast)

    # 锐度增强
    enh_sha = ImageEnhance.Sharpness(img)
    sharpness = 2
    img = enh_sha.enhance(sharpness)

    img_tensor = transforms.ToTensor()(img)
    img_tensor = transforms.Normalize([0.5], [0.5])(img_tensor)

    out = model(img_tensor.unsqueeze(0))
    _, pred = out.max(axis=1)
    return pred[0].item()
