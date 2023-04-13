class Clause:  # 单个谓词的类 如 ~L(a,bb,y) -> ['~L','a','bb','y']
    element = []  # [0]谓词名(含~号)如~L, [1:]变量名 如 a , bb , y

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

    def pre(self):  # 返回谓词的前缀是否为"¬"
        return self.element[0][0] == "¬"

    def getname(self):  # 返回谓词名称
        if self.pre():
            return self.element[0][1:]
        else:
            return self.element[0]

    def get_pre_name(self):     # 返回全称
        return self.element[0]


def out_clause(new_clause):
    if len(new_clause) > 1:
        print("(", end="")
    for j1 in range(len(new_clause)):  # 输出该新子句
        print(new_clause[j1].element[0], end="(", sep="")
        for j2 in range(1, len(new_clause[j1].element)):
            print(new_clause[j1].element[j2], end="")
            if j2 < len(new_clause[j1].element) - 1:
                print(",", end="")
        print(")", end="")
        if j1 < len(new_clause) - 1:
            print(",", end="")
    if len(new_clause) > 1:
        print(")", end="")
    if len(new_clause) > 0:
        print("")


def out_msg(key, i, j, old_name, new_name, clause_set):
    print(len(clause_set), end=":")  # 输出相关信息如 R[A1= 1 ,A2= 6 a ](x = tony,)
    c = chr(key + 97)
    print("\tR[", i + 1, end="", sep="")
    if len(new_name) == 0 and len(clause_set[i]) != 1:
        print(c, end="", sep="")
    print(", ", j + 1, end="", sep="")
    if len(clause_set[j]) != 1:
        print(c, end="", sep="")
    print("]", end="(", sep="")
    for i2 in range(len(old_name)):
        print(old_name[i2], "=", new_name[i2], end="", sep="")
        if i2 < len(old_name)-1:
            print(", ", end="")
    print(") = ", end="", sep="")


def is_break(new_clause, clause_set):
    if len(new_clause) == 0:  # 结束判断end2
        print("  []\nend2")
        return True
    if len(new_clause) == 1:  # 进行结束判断: 若有两句互斥的单谓词子句，则产生空子句
        for j2 in range(len(clause_set) - 1):  # clause_set[j]超过一个谓词的取或的子句
            if len(clause_set[j2]) == 1 and new_clause[0].getname() == clause_set[j2][0].getname() \
                    and new_clause[0].element[1:] == clause_set[j2][0].element[1:] \
                    and new_clause[0].pre() != clause_set[j2][0].pre():
                print(len(clause_set) + 1, ":\tR[", j2 + 1, ", ", len(clause_set), "]() = []\nend1", sep="")
                # keep = False
                return True
    return False


def exit_yet(new_clause, clause_set, key2):
    key = key2
    if len(new_clause) == 1:  # 此处判断为判断是否生成了一个已经存在的子句
        for j in range(len(clause_set)):
            if len(clause_set[j]) == 1 and new_clause[0].element == clause_set[j][0].element:
                key = -1
                break
    return key


# ¬
def main():
    clause_set = []
    print("Please enter a clause set")
    clause0 = input()  # 读入一个子句 ，如(A(x),B(a,z),PPT(s,b)) 或 A(x)
    i = 0
    while clause0:
        clause_set.append([])  # 加入一个空列表用于记录第i个子句，该列表的元素类型为谓词公式类Clause
        if clause0[0] == '(':  # 去掉最外边的括号(如果有的话)
            clause0 = clause0[1:-1]
        str0 = ""  # 用于记录一个谓词公式,如 ",~B(a,z)" 最开头的“,”在create函数里消去
        for j in range(len(clause0)):
            if clause0[j] == " ":  # 跳过空格
                continue
            str0 += clause0[j]
            if clause0[j] == ')':  # 用')'作为结尾分割成多个谓词公式
                clause1 = Clause(str0)  # 创造一个谓词公式类Clause的变量
                # A.create(str0)
                clause_set[i].append(clause1)  # 加入到子句集的第i个子句中
                str0 = ""
        i = i + 1  # i == len(clause_set)-1
        clause0 = input()

    for i in range(len(clause_set)):  # 输出子句集，判断前面对子句集的记录是否正确
        out_clause(clause_set[i])

    last_end = []  # 用于记录上一次while循环的第一重for循环每次结束的子句集的大小，作为下次while循环单位词子句第二重for循环开始的位置
    for i in range(len(clause_set)):
        last_end.append(0)
    keep = True
    while keep:
        last_len = len(clause_set)
        for i in range(len(clause_set)):
            if not keep:
                break
            this_start = last_end[i]    # 本次的第i子句的开始是上次第i子句的结束
            last_end[i] = len(clause_set)   # 本次的第i子句的结束是下次第i子句的开始
            if len(clause_set[i]) == 1:  # clause_set[i]只有一个谓词的子句
                for j in range(this_start, len(clause_set)):  # clause_set[j]超过一个谓词的取或的子句
                    # last_end[i] = len(clause_set)
                    if not keep:
                        break
                    if i == j:
                        continue
                    old_name = []  # 用于记录换名前后的变量名称,old_name自由变量——> new_name存在变量
                    new_name = []
                    key = -1  # key等于-1时表示该子句的同名谓词不能进行消去
                    for k in range(len(clause_set[j])):  # 在子句clause_set[j]中找相同的谓词，位置为key，可以消去
                        if clause_set[i][0].getname() == clause_set[j][k].getname() \
                                and clause_set[i][0].pre() != clause_set[j][k].pre():
                            key = k
                            for t in range(len(clause_set[j][k].element) - 1):  # 找到可以换名的变量并记录
                                if clause_set[j][k].element[t + 1] == clause_set[i][0].element[t + 1]:
                                    continue
                                if len(clause_set[j][k].element[t + 1]) == 1:
                                    old_name.append(clause_set[j][k].element[t + 1])
                                    new_name.append(clause_set[i][0].element[t + 1])
                                elif len(clause_set[i][0].element[t + 1]) == 1:
                                    old_name.append(clause_set[i][k].element[t + 1])
                                    new_name.append(clause_set[j][0].element[t + 1])
                                elif clause_set[j][k].element[t + 1] != clause_set[i][0].element[t + 1]:
                                    key = -1
                                    break
                            break
                    if key == -1:
                        continue
                    new_clause = []  # 记录 换名，消去 后生成的新子句
                    for k in range(len(clause_set[j])):     # 生成新的子句
                        if k != key:    # 对子句clause_set[j]中剩余谓词进行换名生成新子句
                            c1 = Clause("sb")
                            c1.create2(clause_set[j][k].element)
                            c1.change_name(old_name, new_name)  # 换名
                            new_clause.append(c1)
                    key = exit_yet(new_clause, clause_set, key)  # 判断是否生成一个已经存在的子句
                    if key == -1:
                        continue
                    clause_set.append(new_clause)  # 生成的新的子句加入的子句集中
                    last_end.append(0)  # 新子句遍历开始的位置为0
                    out_msg(key, i, j, old_name, new_name, clause_set)  # 输出相关信息如 R[3, 6a]
                    out_clause(new_clause)  # 输出该新子句
                    if is_break(new_clause, clause_set):
                        keep = False
                        break

            else:   # clause_set[j]超过一个谓词的取或的子句clause_set[i]
                for j in range(this_start, len(clause_set)):  # 找可使用规则2的子句clause_set(j)
                    # last_end[i] = len(clause_set)
                    key2 = -1
                    if i != j and len(clause_set[i]) == len(clause_set[j]):
                        for k in range(len(clause_set[i])):
                            if clause_set[i][k].element == clause_set[j][k].element:
                                # 这步只是粗略判断，事实上应进一步考虑各种可进行变量换名的情况
                                continue
                            elif clause_set[i][k].getname() == clause_set[j][k].getname() \
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
                            c1 = Clause("sb")
                            c1.create2(clause_set[j][k].element)
                            new_clause.append(c1)
                    key2 = exit_yet(new_clause, clause_set, key2)   # 判断是否生成一个已经存在的子句
                    if key2 == -1:
                        continue
                    clause_set.append(new_clause)
                    last_end.append(0)
                    out_msg(key2, i, j, [], [], clause_set)
                    out_clause(new_clause)  # 输出该新子句
                    if is_break(new_clause, clause_set):
                        keep = False
                        break
        if last_len == len(clause_set):
            keep = False
            print("Not True")
    print("OK!")


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

以上三个测试样例用2.0都能过，只用到规则1： (A)and(¬A,B,C,...) => (B,C,...)
只用单谓词子句去消除而没有用到规则2  (¬A,B,C,...)and(A,B,C,...) => (B,C,...)
2.0对于以下测试样例过不了（必须要用到规则2的）：

(L(tony, u), ¬L(mike, u))
(L(tony, u), L(mike, u))
(A(map), ¬L(tony, u))
(¬A(map), ¬L(tony, u))

(L(tony, ufo), ¬L0(mike, aa))
(L(tony, ufo), L0(mike, aa))
(¬L(tony, ufo),A(map))
(¬L(tony, ufo),¬A(x))

A(x)
¬A(map)
还有问题,2.1是令map=x；2.2改正为 x = map (方法：把自由变量名放前面(old_name),把改名后的存在变量名放后面(new_name))

L(tony, ufo)
¬L(tony, x)

L(tony,ufo)
¬L(tony,ufo)

(L(tony, ufo), ¬L0(mike, aa))
¬L(tony, x)
(L(tony, ufo), L0(mike, aa))

end1:通过生成的单谓词子句，找到对应的互斥子句(不考虑换名,只考虑完全从字面上互斥的子句,换名由下一次while循环考虑),生成空子句[]结束
end2:在用规则1进行消去时直接生成了一个空子句[]结束,当且仅当子句集中就已经存在两个互斥的子句
"""
