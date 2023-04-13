import copy
import heapq
import time
d_xy = [[0, 1, 0, -1], [1, 0, -1, 0]]
# d_xy = [[1, 0, -1, 0], [0, -1, 0, 1]]
goal = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]

"""
    data = []
    father = -1  # 记录父节点的引用
    last_key = 0  # 记录父节点的状态，避免由子节点返回父节点
    key_0 = 0  # 记录0的位置，x0 = key_0%4 , y0 = key_0 // 4 , 每次移动swap(0,i); key = x + y*4
    # f_x = 0      # 估价函数，f(x)=h(x)+g(x)
    g_x = 0  # 深度
    h_x = 0  # 启发函数,曼哈顿距离"""


def get_str(list0):
    b1 = map(str, list0)
    c1 = ",".join(b1)  # 把列表转化为字符串
    return c1


def get_msg(data, last, g_x1):
    father = '-1'
    now_str = get_str(data)  # 记录父节点的在close表中的位置key值
    last_key = 0  # 记录父节点的状态，避免由子节点返回父节点
    key_0 = 0  # 记录0的位置，x0 = key_0%4 , y0 = key_0 // 4 , 每次移动swap(0,i); key = x + y*4
    # f_x = 0      # 估价函数，f(x)=h(x)+g(x)
    g_x = 0  # 深度
    h_x = 0  # 启发函数,曼哈顿距离
    g_x += g_x1         # 该节点的深度g(x)
    last_key += last    # 记录父节点中0的位置
    num = 0
    for i in range(16):
        if data[i] == 0:
            key_0 = i
        else:
            x1 = i % 4
            y1 = i // 4
            x2 = (data[i] - 1) % 4
            y2 = (data[i] - 1) // 4
            d = abs(x2 - x1) + abs(y2 - y1)
            num += d
    h_x += num      # h(x)，曼哈顿距离
    return [data[:], now_str, last_key, key_0, g_x, h_x, g_x + h_x, father]


def get_son(key0, last_key):  # 返回儿子节点的索引,将二维列表中的位置转化为一维列表中的位置
    x0 = key0 % 4
    y0 = key0 // 4
    next_key = []
    if x0 > 0 and key0 - 1 != last_key:
        next_key.append(key0 - 1)
    if x0 < 3 and key0 + 1 != last_key:
        next_key.append(key0 + 1)
    if y0 > 0 and key0 - 4 != last_key:
        next_key.append(key0 - 4)
    if y0 < 3 and key0 + 4 != last_key:
        next_key.append(key0 + 4)
    return next_key


def out_answer(close_dic):     # 输出关键路径, [data[:], now_str, last_key, key_0, g_x, h_x, f_x, father]
    f = get_str(goal)
    the_way = []
    # 回溯找关键路径, 从close表最后一条开始，逐个查找其父亲节点，
    # 直到某节点父亲节点为-1（即起始节点），并将所有查到的序列写入the_way并输出
    while True:
        # print(f)
        the_way.append(close_dic[f])
        f = close_dic[f][-1]
        if f == '-1':
            break
    t = len(the_way)
    for k in range(t):  # 输出关键路径
        print("move:", k, " g(x):", the_way[t-k-1][-4], " h(x):", the_way[t-k-1][-3], " f(x):", the_way[t-k-1][-2])
        for i in range(16):
            q = the_way[t-k-1][0][i]
            print(q, end=" ")
            if q < 10:
                print(" ", end="")
            if (i+1) % 4 == 0:
                print("")
        print("")


def A_star(open_dic, close_dic, other):
    find = False
    t0 = 1  # 记录节点的总数=len(open_list)+len(close_list)
    vals = list(open_dic.values())
    # print(vals)
    open_list = []
    heapq.heappush(open_list, [vals[0][-2], vals[0][1]])
    while True:
        if len(open_list) == 0:
            break
        min_key = heapq.heappop(open_list)
        p2 = open_dic[min_key[1]]  # [data[:], now_str, last_key, key_0, g_x, h_x, f_x, father]

        if t0 % 100000 == 0 or t0 % 100000 == 1:
            print("now puzzles", len(open_dic) + len(close_dic), t0, "g(x)", p2[-4])  # 输出节点的总个数

        if p2[-3] == 0:  # 目标状态
            find = True
            close_dic[p2[1]] = p2
            open_dic.pop(p2[1])
            open_list.pop(0)
            break
        # print(len(open_dic), len(close_dic))
        list0 = get_son(p2[3], p2[2])
        for i0 in range(len(list0)):
            new_list = p2[0][:]   # 进行移动，即交换0与周围的位置
            tp = new_list[list0[i0]]
            new_list[list0[i0]] = new_list[p2[3]]
            new_list[p2[3]] = tp
            p3 = get_msg(new_list[:], p2[3], p2[4] + 1)
            v0 = open_dic.get(p3[1])
            v1 = close_dic.get(p3[1])
            # if v1 and not v0:
            #    continue
            if v0:  # 如果已经在open表里，判断是否需要更新
                value1 = v0[-2]
                if p3[-2] >= value1:  # 如果不是新的节点且不用更新
                    continue
                if p3[-2] < value1:  # 如果不是新的节点且需要更新,有问题
                    open_dic[p3[1]][4] = p3[4]
                    open_dic[p3[1]][-2] = p3[-2]
                    open_dic[p3[1]][-1] = p2[1]
                    continue
            # 否则不在open表里
            else:
                if v1:  # 如果在close表里
                    value1 = v1[-2]
                    if p3[-2] >= value1:  # 且不用更新
                        continue
                else:   # 否则是新节点
                    t0 += 1
                p3[-1] = p2[1]  # 设置p3的父亲节点为p2,含更新
                open_dic[p3[1]] = p3  # [data[:], now_str, last_key, key_0, g_x, h_x, f_x, father]
                # 在open_list里存储[[f_x, now_str],...,...]
                heapq.heappush(open_list, [p3[-2], p3[1]])
        close_dic[p2[1]] = p2
        open_dic.pop(p2[1])
    other.append(find)      # 记录是否找到
    other.append(t0)        # 记录节点的总个数
    return


def main():
    print("start A*:")
    time1 = time.time()
    # 选择测试样例
    # p1 = [1, 2, 4, 8, 5, 7, 11, 10, 13, 15, 0, 3, 14, 6, 9, 12]   # 22
    # p1 = [5, 1, 3, 4, 2, 7, 8, 12, 9, 6, 11, 15, 0, 13, 10, 14]   # 15
    # p1 = [14, 10, 6, 0, 4, 9, 1, 8, 2, 3, 5, 11, 12, 13, 7, 15]  # 49
    p1 = [6, 10, 3, 15, 14, 8, 7, 11, 5, 1, 0, 2, 13, 12, 9, 4]   # 48

    # p1 = [11, 3, 1, 7, 4, 6, 8, 2, 15, 9, 10, 13, 14, 12, 5, 0]     # 56, 62以下
    # p1 = [0, 5, 15, 14, 7, 9, 6, 13, 1, 2, 12, 10, 8, 11, 4, 3]     # 56+，82以下

    # p1 = [1, 15, 7, 10, 9, 14, 4, 11, 8, 5, 0, 6, 13, 3, 2, 12]    # 40
    # p1 = [1, 7, 8, 10, 6, 9, 15, 14, 13, 3, 0, 4, 11, 5, 12, 2]    # 40
    # p1 = [5, 6, 4, 12, 11, 14, 9, 1, 0, 3, 8, 15, 10, 7, 2, 13]    # 40
    open_dic = {}  # 记录已经出现过的节点
    close_dic = {}  # 记录已经出现过的节点
    other = []  # find, t0
    i = 0
    while i < 1:
        i += 1
        open_dic.clear()
        close_dic.clear()
        other.clear()
        c0 = get_msg(p1, 0, 0)
        open_dic[c0[1]] = c0
        A_star(open_dic, close_dic, other)
    time2 = time.time()

    if other[0]:
        print("have answer!")
        out_answer(close_dic)
        print("all puzzles", len(open_dic)+len(close_dic), other[1])  # 输出节点的总个数
        print("Used Time %f" % (time2 - time1), "sec")
    else:
        print("no answer!")


if __name__ == '__main__':
    main()


