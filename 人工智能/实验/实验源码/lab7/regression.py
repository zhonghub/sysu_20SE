# import imp
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

'''
获得数据
'''
path = (Path(__file__).parent) / 'data/regress_data2.csv'
data = pd.read_csv(str(path),dtype=np.double)
data2 = pd.read_csv(str(path))
'''
画原始数据曲线图
'''
'''
data.plot(kind='scatter', x='面积', y='价格', figsize=(12,8))
plt.xlabel('面积', fontsize=20)
plt.ylabel('价格', rotation=0, fontsize=20)
plt.suptitle("面积-价格")
plt.show()
'''

fig1 = plt.figure()
ax1 = fig1.add_subplot(111, projection='3d')
ax1.scatter(data['面积'],data['房间数'],data['价格'])
ax1.set_xlabel('面积')
ax1.set_ylabel('房间数')
ax1.set_zlabel('价格')
plt.suptitle("数据可视化图")
plt.show()
'''
计算均方误差
'''
def computeCost(X, y, w):
    inner = np.power((np.matmul(X, w) - y), 2)  # 矩阵相乘
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
x1max = data['面积'].max()
x1min = data['面积'].min()
x2max = data['房间数'].max()
x2min = data['房间数'].min()
ymax = data['价格'].max()
ymin = data['价格'].min()
for i in range(data.shape[0]):
    data['面积'][i] = (data['面积'][i]-x1min) / (x1max - x1min)
    data['房间数'][i] = (data['房间数'][i] - x2min) / (x2max - x2min)
    data['价格'][i] = (data['价格'][i] - ymin) / (ymax - ymin)

'''
获取数据
'''
X = data.iloc[:,:3] # 去掉y
X1 = data.iloc[:,:2] # 去掉x2 y
X2 = data.iloc[:,[0,2]] # 去掉x1 y
y = data.iloc[:,3:] # 去掉x1 x2

'''
为了方便矩阵运算，设置X，y，w的shape
'''
X = np.array(X.values, dtype=np.double) # (47, 3) 47行3列
X1 = np.array(X1.values, dtype=np.double) # (47, 2) 47行2列
X2 = np.array(X2.values, dtype=np.double) # (47, 2) 47行2列
y = np.array(y.values, dtype=np.double).reshape(-1, 1) # (47, 1)
w = np.array([0,0,0], dtype=np.double).reshape(-1, 1) #
'''
梯度下降
'''
def batch_gradientDescent(X, y, w, alpha, iters):
    temp = np.zeros(w.shape, dtype=np.double)
    parameters = w.shape[0]
    cost = []
    for i in range(iters):
        error = np.matmul(X, w) - y
        for j in range(parameters):
            term = np.multiply(error, X[:, j:j+1])
            #print("=======")
            #print(term)
            temp[j, 0] = w[j, 0] - ((alpha / len(X)) * (np.sum(term)))
        w = temp
        #print("===========")
        #print(w)
        #print("===========")
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
'''
x = np.linspace(data['房间数'].min(), data['房间数'].max(), 100)
x1 = np.linspace(data['面积'].min(), data['面积'].max(), 100)
x2 = np.linspace(data['房间数'].min(), data['房间数'].max(), 100)
f = x1 * g[1, 0] + g[0, 0]
fig, ax = plt.subplots(figsize=(12, 8))
ax.plot(x1, f, 'r', label='预测值')
ax.scatter(data['面积'], data['价格'], label='训练数据')
ax.legend(loc=2)
ax.set_xlabel('面积', fontsize=18)
ax.set_ylabel('价格', rotation=0, fontsize=18)
ax.set_title('预测', fontsize=18)
plt.show()
'''

ax1 = plt.axes(projection='3d')
#x1 = np.random.rand(10)
#x2 = np.random.rand(10)
x1 = np.linspace(0, 1, 10)
x2 = np.linspace(0, 1, 10)
x1, x2 = np.meshgrid(x1, x2)
f = x2 * g[2, 0] + x1 * g[1, 0] + g[0, 0]

for i in range(10):
    x1[i] = x1[i] * (x1max - x1min) + x1min
    x2[i] = x2[i] * (x2max - x2min) + x2min
    f[i] = f[i] * (ymax - ymin) + ymin

#tmp = pd.DataFrame(x1,columns=['X'])
#tmp['Y'] = x2
#tmp['Z'] = f
ax1.scatter(data2['面积'],data2['房间数'] , data2['价格'], label='训练数据')
#ax1.plot(tmp['X'], tmp['Y'], tmp['Z'],label='预测')
#ax1.legend()alpha=0.5
ax1.plot_surface(x1,x2,f,rstride=1, cstride=1, cmap=plt.cm.coolwarm,alpha=0.5)
ax1.set_xlabel('面积')
ax1.set_ylabel('房间数')
ax1.set_zlabel('价格')
plt.suptitle("数据可视化图")
plt.show()

'''
画loss曲线图
'''
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(np.arange(iters), cost, 'r')
ax.set_xlabel('迭代次数', fontsize=18)
ax.set_ylabel('代价', rotation=0, fontsize=18)
ax.set_title('误差和训练Epoch数', fontsize=18)
plt.show()
