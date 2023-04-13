import torch
import numpy as np
import pandas as pd
import torch.nn as nn
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader
from torchvision.datasets import MNIST
import torchvision.transforms as transforms
from torch.utils.data import DataLoader, Dataset
import glob
import os
from PIL import Image
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
labels = {'baihe': [1,0,0,0,0], 'dangshen': [0,1,0,0,0], 'gouqi': [0,0,1,0,0],
          'huaihua': [0,0,0,1,0], 'jinyinhua': [1,0,0,0,1]}

class MyDataSet(Dataset):
    def __init__(self, root_dir='./data', train_val='train', transform=None):
        self.data_path = os.path.join(root_dir, train_val)
        self.image_names = glob.glob(self.data_path + '/*/*.jpg')
        self.data_transform = transform
        self.train_val = train_val
        #print(self.image_names[0])

    def __len__(self):
        return len(self.image_names)

    def __getitem__(self, item):
        img_path = self.image_names[item]
        #print(img_path)
        img = Image.open(img_path).convert('RGB')
        # print(img.size)
        image = img
        label = img_path.split('\\')[-2]
        label = labels[label]
        label = torch.tensor(label)
        if self.data_transform is not None:
            try:
                # image = self.data_path
                # image = self.data_transform[self.train_val](img)
                image = self.data_transform(img)
            except:
                print('can not load image:{}'.format(img_path))
        return image, label

transform1 = transforms.Compose([
    transforms.Resize(84),
    transforms.CenterCrop(84),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])  #  数据标准化
])

# 测试集
train_dataset = {x: MyDataSet(
    root_dir='D:/桌面文件/pythonAI/lab8/data',
    train_val=x,
    transform=transform1
) for x in ['train']}

# print(train_dataset['train'].image_names)

print(train_dataset['train'].__getitem__(0))

