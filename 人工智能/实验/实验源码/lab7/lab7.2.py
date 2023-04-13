# import imp
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

# 获得数据
path = Path(__file__).parent / 'data/regress_data2.csv'
data = pd.read_csv(str(path), dtype=np.double)
data2 = pd.read_csv(str(path))

# 画原始数据可视化图
fig1 = plt.figure()
ax = fig1.add_subplot(projection='3d')
ax.scatter(data['面积'], data['房间数'], data['价格'])
ax.set_xlabel('面积')
ax.set_ylabel('房间数')
ax.set_zlabel('价格')
plt.suptitle("数据可视化图")
plt.show()

#计算均方误差
def computeCost(X, y, w):
    inner = np.power((np.matmul(X, w) - y), 2)
    return np.sum(inner) / (2 * X.shape[0])


# 添加bias
data.insert(0, 'Ones', 1) # 添加b的系数，因为b前面的系数为1，所以可以把1直接放在x里面
'''
例如 x = [3, 4], k = [0.1, 0.2], b = 0.01
kx+b = [0.1, 0.2] * [3, 4] + 0.01= [0.01, 0.1, 0.2] * [1, 3, 4] = [b, k0, k1] * [1, x1, x2] = b + k0*x0 + k1*x1 = b + kx 
为了方便运算，把b放到k里面的第一项，b和x无关，所以在x前面放个1
'''
# 数据归一化
x1max = data['面积'].max()
x1min = data['面积'].min()
x2max = data['房间数'].max()
x2min = data['房间数'].min()
ymax = data['价格'].max()
ymin = data['价格'].min()
for i in range(data.shape[0]):  # 归一化
    data['面积'][i] = (data['面积'][i]-x1min) / (x1max - x1min)
    data['房间数'][i] = (data['房间数'][i] - x2min) / (x2max - x2min)
    data['价格'][i] = (data['价格'][i] - ymin) / (ymax - ymin)
'''
获取数据
'''
cols = data.shape[1]
X = data.iloc[:, :cols-1]    # 去掉y
y = data.iloc[:, cols-1:]    # 去掉x1,x2
'''
为了方便矩阵运算，设置X，y，w的shape
'''
X = np.array(X.values, dtype=np.double)  # (97, 2)
y = np.array(y.values, dtype=np.double).reshape(-1, 1) # (97, 1)
w = np.array([0,0,0], dtype=np.double).reshape(-1, 1) # (2, 1)


# 梯度下降
def batch_gradientDescent(X, y, w, alpha, iters):
    temp = np.zeros(w.shape, dtype=np.double)
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

# 设置学习率和迭代次数
alpha = 0.01
iters = 10000
# 神经网络利用梯度下降学习参数
g, cost = batch_gradientDescent(X, y, w, alpha, iters)

# 画出预测函数图
x1 = np.linspace(0, 1, data.shape[0])
x2 = np.linspace(0, 1, data.shape[0])
x1, x2 = np.meshgrid(x1, x2)
f = x2 * g[2, 0] + x1 * g[1, 0] + g[0, 0]
for i in range(data.shape[0]):  # 数据复原
    x1[i] = x1[i] * (x1max - x1min) + x1min
    x2[i] = x2[i] * (x2max - x2min) + x2min
    f[i] = f[i] * (ymax - ymin) + ymin

ax1 = plt.axes(projection='3d')
ax1.scatter(data2['面积'],data2['房间数'], data2['价格'], label='训练数据')
ax1.plot_surface(x1,x2,f,rstride=1, cstride=1, cmap=plt.cm.coolwarm, alpha=0.5)
ax1.set_xlabel('面积')
ax1.set_ylabel('房间数')
ax1.set_zlabel('价格')
plt.suptitle("预测函数图")
plt.show()

# 画loss曲线图
fig, ax2 = plt.subplots(figsize=(8, 6))
ax2.plot(np.arange(iters), cost, 'r')
ax2.set_xlabel('迭代次数', fontsize=18)
ax2.set_ylabel('代价', rotation=0, fontsize=18)
ax2.set_title('误差和训练Epoch数', fontsize=18)
plt.show()
