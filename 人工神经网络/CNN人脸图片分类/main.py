import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder
from torch.nn.utils import clip_grad_norm_
from torch.optim.lr_scheduler import CosineAnnealingLR
from sklearn.metrics import accuracy_score
import os
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 4层卷积2层全连接，数据增强# 随机旋转 # 灰度变换
# SGD优化器，学习率调度器

# 参数
epochs = 10
batch_size1 = 64
img_size = 128  # 图像缩放
p_dropout = 0.5  # dropout概率
classes = 500  # 分类数
# SGD优化器参数
lr = 0.1
momentum = 0.7
max_lr = 0.03
weight_decay = 5e-4

# 检测显卡是否可用
use_cuda = torch.cuda.is_available()

# 数据增强
data_transforms = {
    'train': transforms.Compose([
        transforms.Resize(img_size),  # 图像缩放
        transforms.CenterCrop(img_size),
        transforms.RandomRotation(degrees=10),  # 随机旋转
        transforms.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.3, hue=0),  # 灰度变换
        transforms.ToTensor(),  # 转换为张量
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])  # 标准化
    ]),
    'test': transforms.Compose([
        transforms.Resize(img_size),  # 图像缩放
        transforms.CenterCrop(img_size),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
}
# 数据文件夹路径
data_dir = 'face_classification_500'
# 子文件夹名称（训练集、测试集、验证集）
path_dic = {'train': 'train_sample', 'test': 'test_sample', 'dev': 'dev_sample'}
# 选择对应的transform
transforms_dic = {'train': 'train', 'test': 'test', 'dev': 'test'}
# 加载图像数据
train_dataset = {x: ImageFolder(os.path.join(data_dir, path_dic[x]), data_transforms[transforms_dic[x]])
                 for x in ['train', 'test', 'dev']}
# 加载到dataloader，分成多个batch_size
batch_size_dic = {'train': batch_size1, 'test': len(train_dataset['test']), 'dev': batch_size1}
dataloaders = {x: DataLoader(train_dataset[x], batch_size=batch_size_dic[x], shuffle=True)
               for x in ['train', 'test', 'dev']}


# 4层卷积2层全连接
class CNN(nn.Module):
    def __init__(self, classes_num, p0):
        super(CNN, self).__init__()
        self.layers = 4  # 卷积层层数
        self.wh_new = img_size // (2 ** self.layers)  # 特征图大小
        self.out_channel = 4
        self.p = p0
        self.conv1 = nn.Sequential(
            nn.Conv2d(3, self.out_channel * 2, 3, 1, 1),
            nn.BatchNorm2d(self.out_channel * 2),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )
        self.conv2 = nn.Sequential(
            nn.Conv2d(self.out_channel * 2, self.out_channel * 4, 3, 1, 1),
            nn.BatchNorm2d(self.out_channel * 4),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )
        self.conv3 = nn.Sequential(
            nn.Conv2d(self.out_channel * 4, self.out_channel * 8, 3, 1, 1),
            nn.BatchNorm2d(self.out_channel * 8),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )
        self.conv4 = nn.Sequential(
            nn.Conv2d(self.out_channel * 8, self.out_channel * 16, 3, 1, 1),
            nn.BatchNorm2d(self.out_channel * 16),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )
        self.out_channel = self.out_channel * (2 ** self.layers) * self.wh_new * self.wh_new
        self.linear1 = nn.Linear(self.out_channel, 1024)
        self.drop1 = nn.Dropout(p=self.p)
        self.linear2 = nn.Linear(1024, classes_num)

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = self.conv4(x)

        x = x.view(-1, self.out_channel)
        x = self.linear1(x)
        x = F.relu(x)
        x = self.drop1(x)
        x = self.linear2(x)
        return x


# 绘制 训练集/验证集 正确率和损失图
def draw(train_acc, val_acc, train_loss, val_loss):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    ax1.plot(train_acc, '-o', label='训练集准确率')
    ax1.plot(val_acc, '-x', label='验证集准确率')
    ax1.set_title('准确率')
    ax1.set_xlabel('Epochs')
    ax1.set_ylabel('Accuracy')
    ax1.legend(loc='best')

    ax2.plot(train_loss, '-o', label='训练集误差')
    ax2.plot(val_loss, '-x', label='验证集误差')
    ax2.set_title('损失')
    ax2.set_xlabel('Epochs')
    ax2.set_ylabel('Loss')
    ax2.legend(loc='best')
    # 保存结果图片
    plt.savefig('loss_acc.png', dpi=300)
    # 显示图表
    # plt.show()


def test_model(model0, dataloader):
    model0.train(False)
    # 测试集只有1个batch
    for data in dataloader['test']:
        inputs, labels = data
        if use_cuda:
            inputs = inputs.cuda()
        outputs = model0(inputs)
        _, y_pred = torch.max(outputs.data, 1)
        acc = accuracy_score(labels.data.numpy(), y_pred.cpu().numpy())
        print('\nTest Acc: {:.4f}'.format(acc))


def train_model(model0, dataloader, criterion, optimizer, scheduler, num_epochs=25):
    train_acc, val_acc, train_loss, val_loss = [], [], [], []
    for epoch in range(num_epochs):
        print("\nepoch=", epoch)
        # 训练集用于训练，验证集用于调参
        for phase in ['train', 'dev']:
            if phase == 'train':
                model0.train(True)
            else:
                model0.train(False)
            running_loss = 0.0
            running_corrects = 0
            for data in dataloader[phase]:
                inputs, labels = data
                if use_cuda:
                    inputs, labels = inputs.cuda(), labels.cuda()
                # 梯度归零
                optimizer.zero_grad()
                # 正向传播
                outputs = model0(inputs)
                _, preds = torch.max(outputs.data, 1)
                # 计算损失
                loss = criterion(outputs, labels)
                if phase == 'train':
                    # 反向传播
                    loss.backward()
                    # 梯度裁剪
                    clip_grad_norm_(model0.parameters(), max_norm=1.0)
                    # 更新参数
                    optimizer.step()

                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)

            epoch_loss = running_loss / len(dataloader[phase].dataset)
            epoch_acc = running_corrects.double() / len(dataloader[phase].dataset)
            print('{} Loss: {:.4f} Acc: {:.4f}'.format(phase, epoch_loss, epoch_acc))
            if phase == 'train':
                train_acc.append(epoch_acc.cpu())
                train_loss.append(epoch_loss)
            else:
                val_acc.append(epoch_acc.cpu())
                val_loss.append(epoch_loss)
        # 更新学习率
        scheduler.step()
    return model0, (train_acc, val_acc, train_loss, val_loss)


# 训练model并保存训练好的checkpoint
def train(model0):
    # 使用交叉熵损失函数
    criterion = nn.CrossEntropyLoss()
    # 使用带有动量的随机梯度下降
    optimizer = torch.optim.SGD(filter(lambda p: p.requires_grad, model0.parameters()), lr=lr, momentum=momentum,
                                weight_decay=weight_decay)
    # 定义学习率调度
    scheduler = CosineAnnealingLR(optimizer, T_max=epochs, eta_min=max_lr)
    # 训练模型
    model0, list0 = train_model(model0, dataloaders, criterion, optimizer, scheduler, num_epochs=epochs)
    # 保存 checkpoint
    torch.save(model0.state_dict(), './model_checkpoint.pth')
    print("save model_checkpoint.pth")
    # 计算测试集正确率
    test_model(model0, dataloaders)
    # 画图:绘制 训练集/验证集 正确率和损失图
    draw(list0[0], list0[1], list0[2], list0[3])


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # 实例化模型
    model = CNN(classes, p_dropout)
    print(model)
    # 使用GPU
    if use_cuda:
        print("use GPU")
        model.cuda()
    else:
        print("use CPU")
    for i in range(1):
        print(i, " train:")
        lr = 0.1
        momentum = 0.7
        max_lr = 0.03
        weight_decay = 5e-4
        # 加载训练好的checkpoint, 可以在这个checkpoint上继续训练
        # model.load_state_dict(torch.load('./model_checkpoint.pth'))
        # 计算测试集正确率
        # test_model(model, dataloaders)
        # 训练model
        train(model)
