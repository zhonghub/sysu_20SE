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
    c1 = " ".join(b1)  # 把列表转化为字符串
    return c1


def get_msg(data, last_key, g_x):
    father = '-1'
    now_str = get_str(data)  # 记录父节点的在close表中的位置key值
    # last_key = 0  # 记录父节点的状态，避免由子节点返回父节点
    key_0 = 0  # 记录0的位置，x0 = key_0%4 , y0 = key_0 // 4 , 每次移动swap(0,i); key = x + y*4
    # f_x = 0      # 估价函数，f(x)=h(x)+g(x)
    # g_x = 0  # 深度
    h_x = 0  # 启发函数,曼哈顿距离
    for i in range(16):
        if data[i] == 0:
            key_0 = i
        else:
            x1 = i % 4
            y1 = i // 4
            x2 = (data[i] - 1) % 4
            y2 = (data[i] - 1) // 4
            d = 0 if abs(x2 - x1) + abs(y2 - y1) == 0 else abs(x2 - x1) + abs(y2 - y1)
            h_x += d    # # h(x)，曼哈顿距离
    return [data[:], now_str, last_key, key_0, g_x, h_x, father]


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


def out_answer(close_dic):     # 输出关键路径, [data[:], now_str, last_key, key_0, g_x, h_x, father]
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
        print("move:", k, " g(x):", the_way[t-k-1][-3], " h(x):", the_way[t-k-1][-2], " f(x):",
              the_way[t-k-1][-3] + the_way[t-k-1][-2])
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
    heapq.heappush(open_list, [vals[0][-2]+vals[0][-3], vals[0][1]])
    while True:
        if len(open_list) == 0:
            break
        min_key = heapq.heappop(open_list)
        p2 = open_dic[min_key[1]]  # [data[:], now_str, last_key, key_0, g_x, h_x, father]

        if t0 % 100000 == 0:
            print("now puzzles", len(open_dic) + len(close_dic), t0, "g(x)", p2[-3],  "h(x)", p2[-2],
                  "f(x)", p2[-2]+p2[-3])  # 输出节点的总个数

        if p2[-2] == 0:  # 目标状态,h(x)==0
            find = True
            close_dic[p2[1]] = p2
            open_dic.pop(p2[1])
            open_list.pop(0)
            break
        list0 = get_son(p2[3], p2[2])
        for i0 in range(len(list0)):
            new_list = p2[0][:]   # 进行移动，即交换0与周围的位置
            new_list[list0[i0]], new_list[p2[3]] = new_list[p2[3]], new_list[list0[i0]]
            p3 = get_msg(new_list[:], p2[3], p2[4] + 1)
            v0 = open_dic.get(p3[1])
            if v0:  # 如果已经在open表里，判断是否需要更新
                value1 = v0[4]  # g(x)
                if p3[4] >= value1:  # 如果不是新的节点且不用更新
                    continue
                if p3[4] < value1:  # 如果不是新的节点且需要更新,有问题
                    open_dic[p3[1]][4] = p3[4]
                    open_dic[p3[1]][-1] = p2[1]
                    continue
            # 否则不在open表里
            else:
                v1 = close_dic.get(p3[1])
                if v1:  # 如果在close表里
                    value1 = v1[4]
                    if p3[4] >= value1:  # 且不用更新
                        continue
                else:   # 否则是新节点
                    t0 += 1
                p3[-1] = p2[1]  # 设置p3的父亲节点为p2,含更新
                open_dic[p3[1]] = p3  # [data[:], now_str, last_key, key_0, g_x, h_x, father]
                # 在open_list里存储[ [f_x, now_str] ,..., ...]
                heapq.heappush(open_list, [p3[-2]+p3[-3], p3[1]])
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
    p1 = [14, 10, 6, 0, 4, 9, 1, 8, 2, 3, 5, 11, 12, 13, 7, 15]  # 49
    # p1 = [6, 10, 3, 15, 14, 8, 7, 11, 5, 1, 0, 2, 13, 12, 9, 4]   # 48

    # p1 = [5, 1, 2, 4, 9, 6, 3, 8, 13, 15, 10, 11, 14, 0, 7, 12]

    # p1 = [11, 3, 1, 7, 4, 6, 8, 2, 15, 9, 10, 13, 14, 12, 5, 0]     # 56
    # all puzzles 52742392 52742392
    # Used Time 4095.339409 sec

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

"""
测试样例5：
have answer!
move: 0  g(x): 0  h(x): 34  f(x): 34
11 3  1  7  
4  6  8  2  
15 9  10 13 
14 12 5  0  

move: 1  g(x): 1  h(x): 35  f(x): 36
11 3  1  7  
4  6  8  2  
15 9  10 13 
14 12 0  5  

move: 2  g(x): 2  h(x): 34  f(x): 36
11 3  1  7  
4  6  8  2  
15 9  10 13 
14 0  12 5  

move: 3  g(x): 3  h(x): 35  f(x): 38
11 3  1  7  
4  6  8  2  
15 0  10 13 
14 9  12 5  

move: 4  g(x): 4  h(x): 34  f(x): 38
11 3  1  7  
4  6  8  2  
15 10 0  13 
14 9  12 5  

move: 5  g(x): 5  h(x): 33  f(x): 38
11 3  1  7  
4  6  8  2  
15 10 13 0  
14 9  12 5  

move: 6  g(x): 6  h(x): 32  f(x): 38
11 3  1  7  
4  6  8  2  
15 10 13 5  
14 9  12 0  

move: 7  g(x): 7  h(x): 31  f(x): 38
11 3  1  7  
4  6  8  2  
15 10 13 5  
14 9  0  12 

move: 8  g(x): 8  h(x): 30  f(x): 38
11 3  1  7  
4  6  8  2  
15 10 0  5  
14 9  13 12 

move: 9  g(x): 9  h(x): 31  f(x): 40
11 3  1  7  
4  6  0  2  
15 10 8  5  
14 9  13 12 

move: 10  g(x): 10  h(x): 30  f(x): 40
11 3  1  7  
4  6  2  0  
15 10 8  5  
14 9  13 12 

move: 11  g(x): 11  h(x): 29  f(x): 40
11 3  1  7  
4  6  2  5  
15 10 8  0  
14 9  13 12 

move: 12  g(x): 12  h(x): 28  f(x): 40
11 3  1  7  
4  6  2  5  
15 10 0  8  
14 9  13 12 

move: 13  g(x): 13  h(x): 29  f(x): 42
11 3  1  7  
4  6  2  5  
15 0  10 8  
14 9  13 12 

move: 14  g(x): 14  h(x): 30  f(x): 44
11 3  1  7  
4  0  2  5  
15 6  10 8  
14 9  13 12 

move: 15  g(x): 15  h(x): 31  f(x): 46
11 0  1  7  
4  3  2  5  
15 6  10 8  
14 9  13 12 

move: 16  g(x): 16  h(x): 30  f(x): 46
11 1  0  7  
4  3  2  5  
15 6  10 8  
14 9  13 12 

move: 17  g(x): 17  h(x): 29  f(x): 46
11 1  2  7  
4  3  0  5  
15 6  10 8  
14 9  13 12 

move: 18  g(x): 18  h(x): 28  f(x): 46
11 1  2  7  
4  0  3  5  
15 6  10 8  
14 9  13 12 

move: 19  g(x): 19  h(x): 27  f(x): 46
11 1  2  7  
0  4  3  5  
15 6  10 8  
14 9  13 12 

move: 20  g(x): 20  h(x): 26  f(x): 46
0  1  2  7  
11 4  3  5  
15 6  10 8  
14 9  13 12 

move: 21  g(x): 21  h(x): 25  f(x): 46
1  0  2  7  
11 4  3  5  
15 6  10 8  
14 9  13 12 

move: 22  g(x): 22  h(x): 24  f(x): 46
1  2  0  7  
11 4  3  5  
15 6  10 8  
14 9  13 12 

move: 23  g(x): 23  h(x): 23  f(x): 46
1  2  3  7  
11 4  0  5  
15 6  10 8  
14 9  13 12 

move: 24  g(x): 24  h(x): 22  f(x): 46
1  2  3  7  
11 0  4  5  
15 6  10 8  
14 9  13 12 

move: 25  g(x): 25  h(x): 23  f(x): 48
1  0  3  7  
11 2  4  5  
15 6  10 8  
14 9  13 12 

move: 26  g(x): 26  h(x): 24  f(x): 50
1  3  0  7  
11 2  4  5  
15 6  10 8  
14 9  13 12 

move: 27  g(x): 27  h(x): 23  f(x): 50
1  3  4  7  
11 2  0  5  
15 6  10 8  
14 9  13 12 

move: 28  g(x): 28  h(x): 22  f(x): 50
1  3  4  7  
11 2  5  0  
15 6  10 8  
14 9  13 12 

move: 29  g(x): 29  h(x): 21  f(x): 50
1  3  4  0  
11 2  5  7  
15 6  10 8  
14 9  13 12 

move: 30  g(x): 30  h(x): 20  f(x): 50
1  3  0  4  
11 2  5  7  
15 6  10 8  
14 9  13 12 

move: 31  g(x): 31  h(x): 19  f(x): 50
1  0  3  4  
11 2  5  7  
15 6  10 8  
14 9  13 12 

move: 32  g(x): 32  h(x): 18  f(x): 50
1  2  3  4  
11 0  5  7  
15 6  10 8  
14 9  13 12 

move: 33  g(x): 33  h(x): 17  f(x): 50
1  2  3  4  
11 5  0  7  
15 6  10 8  
14 9  13 12 

move: 34  g(x): 34  h(x): 18  f(x): 52
1  2  3  4  
11 5  10 7  
15 6  0  8  
14 9  13 12 

move: 35  g(x): 35  h(x): 19  f(x): 54
1  2  3  4  
11 5  10 7  
15 0  6  8  
14 9  13 12 

move: 36  g(x): 36  h(x): 18  f(x): 54
1  2  3  4  
11 5  10 7  
0  15 6  8  
14 9  13 12 

move: 37  g(x): 37  h(x): 17  f(x): 54
1  2  3  4  
0  5  10 7  
11 15 6  8  
14 9  13 12 

move: 38  g(x): 38  h(x): 16  f(x): 54
1  2  3  4  
5  0  10 7  
11 15 6  8  
14 9  13 12 

move: 39  g(x): 39  h(x): 15  f(x): 54
1  2  3  4  
5  10 0  7  
11 15 6  8  
14 9  13 12 

move: 40  g(x): 40  h(x): 14  f(x): 54
1  2  3  4  
5  10 6  7  
11 15 0  8  
14 9  13 12 

move: 41  g(x): 41  h(x): 13  f(x): 54
1  2  3  4  
5  10 6  7  
11 0  15 8  
14 9  13 12 

move: 42  g(x): 42  h(x): 12  f(x): 54
1  2  3  4  
5  10 6  7  
0  11 15 8  
14 9  13 12 

move: 43  g(x): 43  h(x): 13  f(x): 56
1  2  3  4  
5  10 6  7  
14 11 15 8  
0  9  13 12 

move: 44  g(x): 44  h(x): 12  f(x): 56
1  2  3  4  
5  10 6  7  
14 11 15 8  
9  0  13 12 

move: 45  g(x): 45  h(x): 11  f(x): 56
1  2  3  4  
5  10 6  7  
14 11 15 8  
9  13 0  12 

move: 46  g(x): 46  h(x): 10  f(x): 56
1  2  3  4  
5  10 6  7  
14 11 0  8  
9  13 15 12 

move: 47  g(x): 47  h(x): 9  f(x): 56
1  2  3  4  
5  10 6  7  
14 0  11 8  
9  13 15 12 

move: 48  g(x): 48  h(x): 8  f(x): 56
1  2  3  4  
5  10 6  7  
0  14 11 8  
9  13 15 12 

move: 49  g(x): 49  h(x): 7  f(x): 56
1  2  3  4  
5  10 6  7  
9  14 11 8  
0  13 15 12 

move: 50  g(x): 50  h(x): 6  f(x): 56
1  2  3  4  
5  10 6  7  
9  14 11 8  
13 0  15 12 

move: 51  g(x): 51  h(x): 5  f(x): 56
1  2  3  4  
5  10 6  7  
9  0  11 8  
13 14 15 12 

move: 52  g(x): 52  h(x): 4  f(x): 56
1  2  3  4  
5  0  6  7  
9  10 11 8  
13 14 15 12 

move: 53  g(x): 53  h(x): 3  f(x): 56
1  2  3  4  
5  6  0  7  
9  10 11 8  
13 14 15 12 

move: 54  g(x): 54  h(x): 2  f(x): 56
1  2  3  4  
5  6  7  0  
9  10 11 8  
13 14 15 12 

move: 55  g(x): 55  h(x): 1  f(x): 56
1  2  3  4  
5  6  7  8  
9  10 11 0  
13 14 15 12 

move: 56  g(x): 56  h(x): 0  f(x): 56
1  2  3  4  
5  6  7  8  
9  10 11 12 
13 14 15 0  """
