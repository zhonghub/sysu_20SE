import copy
import time
d_xy = [[0, 1, 0, -1], [1, 0, -1, 0]]
# d_xy = [[1, 0, -1, 0], [0, -1, 0, 1]]
goal = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]


class Node:
    father = -1     # 记录父节点的引用
    data = []
    last_key = 0    # 记录父节点的状态，避免由子节点返回父节点
    key_0 = 0   # 记录0的位置，x0 = key_0%4 , y0 = key_0 // 4 , 每次移动swap(0,i); key = x + y*4
    # f_x = 0      # 估价函数，f(x)=h(x)+g(x)
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
        # self.f_x = num + self.g_x    # h(x)+g(x)


def get_son(key0, last_key):  # 返回儿子节点的索引,将二维列表中的位置转化为一维列表中的位置
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


def out_answer(close_list):     # 输出关键路径
    f = close_list[-1]
    the_way = []
    # 回溯找关键路径, 从close表最后一条开始，逐个查找其父亲节点，
    # 直到某节点父亲节点为-1（即起始节点），并将所有查到的序列写入the_way并输出
    while True:
        the_way.append(f)
        f = f.father
        if f == -1:
            break
    t = len(the_way)
    for k in range(t):  # 输出关键路径
        print("move:", k, " h(x):", the_way[t-k-1].h_x, " g(x):", the_way[t-k-1].g_x, " f(x):", the_way[t-k-1].g_x + \
              the_way[t-k-1].h_x)
        for i in range(16):
            q = the_way[t-k-1].data[i]
            print(q, end=" ")
            if q < 10:
                print(" ", end="")
            if (i+1) % 4 == 0:
                print("")
        print("")


def A_star(open_list, close_list, other):
    find = False
    t0 = 1  # 记录节点的总数=len(open_list)+len(close_list)
    set0 = set()    # 记录已经出现过的节点
    while True:
        p2 = open_list[0]   # 浅复制，相等于引用
        key0 = p2.key_0
        list0 = get_son(p2.key_0, p2.last_key)
        for i0 in range(len(list0)):
            new_list = p2.data[:]   # 进行移动，即交换0与周围的位置
            tp = new_list[list0[i0]]
            new_list[list0[i0]] = new_list[key0]
            new_list[key0] = tp
            b1 = map(str, new_list)
            c1 = ",".join(b1)   # 把列表转化为字符串
            if c1 in set0:  # 如果不是新的节点
                continue
            # 否则是新的节点
            set0.add(c1)
            p3 = Node(new_list, p2.key_0, p2.g_x + 1)  # 生成p3
            """if p3 in set0:  # 如果不是新的节点
                continue
            # 否则是新的节点
            set0.add(p3)"""
            """if a != -1:         # 进行更新，似乎没必要，因为后续节点的g(x)更大(不一定，所以还是必要的)，而h(x)相同
                if p3.f_x < open_list[a].f_x:
                    open_list[a].g_x = p3.g_x"""
            if True:         # 说明是新的节点
                p3.father = p2    # 在节点p3中记录父亲节点p2在close表中的位置
                t0 += 1
                # open_list.append(p3)
                if len(open_list) == 0 or p3.g_x + p3.h_x >= open_list[-1].g_x + open_list[-1].h_x:
                    open_list.append(p3)
                else:
                    for i in range(1, len(open_list)):
                        if p3.g_x + p3.h_x < open_list[i].g_x + open_list[i].h_x:
                            open_list.insert(i, p3)     # 进行插入，完成排序
                            break
                if p3.h_x == 0:     # 目标状态
                    find = True
                    open_list.pop(0)
                    close_list.append(p2)
                    close_list.append(p3)
                    break
        open_list.pop(0)
        if find or len(open_list) == 0:
            break
        close_list.append(p2)
    other.append(find)      # 记录是否找到
    other.append(t0)        # 记录节点的总个数
    return


def main():
    print("start A*:")
    time1 = time.time()
    # 选择测试样例
    # p1 = Node([1, 2, 4, 8, 5, 7, 11, 10, 13, 15, 0, 3, 14, 6, 9, 12], -1, 0)   # 22
    # p1 = Node([5, 1, 3, 4, 2, 7, 8, 12, 9, 6, 11, 15, 0, 13, 10, 14], -1, 0)   # 15
    # p1 = Node([14, 10, 6, 0, 4, 9, 1, 8, 2, 3, 5, 11, 12, 13, 7, 15], -1, 0)  # 49
    # p1 = Node([6, 10, 3, 15, 14, 8, 7, 11, 5, 1, 0, 2, 13, 12, 9, 4], -1, 0)   # 48

    # p1 = Node([11, 3, 1, 7, 4, 6, 8, 2, 15, 9, 10, 13, 14, 12, 5, 0], -1, 0)     # 52+
    # p1 = Node([0, 5, 15, 14, 7, 9, 6, 13, 1, 2, 12, 10, 8, 11, 4, 3], -1, 0)     # 56+

    # p1 = Node([1, 15, 7, 10, 9, 14, 4, 11, 8, 5, 0, 6, 13, 3, 2, 12], -1, 0)    # 40
    p1 = Node([1, 7, 8, 10, 6, 9, 15, 14, 13, 3, 0, 4, 11, 5, 12, 2], -1, 0)    # 40
    # p1 = Node([5, 6, 4, 12, 11, 14, 9, 1, 0, 3, 8, 15, 10, 7, 2, 13], -1, 0)    # 40
    open_list = []
    close_list = []
    other = []  # find, t0
    i = 0
    while i < 1:
        i += 1
        open_list.clear()
        close_list.clear()
        other.clear()
        open_list.append(p1)
        A_star(open_list, close_list, other)
    time2 = time.time()

    if other[0]:
        print("have answer!")
        out_answer(close_list)
        print("all puzzles", len(open_list)+len(close_list), other[1])  # 输出节点的总个数
        print("Used Time %f" % (time2 - time1), "sec")
    else:
        print("no answer!")


if __name__ == '__main__':
    main()


