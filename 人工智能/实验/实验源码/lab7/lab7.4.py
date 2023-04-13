import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import numpy.random
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def model(X, theta):
    # 预测函数  得到预测结果  矩阵相乘
    return sigmoid(np.dot(X, theta.T))

def cost(X, y, theta):
    # 计算损失函数 按照公式
    left = np.multiply(-y, np.log(model(X, theta)))  # 左边的连乘
    right = np.multiply((1 - y), np.log(1 - model(X, theta))) # 右边的连乘
    return np.sum(left - right) / (len(X))

def gradient(X, y, theta):
    # 求解梯度 grad为 theta梯度的更新值
    grad = np.zeros(theta.shape)
    error = (model(X, theta) - y).ravel()
    for j in range(len(theta.ravel())):
        temp = np.multiply(error, X[:,j])
        grad[0, j] = np.sum(temp) / len(X)
    return grad


def shuffleData(data):
    # 洗牌 防止数据有一定的排列规律
    np.random.shuffle(data)
    cols = data.shape[1]
    X = data[:, 0:cols-1]
    y = data[:, cols-1:]
    return X, y


# 最主要的函数 梯度下降求解
def descent(data, w, batchSize, thresh, alpha):
    # batchSize： 为整体值表示批量梯度下降
    # thresh 阈值
    # alpha 学习率
    k = 0 # batch 迭代数据的初始量
    X, y = shuffleData(data)
    costs = [cost(X, y, w)] # 损失值
    for i in range(thresh):
        # batchSize为指定的梯度下降策略
        grad = gradient(X[k:k+batchSize], y[k:k+batchSize], w)
        k += batchSize  # 取batch数量个数据
        if k >= n:
            k = 0
            X, y = shuffleData(data) #重新洗牌
        w = w - alpha*grad # 参数更新
        costs.append(cost(X, y, w)) # 计算新的损失
    return w, costs


path = (Path(__file__).parent) / 'classification_data.txt'
# 载入数据（训练集）
data = pd.read_csv(str(path), header=None, names=['特征一', '特征二', '录取结果'])   #特征一,特征二,录取结果
"""
colors = []
for i in range(data.shape[0]):
    t1 = 'g' if data['录取结果'][i] == 1 else 'r'
    colors.append(t1)
'''
画原始数据曲线图
'''
fig1 = plt.figure()
ax = fig1.add_subplot()
ax.scatter(data['特征一'], data['特征二'], c=colors)
ax.set_xlabel('特征一')
ax.set_ylabel('特征二')
plt.suptitle("数据可视化图")
plt.show()
"""

data.insert(0, 'Ones', 1)
orig_data = data.values
cols = orig_data.shape[1]
X = orig_data[:,0:cols-1]
y = orig_data[:,cols-1:cols]

w = np.zeros([1, 3])

# 设定迭代次数为50000次
n = 100
# runExpe(orig_data, w, n, thresh=50000, alpha=0.0001)
thresh = 50000
alpha = 0.0001
theta, costs = descent(orig_data, w, n, thresh, alpha)
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(np.arange(len(costs)), costs, 'r')
ax.set_xlabel('迭代次数')
ax.set_ylabel('代价')
ax.set_title('误差和训练Epoch数')
plt.show()
