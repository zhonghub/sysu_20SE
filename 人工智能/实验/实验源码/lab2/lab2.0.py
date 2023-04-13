import copy  # 用于深拷贝


class Clause:
    element = []   # [0]谓词名 [1及之后]变量名 如~L(a,b,y)

    def __init__(self):
        self.element = []

    """    def __init__(self, str1):
            if str1[0] == ',':
                str1 = str1[1:]
            s0 = ""
            for i in range(len(str1)):
                s0 += str1[i]
                if str1[i] == '(' or str1[i] == ',' or str1[i] == ')':
                    self.element.append(s0[0:-1])
                    s0 = ""
    """
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
if __name__ == '__main__':
    clause_set = []
    print("Please enter a clause set")
    clause0 = input()
    i = 0
    while clause0 != "":
        clause_set.append([])
        if clause0[0] == '(':
            clause0 = clause0[1:-1]
        str0 = ""
        for j in range(len(clause0)):
            if clause0[j] == " ":
                continue
            str0 += clause0[j]
            if clause0[j] == ')':   # 分割谓词公式
                A = Clause()
                A.create(str0)
                clause_set[i].append(A)
                str0 = ""
        i = i + 1
        clause0 = ""
        clause0 = input()

    for i in range(len(clause_set)):
        for j in range(len(clause_set[i])):
            print(clause_set[i][j].element,end="")
        print("")
    # print(len(clause_set))

    last_end = []  # 用于记录上一次while循环开始的子句集中子句的数目，作为下次while循环单位词子句第二重for循环开始的位置
    for i in range(len(clause_set)):
        last_end.append(0)
    keep = True
    while keep:
        for i in range(len(clause_set)):
            # print("i=", i)
            if not keep:
                break
            if len(clause_set[i]) == 1:     # clause_set[i]只有一个谓词的子句
                for j in range(last_end[i], len(clause_set)):     # clause_set[j]超过一个谓词的取或的子句
                    last_end[i] = len(clause_set)
                    if not keep:
                        break
                    if i == j:
                        continue
                    old_name = []
                    new_name = []
                    key = -1
                    for k in range(len(clause_set[j])):     # 在子句clause_set[j]中找相同的谓词，位置为key，可以消去
                        if clause_set[i][0].getname() == clause_set[j][k].getname() \
                                and clause_set[i][0].pre() != clause_set[j][k].pre():
                            key = k
                            for t in range(len(clause_set[j][k].element)-1):
                                if len(clause_set[j][k].element[t+1]) == 1 or len(clause_set[i][0].element[t+1]) == 1:
                                    old_name.append(clause_set[j][k].element[t+1])
                                    new_name.append(clause_set[i][0].element[t+1])
                                elif clause_set[j][k].element[t+1] != clause_set[i][0].element[t+1]:
                                    key = -1
                                    break
                            break
                    if key == -1:
                        continue
                    new_clause = []
                    for k in range(len(clause_set[j])):
                        if k != key:
                            A = Clause()
                            A.create2(clause_set[j][k].element)
                            A.change_name(old_name, new_name)
                            new_clause.append(A)
                    if len(new_clause) == 0:
                        continue
                    if len(new_clause) == 1:
                        for j2 in range(len(clause_set)):  # clause_set[j]超过一个谓词的取或的子句
                            if len(clause_set[j2]) == 1 and new_clause[0].element == clause_set[j2][0].element:
                                key = -1
                                break
                    if key == -1:
                        continue
                    clause_set.append(new_clause)
                    last_end.append(0)
                    print(len(clause_set), end=":   ")
                    c = chr(key+97)
                    print("R[A1=", i+1, ",A2=", j+1, c, "]", end="(")
                    for i2 in range(len(old_name)):
                        print(old_name[i2], "=", new_name[i2], end="")
                        if i2<len(old_name)-1:
                            print(" ,", end="")
                    print(")  ", end="")
                    i1 = len(clause_set)-1
                    for j1 in range(len(clause_set[i1])):
                        print(clause_set[i1][j1].element, end="")
                    print("")
                    if len(new_clause) == 1:
                        for j2 in range(len(clause_set)-1):  # clause_set[j]超过一个谓词的取或的子句
                            if len(clause_set[j2]) == 1 and new_clause[0].getname() == clause_set[j2][0].getname() \
                                    and new_clause[0].element[1:] == clause_set[j2][0].element[1:] \
                                    and new_clause[0].pre() != clause_set[j2][0].pre():
                                print("Last: [A1=", j2+1, "A2=", len(clause_set), "]():  []")
                                keep = False
                                break

print("end")

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

以上三个测试样例用2.0都能过，只用到规则1： (A)and(¬A,B,C,...) => (B,C,...)
只用单谓词子句去消除而没有用到规则2  (¬A,B,C,...)and(A,B,C,...) => (B,C,...)
2.0对于以下测试样例过不了（必须要用到规则2的）：
测试样例：

(L(tony, u), ¬L(mike, u))
(L(tony, u), L(mike, u))
(¬L(tony, u),A(map))
(¬L(tony, u),¬A(map))

(L(tony, ufo), ¬L0(mike, aa))
(L(tony, ufo), L0(mike, aa))
(¬L(tony, ufo),A(map))
(¬L(tony, ufo),¬A(x))
#这种情况可以消除

A(x)
¬A(map)
还有问题,2.1令map=x,2.2改正为 x = map 

"""
