# import imp
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 获得数据
path = Path(__file__).parent / 'classification_data.txt'
data = pd.read_csv(str(path), header=None, names=['特征一', '特征二', '录取结果'], dtype=np.double)
data2 = pd.read_csv(str(path), header=None, names=['特征一', '特征二', '录取结果'], dtype=np.double)
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
'''
计算均方误差
'''

'''
添加bias
'''
data.insert(0, 'Ones', 1)  # 添加b的系数，因为b前面的系数为1，所以可以把1直接放在x里面
'''
例如 x = [3, 4]
k = [0.1, 0.2]
b = 0.01
kx+b = [0.1, 0.2] * [3, 4] + 0.01= [0.01, 0.1, 0.2] * [1, 3, 4] = [b, k0, k1] * [1, x1, x2] = b + k0*x0 + k1*x1 = b + kx 
为了方便运算，把b放到k里面的第一项，b和x无关，所以在x前面放个1
'''
x1max = data['特征一'].max()
x1min = data['特征一'].min()
x2max = data['特征二'].max()
x2min = data['特征二'].min()
ymax = data['录取结果'].max()
ymin = data['录取结果'].min()
for i in range(data.shape[0]):  # 归一化
    data['特征一'][i] = (data['特征一'][i] - x1min) / (x1max - x1min)
    data['特征二'][i] = (data['特征二'][i] - x2min) / (x2max - x2min)
    data['录取结果'][i] = (data['录取结果'][i] - ymin) / (ymax - ymin)
'''
获取数据
'''
cols = data.shape[1]
X = data.iloc[:, :cols - 1]  # 去掉y
y = data.iloc[:, cols - 1:]  # 去掉x1,x2
# x1 = data.iloc[:,cols-3:cols-2]
# x2 = data.iloc[:,cols-2:cols-1]
# y = data.iloc[:,cols-1:]
'''
为了方便矩阵运算，设置X，y，w的shape
'''
X = np.array(X.values, dtype=np.float)  # (97, 2)
y = np.array(y.values, dtype=np.float).reshape(-1, 1)  # (97, 1)
w = np.array([0, 0, 0], dtype=np.float).reshape(-1, 1)  # (2, 1)


# 定义sigmoid函数。
def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def model(X, w):
    # 预测函数  得到预测结果  矩阵相乘
    return sigmoid(np.matmul(X, w))


def cost1(X, y, w):
    # 计算损失函数 按照公式
    left = np.multiply(-y, np.log(model(X, w)))  # 左边的连乘
    right = np.multiply((1 - y), np.log(1 - model(X, w))) # 右边的连乘
    return np.sum(left - right) / (2 * X.shape[0])


def computeCost(X, y, w):
    # y^ = (np.matmul(X, w)
    inner = np.power((np.matmul(X, w) - y), 2)
    return np.sum(inner) / (2 * X.shape[0])


# 梯度下降
def batch_gradientDescent(X, y, w, alpha, iters):
    temp = np.zeros(w.shape, dtype=np.double)
    parameters = w.shape[0]
    cost = []
    for i in range(iters):
        error = np.matmul(X, w) - y
        for j in range(parameters):
            term = np.multiply(error, X[:, j:j + 1])
            temp[j, 0] = w[j, 0] - ((alpha / len(X)) * np.sum(term))
        w = temp
        cost.append(computeCost(X, y, w))
    return w, cost


'''
设置学习率和迭代次数
'''
alpha = 0.01
iters = 1500
'''
神经网络利用梯度下降学习参数
'''
g, cost = batch_gradientDescent(X, y, w, alpha, iters)

# 画出边界曲线
x1 = np.linspace(0, 1, 100)
x2 = np.linspace(0, 1, 100)
x1, x2 = np.meshgrid(x1, x2)
# f = x2 * g[2, 0] + x1 * g[1, 0] + g[0, 0]
# x_2 = (f - x_1*g[1,0] - g[0,0])/g[2,0]
x3 = (0.5 - x1 * g[1, 0] - g[0, 0]) / g[2, 0]

for i in range(100):
    x1[i] = x1[i] * (x1max - x1min) + x1min
    x2[i] = x2[i] * (x2max - x2min) + x2min
    x3[i] = x3[i] * (x2max - x2min) + x2min


plt.scatter(x1, x3,  c='k')
plt.scatter(data2['特征一'], data2['特征二'], c=np.array(colors))
plt.xlabel('特征一', fontsize=15)
plt.ylabel('特征二', rotation=0, fontsize=15)
plt.suptitle("数据可视化图")
plt.show()

# 画loss曲线图
fig, ax2 = plt.subplots(figsize=(8, 6))
ax2.plot(np.arange(iters), cost, 'r')
ax2.set_xlabel('迭代次数', fontsize=18)
ax2.set_ylabel('代价', rotation=0, fontsize=18)
ax2.set_title('误差和训练Epoch数', fontsize=18)
plt.show()

x1 = data.iloc[:,1:2]
x2 = data.iloc[:,2:3]
x1 = np.array(x1, dtype=np.double).reshape(-1, 1)
x2 = np.array(x2, dtype=np.double).reshape(-1, 1)
f = x2 * g[2, 0] + x1 * g[1, 0] + g[0, 0]
y = data.iloc[:,3:]
y = np.array(y).reshape(-1, 1)
countright = 0
for i in range(f.shape[0]):
    if(f[i] > 0.5):
        if(y[i] == 1):
            countright += 1
    else:
        if(y[i] == 0):
            countright += 1
print("模型收敛后的分类准确率",countright,"%")