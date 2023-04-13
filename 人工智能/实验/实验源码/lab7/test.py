# import imp
import importlib
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
'''
获得数据
'''
path = (Path(__file__).parent) / 'data/regress_data1.csv'
data = pd.read_csv(str(path))
'''
画原始数据曲线图
'''
data.plot(kind='scatter', x='人口', y='收益', figsize=(12,8))
plt.xlabel('人口', fontsize=18)
plt.ylabel('收益', rotation=0, fontsize=18)
plt.show()
'''
计算均方误差
'''
def computeCost(X, y, w):
    inner = np.power((np.matmul(X, w) - y), 2)
    return np.sum(inner) / (2 * X.shape[0])

'''
添加bias
'''
data.insert(0, 'Ones', 1) # 添加b的系数，因为b前面的系数为1，所以可以把1直接放在x里面
'''
例如 x = [3, 4]
k = [0.1, 0.2]
b = 0.01
kx+b = [0.1, 0.2] * [3, 4] + 0.01= [0.01, 0.1, 0.2] * [1, 3, 4] = [b, k0, k1] * [1, x1, x2] = b + k0*x0 + k1*x1 = b + kx 
为了方便运算，把b放到k里面的第一项，b和x无关，所以在x前面放个1
'''

'''
获取数据
'''
cols = data.shape[1]
X = data.iloc[:,:cols-1] # 去掉y
y = data.iloc[:,cols-1:] # 去掉x

'''
为了方便矩阵运算，设置X，y，w的shape
'''
X = np.array(X.values, dtype=np.float) # (97, 2)
y = np.array(y.values, dtype=np.float).reshape(-1, 1) # (97, 1)
w = np.array([0,0], dtype=np.float).reshape(-1, 1) # (2, 1)

'''
梯度下降
'''
def batch_gradientDescent(X, y, w, alpha, iters):
    temp = np.zeros(w.shape, dtype=np.float)
    parameters = w.shape[0]
    cost = []
    for i in range(iters):
        error = np.matmul(X, w) - y
        for j in range(parameters):
            term = np.multiply(error, X[:, j:j+1])
            temp[j, 0] = w[j, 0] - ((alpha / len(X)) * np.sum(term))
        w = temp
        cost.append(computeCost(X, y, w))
    return w, cost

'''
设置学习率和迭代次数
'''
alpha = 0.01
iters = 1000

'''
神经网络利用梯度下降学习参数
'''
g, cost = batch_gradientDescent(X, y, w, alpha, iters)

'''
生成一组随机特征x，画曲线图
'''
x = np.linspace(data['人口'].min(), data['人口'].max(), 100)
f = x * g[1, 0] + g[0, 0]
fig, ax = plt.subplots(figsize=(12, 8))
ax.plot(x, f, 'r', label='预测值')
ax.scatter(data['人口'], data['收益'], label='训练数据')
ax.legend(loc=2)
ax.set_xlabel('人口', fontsize=18)
ax.set_ylabel('收益', rotation=0, fontsize=18)
ax.set_title('预测收益和人口规模', fontsize=18)
plt.show()

'''
画loss曲线图
'''
fig, ax = plt.subplots(figsize=(12, 8))
ax.plot(np.arange(iters), cost, 'r')
ax.set_xlabel('迭代次数', fontsize=18)
ax.set_ylabel('代价', rotation=0, fontsize=18)
ax.set_title('误差和训练Epoch数', fontsize=18)
plt.show()
