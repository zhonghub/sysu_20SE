from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import heapq


def main():
    x1 = []     # 句子
    y1 = []     # 标签
    all_y1 = [0, 0, 0, 0, 0, 0, 0]

    train_data = []
    for line in open("Classification/train.txt", "r"):  # 读入train.txt到列表clause中
        data = line[:]
        str_list = data.split()     # 字符串转化成列表
        train_data.append(str_list)  # 将每一行文件加入到列表clause中
    for i in range(1, len(train_data)):
        list_words = train_data[i][3:]
        clause = " ".join(list_words)
        x1.append(clause)
        y1.append(train_data[i][1])
        all_y1[int(train_data[i][1])] += 1
    print("train_data  ", all_y1)

    test_data = []
    for line2 in open("Classification/test.txt", "r"):  # 读取测试集到test中
        data = line2[:]
        str_list = data.split()
        test_data.append(str_list)

    # countvec = TfidfVectorizer(token_pattern='[\w]{1,}')   # 63 38.8%; token_pattern='[\w]{1,}', 18,36.4%
    countvec = CountVectorizer(token_pattern='[\w]{1,}')  # 42,37.8%; token_pattern='[\w]{1,}',26,38.1%
    countvec1 = countvec.fit_transform(x1).toarray()
    # print(countvec1)

    k1 = 26
    all = [0, 0, 0, 0, 0, 0, 0]
    right = [0, 0, 0, 0, 0, 0, 0]  # 记录正确的结果数目
    for i in range(1, len(test_data)):
        list_words = test_data[i][3:]
        clause = " ".join(list_words)
        s_seg_vec = countvec.transform([clause]).toarray()
        # print(s_seg_vec)
        kdd = []
        for t in range(len(countvec1)):
            dist = np.linalg.norm(countvec1[t] - s_seg_vec)
            heapq.heappush(kdd, [dist, y1[t]])
        num = [0, 0, 0, 0, 0, 0, 0]
        for k3 in range(k1):
            min = heapq.heappop(kdd)
            num[int(min[1])] += 1
        key = 1
        max_pi = 0
        for t3 in range(1, 7):  # 选出k个点中数量最多的点
            if num[t3] * all_y1[t3] > max_pi:
                max_pi = num[t3] * all_y1[t3]  # *all_y1[t3]/(len(train_data)-1)
                key = t3  # 获得最大概率对应的情绪的序号
        all[int(test_data[i][1])] += 1
        if key == int(test_data[i][1]):  # and key != 4:  # 如果与正确结果相同
            right[key] += 1
            right[0] += 1
        # test_data[i].append(key)
        # test_data[i].append(num)  # 在测试的句子末尾加入该结果，方便观察
        # print(test_data[i])
    print(all)
    print(right)  # /(len(test)-1)*100, "%", sep="")  # 输出正确率
    print(right[0] / (len(test_data) - 1) * 100, "%", sep="")  # 输出正确率


# print(t, right / (len(test_data) - 1) * 100, "%")


if __name__ == '__main__':
    main()


# k的取值：大或者小都可能不能达到期望结果。一般情况会倾向于选择较小值，然后通过交叉验证选取最优值。