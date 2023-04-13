# 帕斯卡三角形： data_n[i] = data_n-1[i-1]+data_n-1[i] , i-1或i越过[0，n-2]的界时取0
num = int(input("Enter the number: "))
list1 = []  # 空列表
for i in range(num):
    list1.append([])        # 使用线性表，第i行有i个数
    list1[i].append(1)      # 每行第一个数为1
    for j in range(1, i):
        # 给每行中间非1的数赋值，i的范围为2~num-1，从第3行到最后一行，避免越界
        list1[i].append(list1[i - 1][j - 1] + list1[i - 1][j])
    if i != 0:              # 第一行只有1个数
        list1[i].append(1)  # 每行最后一个为1
for i in range(num):        # 输出每行
    print(list1[i])
