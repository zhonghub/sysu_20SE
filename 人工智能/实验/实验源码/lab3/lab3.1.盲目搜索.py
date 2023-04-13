import time
# d_xy = [[0, 0, 1, -1], [-1, 1, 0, 0]] # 改变方向对bfs广度优先没什么影响，但对dfs深度优先影响很大
d_xy = [[1, 0, -1, 0], [0, -1, 0, 1]]


# 栈和队列共用一个类，使用时调用不同函数，栈使用pop，top；队列使用dequeue，front，其余push，empty，size共用
class StackAndQueue:
    data = []

    def __init__(self):
        self.data = []

    def push(self, element):
        self.data.append(element)

    def dequeue(self):  # 出队,队首出队，如果用切片操作是生成一个新列表self.data = self.data[1:]
        self.data.pop(0)

    def pop(self):      # 出栈，栈顶出栈,如果用切片操作是生成一个新列表self.data = self.data[:-1]
        self.data.pop(self.size()-1)

    def empty(self):
        return len(self.data) == 0

    def top(self):  # 栈顶
        return self.data[-1]

    def front(self):    # 队首
        return self.data[0]

    def size(self):
        return len(self.data)


def dfs(sx, sy, ex, ey, near_x, near_y, data, ready, father):   # 使用栈中的top，pop函数
    for i in range(4):
        x = sx + d_xy[0][i]
        y = sy + d_xy[1][i]
        if data[x][y] != '1' and ready[x][y] == 1:
            ready[x][y] = 0
            near_x.push(x)
            near_y.push(y)
            father[x][y] = [sx, sy]
            if ready[ex][ey] == 0:      # dfs找到的路径就是在栈中
                return
            dfs(x, y, ex, ey, near_x, near_y, data, ready, father)
            if ready[ex][ey] == 0:      # dfs找到的路径就是在栈中
                return
            near_x.pop()
            near_y.pop()
    return


def ids(sx, sy, ex, ey, near_x, near_y, data, ready, depth, max_depth, high_x, high_y, father):   # 迭代加深，使用栈中的top，pop函数
    if depth == max_depth:      # 使用队列记录当前最大深度的节点
        high_x.push(sx)
        high_y.push(sy)
        return
    for i in range(4):
        x = sx + d_xy[0][i]
        y = sy + d_xy[1][i]
        if data[x][y] != '1' and ready[x][y] == 1:
            ready[x][y] = 0
            near_x.push(x)      # dfs用栈
            near_y.push(y)
            father[x][y] = [sx, sy]
            if ready[ex][ey] == 0:      # 用 father[x][y] = [sx,sy]
                return
            ids(x, y, ex, ey, near_x, near_y, data, ready, depth+1, max_depth,  high_x, high_y, father)
            near_x.pop()
            near_y.pop()
    if near_x.empty():      # 如果在当前深度没找到目标位置，逐个再对最大深度节点进行ids
        if not high_x.empty():
            x = high_x.front()
            y = high_y.front()
            high_x.dequeue()
            high_y.dequeue()
            ids(x, y, ex, ey, near_x, near_y, data, ready, 0, max_depth, high_x, high_y, father)
    return


def bfs(sx, sy, ex, ey, near_x, near_y, data, ready, father):   # 使用队列中的dequeue，front函数
    ready[sx][sy] = 0
    for i in range(4):
        x = sx + d_xy[0][i]
        y = sy + d_xy[1][i]
        if data[x][y] != '1' and ready[x][y] == 1:
            ready[x][y] = 0     # 用 father[x][y] = [sx,sy]
            father[x][y] = [sx, sy]
            if ready[ex][ey] == 0:
                return
            near_x.push(x)
            near_y.push(y)
    if near_x.empty():
        return
    new_x = near_x.front()
    new_y = near_y.front()
    near_x.dequeue()
    near_y.dequeue()
    bfs(new_x, new_y, ex, ey, near_x, near_y, data, ready, father)
    return


def bilateral(near_x1, near_y1, near_x2, near_y2, data, ready, ready1, ready2, is_find, father):     # 双向搜索
    sx = near_x1.front()    # 使用队列，双向都是bfs
    sy = near_y1.front()
    near_x1.dequeue()
    near_y1.dequeue()
    if data[sx][sy] == '1':     # 这句条件应该没用，处于两个队列中的(sx,sy)都是可达的
        return
    if ready1[sx][sy] == 0 and ready2[sx][sy] == 0:     # 这句一般没用，一般都是在产生一个新的可达点进行判断
        return
    for i in range(4):
        x = sx + d_xy[0][i]
        y = sy + d_xy[1][i]
        if data[x][y] != '1' and ready1[x][y] == 1:     # 未到达过的可达点
            ready1[x][y] = 0
            ready[x][y] = 0
            if ready1[x][y] == 0 and ready2[x][y] == 0:     # 如果从两个点出发都能到达该点，说明连通
                is_find[0] = True
                is_find[1] = x       # 这种情况不用令用 father[x][y] = [sx,sy]，分别从两个点回溯路径
                is_find[2] = y
                is_find[3] = sx
                is_find[4] = sy
                return
            # 用 father[x][y] = [sx,sy]
            father[x][y] = [sx, sy]
            near_x1.push(x)
            near_y1.push(y)
    if near_x1.empty() or near_x2.empty():     # 如果满足该条件，说明这两个点之间是不连通的，直接返回
        return
    bilateral(near_x2, near_y2, near_x1, near_y1, data, ready, ready2, ready1, is_find, father)  # 交换位置，从另一个点开始搜索
    return


def out_answer(temp, sx, sy, ex, ey):
    for i in range(len(temp)):     # 输出路径上的所有点
        for j in range(len(temp[i])):
            if i == 0 or j == 0 or i == len(temp)-1 or j == len(temp[i])-1:   # 边界
                print("1", end="", sep="")
            elif i == sx and j == sy:
                print("S", end="", sep="")
            elif i == ex and j == ey:
                print("E", end="", sep="")
            elif temp[i][j] != 1:
                print(temp[i][j], end="", sep="")
            else:
                print(" ", end="", sep="")
        print("")
    return


def main():
    data = []   # 用于记录图
    sx, sy, ex, ey = -1, -1, -1, -1
    for line in open("d:\桌面文件\pythonAI\lab3\MazeData.txt", "r"):  # 设置文件对象并读取每一行文件
        data.append(line[:-1])  # 将每一行文件加入到列表data中
        i = len(data)-1
        for j in range(len(data[i])):  # 找到起点和终点的位置
            if data[i][j] == "E":
                ex = i
                ey = j
            if data[i][j] == "S":
                sx = i
                sy = j
    time1 = time.time()
    len_x = len(data)
    len_y = len(data[0])
    # print(len_x, len_y)
    print("S=(", sx, ",", sy, ")  E=(", ex, ",", ey, ")", sep="")   # 输出起点，终点的位置

    ready = []      # 记录所有从起点出发可到达的点
    the_way = []    # 记录从起点出发到终点的路径上的点
    father = []  # 用于记录某点的父亲节点是谁，如father[x][y] = [fx][fy] ,表示是从(fx,fy)出发访问到(x,y)
    for i in range(len_x):
        item = [1] * len_y
        ready.append(item)
        the_way.append(item[:])
        item2 = [[]] * len_y
        father.append(item2)
    ready[sx][sy] = 0   # 记录所有从起点出发可到达的点，初始状态令起点S位置为0，表示S可达

    near_x, near_y = StackAndQueue(), StackAndQueue()    # 用于记录未访问的可达点的x,y坐标，依据bfs或dfs选择使用栈或队列
    high_x, high_y = StackAndQueue(), StackAndQueue()    # 用于记录ids中处于最大深度的可达点的x,y坐标，使用队列
    # 选择搜索方法：
    # ids(sx, sy, ex, ey, near_x, near_y, data, ready, 0, 10, high_x, high_y, father)
    # dfs(sx, sy, ex, ey, near_x, near_y, data, ready, father)
    # bfs(sx, sy, ex, ey, near_x, near_y, data, ready, father)
    a, b = ex, ey
    while len(father[ex][ey]) != 0:      # 从终点出发回溯路径上的点
        if a == sx and b == sy:
            break
        the_way[a][b] = 0
        fa = father[a][b][0]
        fb = father[a][b][1]
        a, b = fa, fb

    near_x1, near_y1, near_x2, near_y2 = StackAndQueue(), StackAndQueue(), StackAndQueue(), StackAndQueue()
    ready1, ready2 = [], []
    for i in range(len_x):
        item = [1] * len_y
        ready1.append(item)
        item2 = item[:]
        ready2.append(item2)
    ready1[sx][sy] = 0
    ready2[ex][ey] = 0  # 初始状态令起点S位置为0，表示S可达
    near_x1.push(sx)
    near_y1.push(sy)
    near_x2.push(ex)
    near_y2.push(ey)
    is_find = [False, sx, sy, ex, ey]
    #   双向搜索
    bilateral(near_x1, near_y1, near_x2, near_y2, data, ready, ready1, ready2, is_find, father)

    for i in range(2):      # 从交点向两端回溯路径
        a, b = is_find[2*i+1], is_find[2*i+2]
        while True:
            if a == sx and b == sy or a == ex and b == ey:
                break
            the_way[a][b] = 0
            fa = father[a][b][0]
            fb = father[a][b][1]
            a, b = fa, fb
    time2 = time.time()
    if ready[ex][ey] == 0 or is_find[0]:
        print("reachable")
        if is_find[0]:
            print("交点: ",is_find[1], is_find[2])   # 输出双向搜索中相交点的位置
    else:
        print("not reachable")
    print("Used Time %f" % (time2 - time1), "sec")
    temp = the_way[:]   # 关键路径上的点
    # temp = ready[:]   # 所有到达过的节点
    out_answer(temp, sx, sy, ex, ey)


if __name__ == '__main__':
    main()
