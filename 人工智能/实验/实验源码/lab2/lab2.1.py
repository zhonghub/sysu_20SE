import copy  # 用于深拷贝


class Clause:       # 单个谓词的类 如 ~L(a,bb,y) -> ['~L','a','bb','y']
    element = []   # [0]谓词名(含~号)如~L, [1:]变量名 如 a , bb , y

    def __init__(self):
        self.element = []

    def __init__(self, str1):
        self.element = []
        if str1[0] == ',':
            str1 = str1[1:]
        s0 = ""
        for i in range(len(str1)):
            s0 += str1[i]
            if str1[i] == '(' or str1[i] == ',' or str1[i] == ')':
                self.element.append(s0[0:-1])
                s0 = ""

    def __del__(self):
        self.element = []

    def create(self, str1):
        if str1[0] == ',':
            str1 = str1[1:]
        s0 = ""
        for i in range(len(str1)):
            s0 += str1[i]
            if str1[i] == '(' or str1[i] == ',' or str1[i] == ')':
                self.element.append(s0[0:-1])
                s0 = ""

    def create2(self, list2):
        for i in range(len(list2)):
            self.element.append(list2[i])

    def change_name(self, old_name0, new_name0):
        for i in range(len(old_name0)):
            j = 1
            while j < len(self.element):
                if self.element[j] == old_name0[i]:
                    self.element[j] = new_name0[i]
                j = j + 1

    def size(self):
        return len(self.element)

    def clear(self):
        self.element = []

    def pre(self):      # 返回谓词的前缀是否为"¬"
        return self.element[0][0] == "¬"

    def getname(self):      # 返回谓词名称
        if self.pre():
            return self.element[0][1:]
        else:
            return self.element[0]

    def get_pre_name(self):
        return self.element[0]


# ¬
def main():
    clause_set = []
    print("Please enter a clause set")
    clause0 = input()  # 读入一个子句 ，如(A(x),B(a,z),PPT(s,b)) 或 A(x)
    i = 0
    while clause0 != "":
        clause_set.append([])   # 加入一个空列表用于记录第i个子句，该列表的元素为谓词公式类Clause的变量
        if clause0[0] == '(':   # 去掉最外边的括号(如果有的话)
            clause0 = clause0[1:-1]
        str0 = ""              # 用于记录一个谓词公式,如 ",~B(a,z)" 最开头的“,”在create函数里消去
        for j in range(len(clause0)):
            if clause0[j] == " ":  # 跳过空格
                continue
            str0 += clause0[j]
            if clause0[j] == ')':   # 用')'作为结尾分割成多个谓词公式
                clause1 = Clause(str0)  # 创造一个谓词公式类Clause的变量
                # A.create(str0)
                clause_set[i].append(clause1)   # 加入到子句集的第i个子句中
                str0 = ""
        i = i + 1   # i == len(clause_set)-1
        clause0 = input()

    for i in range(len(clause_set)):    # 输出子句集，判断前面对子句集的记录是否正确
        for j in range(len(clause_set[i])):
            print(clause_set[i][j].element, end="")
        print("")
    # print(len(clause_set))

    last_end = []    # 用于记录上一次while循环开始的子句集中子句的数目，作为下次while循环单位词子句第二重for循环开始的位置
    for i in range(len(clause_set)):
        last_end.append(0)
    keep = True
    while keep:
        for i in range(len(clause_set)):
            if not keep:
                break
            if len(clause_set[i]) == 1:     # clause_set[i]只有一个谓词的子句
                for j in range(last_end[i], len(clause_set)):     # clause_set[j]超过一个谓词的取或的子句
                    last_end[i] = len(clause_set)
                    if not keep:
                        break
                    if i == j:
                        continue
                    old_name = []   # 用于记录换名前后的变量名称
                    new_name = []
                    key = -1    # key等于-1时表示该子句的同名谓词不能进行消去
                    for k in range(len(clause_set[j])):     # 在子句clause_set[j]中找相同的谓词，位置为key，可以消去
                        if clause_set[i][0].getname() == clause_set[j][k].getname() \
                                and clause_set[i][0].pre() != clause_set[j][k].pre():
                            key = k
                            for t in range(len(clause_set[j][k].element)-1):    # 找到可以换名的
                                if len(clause_set[j][k].element[t+1]) == 1 or len(clause_set[i][0].element[t+1]) == 1:
                                    old_name.append(clause_set[j][k].element[t+1])
                                    new_name.append(clause_set[i][0].element[t+1])
                                elif clause_set[j][k].element[t+1] != clause_set[i][0].element[t+1]:
                                    key = -1
                                    break
                            break
                    if key == -1:
                        continue
                    new_clause = []     # 记录 换名，消去 后生成的新子句
                    for k in range(len(clause_set[j])):
                        if k != key:
                            A = Clause("sb")
                            A.create2(clause_set[j][k].element)
                            A.change_name(old_name, new_name)
                            new_clause.append(A)
                    if len(new_clause) == 1:    # 此处判断为判断是否生成了一个已经存在的子句
                        for j2 in range(len(clause_set)):
                            if len(clause_set[j2]) == 1 and new_clause[0].element == clause_set[j2][0].element:
                                key = -1
                                break
                    if key == -1:
                        continue
                    clause_set.append(new_clause)   # 生成的新的子句加入的子句集中
                    last_end.append(0)
                    print(len(clause_set), end=":   ")  # 输出相关信息如 R[A1= 1 ,A2= 6 a ](x = tony,)
                    c = chr(key+97)
                    print("R[A1=", i+1, ",A2=", j+1, c, "]", end="(")
                    for i2 in range(len(old_name)):
                        print(old_name[i2], "=", new_name[i2], end=",")
                    print(")  ", end="")
                    i1 = len(clause_set)-1
                    if len(clause_set[i1]) == 0:
                        print("   []")
                    for j1 in range(len(clause_set[i1])):   # 输出该新子句
                        print(clause_set[i1][j1].element, end="")
                    print("")
                    if len(new_clause) == 0:    # 进行结束判断: 若有两句互斥的单谓词子句(需考虑换名)，则产生空子句
                        keep = False
                        break

            else:
                for i in range(len(clause_set)):
                    for j in range(len(clause_set)):
                        key2 = -1
                        if i != j and len(clause_set[i]) == len(clause_set[j]):
                            for k in range(len(clause_set[i])):
                                if clause_set[i][k].element == clause_set[j][k].element:
                                    # 这步只是粗略判断，事实上应进一步考虑各种可进行变量换名的情况
                                    continue
                                elif clause_set[i][k].getname() == clause_set[j][k].getname()\
                                        and clause_set[i][k].element[1:] == clause_set[j][k].element[1:]:
                                    # 需要在这里判断变量换名的情况
                                    if key2 != -1:  # 表明已经存在一处不等的情况，无法使用该规则进行消除
                                        key2 = -1
                                        break
                                    key2 = k
                                else:
                                    key2 = -1
                                    break
                        if key2 == -1:
                            continue
                        new_clause = []
                        for k in range(len(clause_set[i])):
                            if k != key2:
                                A = Clause("sb")
                                A.create2(clause_set[j][k].element)
                                new_clause.append(A)
                        if len(new_clause) == 1:  # 此处判断为判断是否生成了一个已经存在的子句
                            for j2 in range(len(clause_set)):
                                if len(clause_set[j2]) == 1 and new_clause[0].element == clause_set[j2][0].element:
                                    key2 = -1
                                    break
                        if key2 == -1:
                            continue
                        clause_set.append(new_clause)
                        last_end.append(0)
                        print(len(clause_set), end=":   ")  # 输出相关信息如 R[A1= 1 ,A2= 6 a ](x = tony,)
                        c = chr(key2 + 97)
                        print("R[A1=", i + 1, c, ",A2=", j + 1, c, "]", end="()")
                        i1 = len(clause_set) - 1
                        for j1 in range(len(clause_set[i1])):  # 输出该新子句
                            print(clause_set[i1][j1].element, end="")
                        print("")

    print("end")


if __name__ == '__main__':
    main()

"""
On(aa,bb) 
On(bb,cc)
Green(aa)
¬Green(cc)
(¬On(x,y),¬Green(x),Green(y))

GradStudent(sue)
(¬GradStudent(x), Student(x))
(¬Student(x),HardWorker(x))
¬HardWorker(sue)

A(tony)
A(mike)
A(john)
L(tony, rain)
L(tony, snow)
(¬A(x), S(x), C(x))
(¬C(y), ¬L(y, rain))
(L(z, snow), ¬S(z))
(¬L(tony, u), ¬L(mike, u))
(L(tony, v), L(mike, v))
(¬A(w), ¬C(w), S(w))

只用单谓词子句去消除没有用到规则 (~A,B)and(A,B) <=> B
测试样例：
(L(tony, u), ¬La(mike, u))
(L(tony, u), La(mike, u))
(¬L(tony, u),A(map))
(¬L(tony, u),¬A(map))
2.0过不了，而升级版2.1可以过，
(L(tony, ufo), ¬L0(mike, aa))
(L(tony, ufo), L0(mike, aa))
(¬L(tony, ufo),A(map))
(¬L(tony, ufo),¬A(x))

A(x)
¬A(map)

"""
