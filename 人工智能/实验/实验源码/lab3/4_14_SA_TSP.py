import random
from math import exp

dist = [
[0, 9, -1000, 4, 14],
[9, 0, 12, 8, 5],\
[-1000, 12, 0, 13, 27],\
[4, 6, 13, 0, 6],\
[14, 5, 27, 6, 0]]

T0 = 100.0  # 初始温度
T_end = 5  # 结束温度
q = 0.98    # 每次退火的比例
L = 500    # 每个温度的迭代次数


def total_distance(a):  # 返回当前解的路径长度
    value = 0
    for j in range(4):
        value += dist[a[j]][a[j+1]]
    value += dist[a[0]][a[4]]
    return value


# 初始化一个解 [0,1,2,3..30]
def init_ans():
    ans = []
    for i in range(5):
        ans.append(i)
    return ans


# 随机选取两个节点交换位置，得到新解
def creat_new(ans_before):
    ans_after = ans_before[:]
    cuta = random.randint(0,4)
    cutb = random.randint(0,4)
    ans_after[cuta], ans_after[cutb] = ans_after[cutb], ans_after[cuta]
    return ans_after


if __name__ == '__main__':
    ans0 = init_ans()   # 记录当前路径
    ans_min = ans0  # 记录最短路径
    T = T0
    cnt = 0
    trend = []
    while T > T_end:    # 当当前温度>结束温度时继续降温
        for i in range(L):  # 在当前温度下循环产生新解
            new_ans = creat_new(ans0)   # 随机产生新解
            old_dist = total_distance(ans0)
            new_dist = total_distance(new_ans)
            if new_dist < 0:    # 表明该新解含不可达的路径
                continue
            df = new_dist - old_dist
            if df >= 0:     # 新解路径更大时
                rand = random.uniform(0,1)
                if rand < 1/(exp(df / T)):
                    ans0 = new_ans
            else:   # 新解路径更小时
                ans0 = new_ans
        T = T * q
        cnt += 1
        now_dist = total_distance(ans0)
        min_dist = total_distance(ans_min)
        if now_dist < min_dist:     # 当前路径为最短路径时替换
            ans_min = ans0
        print(cnt, "次降温，温度为：", T, " 当前路程长度为：", now_dist, " 最短路程长度为：", min_dist)
    min_distance = total_distance(ans_min)
    print("最短路径长度：", min_distance)
    print("最短路径为", end=":")
    for i in range(5):
        c = ans_min[i]+65
        print(chr(c), end="")
        print(" <-> ", end="")
    c = ans_min[0] + 65
    print(chr(c))
    # 最短路径长度： 48
    # 最短路径为:C <-> D <-> A <-> E <-> B <-> C
