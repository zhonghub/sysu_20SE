from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
import numpy as np


def main():
    x1 = []     # 句子
    y1 = []     # 标签
    x2, y2 = [], []

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
    # print("train_data  ", all_y1)

    test_data = []
    for line2 in open("Classification/test.txt", "r"):  # 读取测试集
        data = line2[:]
        str_list = data.split()
        test_data.append(str_list)
    for i in range(1, len(test_data)):
        list_words = test_data[i][3:]
        clause = " ".join(list_words)
        x2.append(clause)
        y2.append(test_data[i][1])

    x = x1
    y = y1
    test = test_data
    # test = train_data


    # 词袋模型，转化为词向量
    countvec = CountVectorizer(token_pattern='[\w]{1,}')  # 26,38.1%
    # countvec = TfidfTransformer()  # 26,38.1%
    countvec1 = countvec.fit_transform(x).toarray()
    # tf = TfidfTransformer()
    # tfidf = tf.fit_transform(countvec1).toarray()
    # print(countvec1)
    clf = LinearSVC()  # 线性支持向量机
    clf.fit(countvec1, y)
    # clf.fit(tfidf, y)

    right = 0   # 记录正确的分类结果的数目
    for i in range(1, len(test)):  # 对测试集中的每个句子进行分类
        list_words = test[i][3:]
        clause = " ".join(list_words)
        s_seg_vec = countvec.transform([clause]).toarray()  # 将测试的句子转化为词向量
        # s_seg_vec = tf.transform(s_seg_vec).toarray()
        result = clf.predict(s_seg_vec)
        if result == test[i][1]:   # 如果与正确结果相同
            right += 1
        test[i].append(result)    # 在测试的句子末尾加入该分类结果，方便观察
        print(test[i])
    print("正确率为： ", right / (len(test) - 1) * 100, "%", sep="")  # 输出正确率


if __name__ == '__main__':
    main()

