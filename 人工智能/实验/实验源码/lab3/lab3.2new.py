import copy
import time
d_xy = [[0, 1, 0, -1], [1, 0, -1, 0]]
# d_xy = [[1, 0, -1, 0], [0, -1, 0, 1]]
goal = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]


class Node:
    # father = None     # 记录父节点在close表中的位置
    data = []
    last_key = 0    # 记录父节点的状态，避免由子节点返回父节点
    key_0 = 0   # 记录0的位置，x0 = key_0%4 , y0 = key_0 // 4 , 每次移动swap(0,i); key = x + y*4
    f_x = 0      # 估价函数，f(x)=h(x)+g(x)
    g_x = 0     # 深度
    h_x = 0     # 启发函数,曼哈顿距离

    def __init__(self, list1, last, g_x1):
        self.g_x = g_x1         # 该节点的深度g(x)
        self.last_key = last    # 记录父节点中0的位置
        self.data = list1[:]
        num = 0
        for i in range(16):
            if self.data[i] == 0:
                self.key_0 = i
            else:
                x1 = i % 4
                y1 = i // 4
                x2 = (self.data[i] - 1) % 4
                y2 = (self.data[i] - 1) // 4
                d = abs(x2 - x1) + abs(y2 - y1)
                num += d
        self.h_x = num      # h(x)，曼哈顿距离
        self.f_x = num + self.g_x    # h(x)+g(x)


def get_son(key0, last_key):  # 返回儿子节点中0的位置,将二维列表中的位置转化为一维列表中的位置
    x0 = key0 % 4
    y0 = key0 // 4
    next_key = []
    for i in range(4):
        x = x0 + d_xy[0][i]
        y = y0 + d_xy[1][i]
        if 0 <= x <= 3 and 0 <= y <= 3:
            key = x + y * 4
            if key != last_key:  # 避免由子节点返回父节点
                next_key.append(key)
    return next_key


def is_in(node, list1):
    for i in range(len(list1)):  # 可用二分查找法或其他优化
        if node.data == list1[i].data:
            return i
    return -1


def out_answer(path):     # 输出关键路径
    t = len(path)
    for k in range(t):  # 输出关键路径
        print("move:", k, " h(x):", path[k].h_x, " g(x):", path[k].g_x, " f(x):", path[k].f_x)
        for i in range(16):
            q = path[k].data[i]
            print(q, end=" ")
            if q < 10:
                print(" ", end="")
            if (i+1) % 4 == 0:
                print("")
        print("")


def IDA_search(path, bound):
    p1 = path[-1]
    if p1.f_x > bound:  # 如果f(n)的值大于bound则返回f(n)
        return p1.f_x
    if p1.h_x == 0:  # 目标检测，以0表示找到目标
        return 0
    Min = 99999
    p2 = copy.deepcopy(p1)
    key0 = p2.key_0
    list0 = get_son(p2.key_0, p2.last_key)
    for i0 in range(len(list0)):        # 生成儿子节点
        new_list = p2.data[:]  # 进行移动，即交换0与周围的位置
        tp = new_list[list0[i0]]
        new_list[list0[i0]] = new_list[key0]
        new_list[key0] = tp
        p3 = Node(new_list, key0, p2.g_x + 1)  # 生成p3
        path.append(p3)     # dfs压栈
        t = IDA_search(path, bound)
        if t == 0:  # 如果得到的返回值为0，表示找到目标，迭代结束
            return 0
        if t < Min:  # 如果返回值不是0，且f>bound，这时对Min进行更新，取值最小的返回值作为Min
            Min = t
        path.pop()      # 栈去顶
    return Min


def IDA_star(start):
    bound = start.f_x  # start.f_x   # IDA*迭代限制,55
    path = [start]     # 路径集合, 视为栈
    while True:
        ans = IDA_search(path, bound)    # path, g, Hx, bound
        print(ans)      # 输出深度，查看深度变化
        if ans == 0:
            return path
        if ans == -1:
            return None
        bound = ans     # 此处对bound进行更新
    return []


def main():
    print("start A*:")
    time1 = time.time()
    # p1 = Node([1, 2, 4, 8, 5, 7, 11, 10, 13, 15, 0, 3, 14, 6, 9, 12], -1, 0)   # 22
    # p1 = Node([5, 1, 3, 4, 2, 7, 8, 12, 9, 6, 11, 15, 0, 13, 10, 14], -1, 0)   # 15
    p1 = Node([14, 10, 6, 0, 4, 9, 1, 8, 2, 3, 5, 11, 12, 13, 7, 15], -1, 0)   # 49
    # p1 = Node([6, 10, 3, 15, 14, 8, 7, 11, 5, 1, 0, 2, 13, 12, 9, 4], -1, 0)   # 48

    # p1 = Node([11, 3, 1, 7, 4, 6, 8, 2, 15, 9, 10, 13, 14, 12, 5, 0], -1, 0)     # 52+
    # p1 = Node([0, 5, 15, 14, 7, 9, 6, 13, 1, 2, 12, 10, 8, 11, 4, 3], -1, 0)     # 56+

    # p1 = Node([1, 15, 7, 10, 9, 14, 4, 11, 8, 5, 0, 6, 13, 3, 2, 12], -1, 0)    # 40
    # p1 = Node([1, 7, 8, 10, 6, 9, 15, 14, 13, 3, 0, 4, 11, 5, 12, 2], -1, 0)    # 40
    # p1 = Node([5, 6, 4, 12, 11, 14, 9, 1, 0, 3, 8, 15, 10, 7, 2, 13], -1, 0)    # 40
    path = []
    i = 0
    while i < 1:
        i += 1
        path.clear()
        path = IDA_star(p1)
    time2 = time.time()

    if len(path) > 0:
        print("have answer!\n")
        out_answer(path)
        print("all puzzles", len(path))     # 输出使用节点的最多个数
        print("Used Time %f" % (time2 - time1), "sec")
    else:
        print("no answer!\n")


if __name__ == '__main__':
    main()


