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
        self.element = []
        if str1[0] == ',':
            str1 = str1[1:]
        s0 = ""
        for i in range(len(str1)):
            s0 += str1[i]
            if str1[i] == '(' or str1[i] == ',' or str1[i] == ')':
                self.element.append(s0[0:-1])
                s0 = ""

    def create2(self, list2):
        self.element = []
        for i in range(len(list2)):
            self.element.append(list2[i])

    def change_name(self, old_name0, new_name0):    # 自由变量换名，进行合一置换
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


def out_clause(new_clause):     # 输出一个子句
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


def out_msg(key1, key2, i, j, old_name, new_name, clause_set):     # 输出合一置换的相关信息如 R[1 ,6a](x=tony) =
    print(len(clause_set), end=":")
    c1 = chr(key1 + 97)   # 将key(置换的变量的位置)转化为字符
    c2 = chr(key2 + 97)
    print("\tR[", i + 1, end="", sep="")
    if len(clause_set[i]) != 1:     # len(new_name) == 0 and
        print(c1, end="", sep="")
    print(", ", j + 1, end="", sep="")
    if len(clause_set[j]) != 1:
        print(c2, end="", sep="")
    print("]", end="(", sep="")
    for i2 in range(len(old_name)):
        print(old_name[i2], "=", new_name[i2], end="", sep="")
        if i2 < len(old_name)-1:
            print(", ", end="")
    print(") = ", end="", sep="")


# end1:每生成一个单谓词子句（单元子句）,若能找到对应的互补子句(不考虑合一置换,只考虑完全从字面上互补的子句,合一置换由下一次while循环考虑),
#        则生成空子句[]结束
# end2:在用归结原理（单元优先策略）进行归结时直接生成了一个空子句[]则结束(当且仅当子句集中就已经存在两个互补的单元子句。含合一置换后互补的)
def is_break(new_clause, clause_set):   # 判读是否结束end1/end2,
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


def mgu(clause1, clause2, key1, key2, old_name, new_name, new_clause):  # (¬A,C1)∧(A,C2) => (C1,C2)
    num = 0
    key1.clear()
    key2.clear()
    old_name.clear()
    new_name.clear()
    for i in range(len(clause1)):
        for j in range(len(clause2)):
            if clause1[i].pre() != clause2[j].pre() and clause1[i].getname() == clause2[j].getname():
                old_name.append([])
                new_name.append([])
                num += 1
                key1.append(i)
                key2.append(j)
                for k in range(len(clause1[i].element)-1):
                    t = len(old_name)-1
                    if clause1[i].element[k + 1] == clause2[j].element[k + 1]:
                        continue
                    if len(clause1[i].element[k + 1]) == 1:
                        old_name[t].append(clause1[i].element[k + 1])
                        new_name[t].append(clause2[j].element[k + 1])
                    elif len(clause2[j].element[k + 1]) == 1:
                        old_name[t].append(clause2[j].element[k + 1])
                        new_name[t].append(clause1[i].element[k + 1])
                    elif clause1[i].element[k + 1] != clause2[j].element[k + 1]:
                        num = num-1
                        key1[t] = -1
                        key2[t] = -1
                        break
                break
    new_clause.clear()
    the_key = -1
    if num == 1:
        for i in range(len(key1)):
            if key1[i] != -1:
                the_key = i
                for k1 in range(len(clause1)):
                    if k1 != key1[i]:
                        c1 = Clause("sb")
                        c1.create2(clause1[k1].element)
                        c1.change_name(old_name[i], new_name[i])
                        new_clause.append(c1)
                for k2 in range(len(clause2)):
                    if k2 != key2[i]:
                        c2 = Clause("sb")
                        c2.create2(clause2[k2].element)
                        c2.change_name(old_name[i], new_name[i])
                        yet = False
                        for j in range(len(new_clause)):    # 去除重复的谓词
                            if new_clause[j].element == c2.element:
                                yet = True
                        if not yet:
                            new_clause.append(c2)
                break
    return the_key


# ¬
def main():
    clause_set = []     # 储存子句集,clause_set[i]表示子句集中的第i个子句
    print("Please enter a clause set")
    clause0 = input()  # 读入一个子句 ，如(A(x),B(a,z),PPT(s,b)) 或 A(x)
    i = 0
    while clause0:  # 读入子句集并记录
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
    model = 1   # 用于转换归并原理的策略，model==0时使用单元优先策略，model==1时使用普遍策略
    while keep:
        last_len = len(clause_set)
        # 采用单元优先策略,先只用单元子句和其他子句进行归结，没有新子句产生时，再使用最一般的归结原则
        for i in range(len(clause_set)):
            if not keep:
                break
            this_start = last_end[i]  # 本次的第i子句的开始是上次第i子句的结束
            last_end[i] = len(clause_set)  # 本次的第i子句的结束是下次第i子句的开始
            for j in range(this_start, len(clause_set)):  # clause_set[j]超过一个谓词的取或的子句
                if not keep:
                    break
                if i >= j:  # i >= j 在普通形式时使用
                    continue
                key1, key2, old_name, new_name, new_clause = [], [], [], [], []
                the_key = mgu(clause_set[i], clause_set[j], key1, key2, old_name, new_name, new_clause)
                the_key = exit_yet(new_clause, clause_set, the_key)
                if the_key == -1:
                    continue
                clause_set.append(new_clause)
                last_end.append(0)
                if len(new_clause) == 0 and len(clause_set[i]) == 1 and len(clause_set[j]) == 1:
                    out_msg(key1[the_key], key2[the_key], i, j, old_name[the_key], new_name[the_key], clause_set)
                    # 输出相关信息如 R[3, 6a] =
                    out_clause(new_clause)  # 输出该新子句
                elif len(new_clause) == 0:
                    continue
                else:
                    out_msg(key1[the_key], key2[the_key], i, j, old_name[the_key], new_name[the_key], clause_set)
                    # 输出相关信息如 R[3, 6a] =
                    out_clause(new_clause)  # 输出该新子句
                if is_break(new_clause, clause_set):
                    keep = False
                    break
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

"""
