import torch
import numpy as np
import torch.nn as nn
import matplotlib.pyplot as plt
import torchvision.transforms as transforms
from torch.utils.data import DataLoader, Dataset
import glob
import os
from PIL import Image

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 批处理大小
batch_size1 = 50


# 定义CNN模型
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Sequential(
            nn.Conv2d(  # 输入 3*84*84，batch_size = batch_size1=50
                in_channels=3,
                out_channels=16,
                kernel_size=5,
                stride=1,
                padding=2,
            ),  # (16，84，84)
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2),  # (16，42，42)
        )
        self.conv2 = nn.Sequential(  # (16，42，42)
            nn.Conv2d(16, 32, 5, 1, 2),  # (32，42，42)
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2),  # (32，21，21)
        )
        self.out = nn.Linear(32 * 21 * 21, batch_size1)  # (32，21，21) 这里第2个参数应为分类树，这里是10分类，则为10

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = x.view(-1, 32 * 21 * 21)  # (32，21，21)
        output = self.out(x)
        return output


# 将每个标签转换成对应的数字, 因为在使用字符串转换为张量会报错
labels = {'baihe': 1, 'dangshen': 2, 'gouqi': 3, 'huaihua': 4, 'jinyinhua': 5}


# 编写我自己的数据集的类
class MyDataSet(Dataset):
    def __init__(self, root_dir='./data', train_val='train', transform=None):
        self.data_path = os.path.join(root_dir, train_val)
        self.image_names = glob.glob(self.data_path + '/*/*.jpg')
        self.data_transform = transform
        self.train_val = train_val
        # print(self.image_names[0])

    def __len__(self):
        return len(self.image_names)

    def __getitem__(self, item):
        img_path = self.image_names[item]
        # print(img_path)
        img = Image.open(img_path).convert('RGB')
        # print(img.size)
        image = img
        label = img_path.split('\\')[-2]
        label = labels[label]
        label = torch.tensor(label)
        if self.data_transform is not None:
            try:
                image = self.data_transform(img)
            except:
                print('can not load image:{}'.format(img_path))
        return image, label


# 把数据转成tensor,并遵从正态分布
transform1 = transforms.Compose([
    transforms.Resize(84),
    transforms.CenterCrop(84),  # 将图像缩放成84*84大小
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])  # 标准化
])

# 使用MyDataSet来生成训练集,测试集（手动将文件夹test转换为train的格式，命名为test1）
train_dataset = {x: MyDataSet(
    root_dir=r'D:/桌面文件/pythonAI/lab8/data',
    train_val=x,
    transform=transform1
) for x in ['train', 'test1']}
# 使用DataLoader
train_loader = DataLoader(
    train_dataset['train'],
    batch_size=batch_size1,
    shuffle=True
)
test_loader = DataLoader(
    train_dataset['test1'],
    batch_size=10,  # 只有10张照片
    shuffle=True
)

# 实例化模型
model = Net()
# 检测显卡是否可用
use_cuda = torch.cuda.is_available()
# 使用GPU
if use_cuda:
    model.cuda()

print(model)
# 使用交叉熵损失函数
criterion = nn.CrossEntropyLoss()
# 使用带有动量的随机梯度下降
optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.5)
# 用于存储损失
loss_list = []
# 用于存储在训练集train中的准确率
acc = []
# 用于存储在test的10张照片中的准确率
acc2 = []
epochs = 40
# 总迭代次数
all = epochs * train_dataset['train'].__len__()
# print(all)
# 进行模型训练
for epoch in range(epochs):
    for batch, (X, y) in enumerate(train_loader):
        if use_cuda:
            X, y = X.cuda(), y.cuda()  # 使用GPU加速
        # 正向传播
        y_pred = model(X)
        # 计算损失
        loss = criterion(y_pred, y)
        # 梯度归零
        optimizer.zero_grad()
        # 反向传播
        loss.backward()
        # 更新参数
        optimizer.step()
        # 每n次看下损失和准确率
        if batch % 200 == 0:  # n = 200
            loss_list.append(loss.data.item())
            print("loss------------", loss.data.item())
            # 检验测试集的正确率
            total = 0
            correct = 0
            # 不需要计算梯度
            with torch.no_grad():
                for X, y in train_loader:  # 检验在训练集上的准确率
                    if use_cuda:
                        X, y = X.cuda(), y.cuda()
                    y_pred = model(X)
                    # 返回值有两个，第一个是最大的值，第二个是最大值的索引
                    _, predicted = torch.max(y_pred.data, dim=1)
                    total += y.size(0)
                    correct += (predicted == y).sum().item()
                acc.append((100.0 * (correct / total)))
                print("在训练集train中的准确率acc= ", acc[-1], "%")
                total = 0
                correct = 0
                for X, y in test_loader:  # 检验在测试集上的准确率
                    if use_cuda:
                        X, y = X.cuda(), y.cuda()
                    y_pred = model(X)
                    # 返回值有两个，第一个是最大的值，第二个是最大值的索引
                    _, predicted = torch.max(y_pred.data, dim=1)
                    total += y.size(0)
                    correct += (predicted == y).sum().item()
                acc2.append((100.0 * (correct / total)))
                print("在测试集test中的准确率acc2= ", acc2[-1], "%")

# 显示loss曲线图, all为总迭代次数 = epochs * 训练集大小(902)
plt.plot(np.linspace(0, all, len(loss_list)), loss_list)
plt.xlabel('迭代次数', fontsize=18)
plt.ylabel('代价', rotation=0, fontsize=18)
plt.title('误差和训练Epoch数', fontsize=18)
plt.show()
# 显示在训练集train的准确率acc曲线图
plt.plot(np.linspace(0, all, len(acc)), acc)
plt.xlabel("迭代次数", fontsize=18)
plt.ylabel("acc", rotation=0, fontsize=18)
plt.title('训练集train准确率和训练Epoch数', fontsize=18)
plt.show()
# 显示在测试集test的准确率acc2曲线图
plt.plot(np.linspace(0, all, len(acc2)), acc2)
plt.xlabel("迭代次数", fontsize=18)
plt.ylabel("acc2", rotation=0, fontsize=18)
plt.title('测试集test准确率和训练Epoch数', fontsize=18)
plt.show()

# 检验测试集test1中10张照片的正确率
# print("In test1:")
# total = 0
# correct = 0
# 不需要计算梯度
# with torch.no_grad():
#     for X, y in test_loader:  # 检验在训练集上的准确率
#         if use_cuda:
#             X, y = X.cuda(), y.cuda()
#         y_pred = model(X)
#         # 返回值有两个，第一个是最大的值，第二个是最大值的索引
#         _, predicted = torch.max(y_pred.data, dim=1)
#         total += y.size(0)
#         correct += (predicted == y).sum().item()
#         for i in range(10):
#             print("y[", i, "]=", y[i], "   predicted[", i, "]=", predicted[i], end="   ")
#             if predicted[i] == y[i]:
#                 print("True")
#             else:
#                 print("False")
#     acc2.append((100.0 * (correct / total)))
#     print(acc2[-1], "%")
