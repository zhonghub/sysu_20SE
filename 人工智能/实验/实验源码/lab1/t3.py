# 帕斯卡三角形： data_n[i] = data_n-1[i-1]+data_n-1[i] , i-1或i越过[0，n-2]的界时取0
num = int(input("Enter the number: "))
list1 = []  # 空列表
for i in range(num):
    list1.append([])
    list1[i].append(1)
    for j in range(1, i):
        list1[i].append(list1[i - 1][j - 1] + list1[i - 1][j])
    if num != 0:
        list1[i].append(1)
for i in range(num):
    print("[1", end="")
    for j in range(1, i+1):
        print(", ", list1[i][j], end="", sep="")
    print("]")
