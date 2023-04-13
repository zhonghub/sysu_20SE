import copy  # 用于深拷贝


class MyList:
    mylist = []

    def __init__(self):
        self.mylist = []

    def __init__(self, list00):
        self.mylist = copy.deepcopy(list00)

    def push(self, args):
        self.mylist.append(args)

    def get(self, num):
        print(self.mylist[num])

    def len0(self):
        print(len(self.mylist))

    def del0(self):
        print(self.mylist.pop(0))

    def clear(self):
        while len(self.mylist) > 0:
            self.mylist.pop()

    def print0(self):   # 用于输出列表
        print(self.mylist)


list0 = ['sb', '2sb', '3sb']    # 以下为实例化测试
list1 = MyList(list0)   # 构造函数
list1.print0()          # 这里输出应为 ['sb', '2sb', '3sb']
list1.len0()            # len()函数，此处输出应为3
list1.push('4sb')       # push(args)函数
list1.len0()            # len()函数，应输出4
list1.print0()          # 这里输出应为 ['sb', '2sb', '3sb', '4sb']
list1.get(2)            # get(num)函数 ，应输出第2个元素(从0开始)为 3sb
list1.del0()            # del()函数 ，删除首个元素并输出，应输出 sb
list1.print0()          # 应输出 ['2sb', '3sb', '4sb']
list1.clear()           # clear()函数
list1.print0()          # 应输出[]
list1.len0()            # 应输出0





