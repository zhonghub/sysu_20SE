import copy
import time
import heapq
d_xy = [[0, 1, 0, -1], [1, 0, -1, 0]]   # 改变方向对bfs广度优先没什么影响，但对dfs深度优先影响很大
# d_xy = [[1, 0, -1, 0], [0, -1, 0, 1]]
goal = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]


class Puzzle:
    father = -1
    data = []
    last_key = 0
    key_0 = 0   # 记录0的位置，x0 = key_0%4 , y0 = key_0 // 4 , 每次移动swap(0,i); key = x + y*4
    f_x = 0      # 代价函数，f(x)=h(x)+g(x)
    g_x = 0     # 深度
    h_x = 0     # 启发函数

    def __init__(self):
        self.data = []

    def creat_list(self, list1, last, g_x1):
        self.g_x = g_x1
        self.last_key = last
        self.data = copy.deepcopy(list1[:])
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
        self.h_x = num      # h(x)
        self.f_x = num + self.g_x    # h(x)+g(x)

    def next(self):
        x0 = self.key_0 % 4
        y0 = self.key_0 // 4
        next_key = []
        for i in range(4):
            x = x0 + d_xy[0][i]
            y = y0 + d_xy[1][i]
            if 0 <= x <= 3 and 0 <= y <= 3:
                key = x + y * 4
                if key != self.last_key:
                    next_key.append(key)
        return next_key


def is_in(puzzle, list1):
    for i in range(len(list1)):  # 可用二分查找法
        if puzzle.data == list1[i].data:
            return i
    return -1


# def A_star(open_list, close_list):


def main():
    print("start A*:")
    p1 = Puzzle()
    p1.creat_list([1, 2, 4, 8, 5, 7, 11, 10, 13, 15, 0, 3, 14, 6, 9, 12], -1, 0)
    # p1.creat_list([5, 1, 3, 4, 2, 7, 8, 12, 9, 6, 11, 15, 0, 13, 10, 14], -1, 0)
    # p1.creat_list([14, 10, 6, 0, 4, 9, 1, 8, 2, 3, 5, 11, 12, 13, 7, 5], -1, 0)
    # p1.creat_list([6, 10, 3, 15, 14, 8, 7, 11, 5, 1, 0, 2, 13, 12, 9, 4], -1, 0)

    # p1.creat_list([5, 6, 4, 12, 11, 14, 9, 1, 0, 3, 8, 15, 10, 7, 2, 13], -1 , 0)
    open_list = []
    close_list = []
    open_list.append(p1)

    find = False
    t0 = 0
    time1 = time.time()
    while True:
        p2 = copy.deepcopy(open_list[0])
        key0 = p2.key_0
        list0 = p2.next()
        for i0 in range(len(list0)):
            new_list = copy.deepcopy(p2.data)   # 进行移动，即交换0与周围的位置
            tp = new_list[list0[i0]]
            new_list[list0[i0]] = new_list[key0]
            new_list[key0] = tp
            p3 = Puzzle()
            p3.creat_list(new_list, p2.key_0, p2.g_x+1)        # 生成p3

            a = is_in(p3, open_list)
            b = is_in(p3, close_list)
            if a != -1:
                if p3.f_x < open_list[a].f_x:
                    open_list[a].f_x = p3.f_x
                    open_list[a].g_x = p3.g_x
                    open_list[a].h_x = p3.h_x
            if a == -1 and b == -1:
                p3.father = len(close_list)
                t0 += 1
                open_list.append(p3)
                if p3.h_x == 0:     # 目标状态
                    find = True
                    open_list.pop(0)
                    close_list.append(copy.deepcopy(p2))
                    close_list.append(copy.deepcopy(p3))
                    break
            """for i in range(2, len(open_list)):   # 可使用优先队列，小根堆实现
                if open_list[i].f_x < open_list[i-1].f_x:
                    temp = copy.deepcopy(open_list[i])
                    open_list[i] = open_list[i-1]
                    open_list[i-1] = temp"""
        for i in range(len(open_list)-1):
            for j in range(len(open_list)-i-1):
                if open_list[j].f_x > open_list[j + 1].f_x:
                    temp = open_list[j]
                    open_list[j] = open_list[j + 1]
                    open_list[j + 1] = temp
        open_list.pop(0)
        if find or len(open_list) == 0:
            break
        close_list.append(copy.deepcopy(p2))

    time2 = time.time()
    f = len(close_list)-1
    the_way = []
    while True:     # 回溯找关键路径
        the_way.append(close_list[f])
        f = close_list[f].father
        if f == -1:
            break
    t = len(the_way)
    for k in range(t):  # 输出关键路径
        print("move", k, the_way[t-k-1].h_x)
        print(the_way[t-k-1].data[0:4], the_way[t-k-1].data[4:8], the_way[t-k-1].data[8:12], \
              the_way[t-k-1].data[12:], sep="\n")
        print("")
    print("all puzzles", len(open_list)+len(close_list), t0+1)
    print("Used Time %f" % (time2 - time1), "sec")


if __name__ == '__main__':
    main()


