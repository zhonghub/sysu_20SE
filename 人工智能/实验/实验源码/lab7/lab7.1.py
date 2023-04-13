from sklearn.feature_extraction.text import CountVectorizer
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
    # print("train_data  ", all_y1)

    test_data = []
    for line2 in open("Classification/test.txt", "r"):  # 读取测试集
        data = line2[:]
        str_list = data.split()
        test_data.append(str_list)

    # 词袋模型，转化为词向量
    countvec = CountVectorizer(token_pattern='[\w]{1,}')  # 26,38.1%
    countvec1 = countvec.fit_transform(x1).toarray()
    # print(countvec1)

    k1 = 26
    right = 0   # 记录正确的分类结果的数目
    for i in range(1, len(test_data)):  # 对测试集中的每个句子进行分类
        list_words = test_data[i][3:]
        clause = " ".join(list_words)
        s_seg_vec = countvec.transform([clause]).toarray()  # 将测试的句子转化为词向量
        # print(s_seg_vec)
        kdd = []    # 用于记录距离
        for t in range(len(countvec1)):
            dist = np.linalg.norm(countvec1[t] - s_seg_vec)
            # 求该句子的词向量与每个测试集句子的词向量欧式距离
            heapq.heappush(kdd, [dist, y1[t]])
        num = [0, 0, 0, 0, 0, 0, 0]     # 记录最近的k个点中每种点的数量
        for k3 in range(k1):
            min = heapq.heappop(kdd)
            num[int(min[1])] += 1
        key = 1
        max_pi = 0
        for t3 in range(1, 7):  # 选出k个点中数量最多的点
            if num[t3] * all_y1[t3] > max_pi:
                max_pi = num[t3] * all_y1[t3]
                key = t3  # 获得最大概率对应的情绪的序号
        if key == int(test_data[i][1]):   # 如果与正确结果相同
            right += 1
        test_data[i].append(key)    # 在测试的句子末尾加入该分类结果，方便观察
        print(test_data[i])
    print("正确率为： ", right / (len(test_data) - 1) * 100, "%", sep="")  # 输出正确率


if __name__ == '__main__':
    main()

