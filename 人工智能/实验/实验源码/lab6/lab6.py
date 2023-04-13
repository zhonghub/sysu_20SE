def main():
    words = set()   # 用于记录训练集中出现过的单词
    clause = []     # 用于记录train.txt
    emotion_clause = [0, 0, 0, 0, 0, 0, 0]  # [1:6]用于记录每种emotion的句子数量
    emotion_word = [0, 0, 0, 0, 0, 0, 0]    # 记录每种emotion的句子的单词总数
    emotion_word_num = [0, {}, {}, {}, {}, {}, {}]  # 用于记录每种emotion中各个单词出现的次数
    for line in open("Classification/train.txt", "r"):  # 读入train.txt到列表clause中
        data = line[:]
        str_list = data.split()     # 字符串转化成列表
        clause.append(str_list)  # 将每一行文件加入到列表clause中

    for i in range(1, len(clause)):     # 对clause进行处理
        ei = int(clause[i][1])
        emotion_clause[ei] += 1     # emotion[ei]的句子总数+1
        for j in range(3, len(clause[i])):
            emotion_word[ei] += 1   # emotion[ei]的单词总数+1
            words.add(clause[i][j])     # 使用集合将该单词加入到总的单词中
            if clause[i][j] in emotion_word_num[ei]:    # 如果单词clause[i][j]出现在emotion_word_num[ei]中
                emotion_word_num[ei][clause[i][j]] += 1
            else:
                emotion_word_num[ei][clause[i][j]] = 1

    all_clause = len(clause)-1      # 训练集句子总数
    dif_words = len(words)      # 不同单词数
    test = []
    for line2 in open("Classification/test.txt", "r"):  # 读取测试集到test中
        data = line2[:]
        str_list = data.split()
        test.append(str_list)

    right = 0   # 记录正确的结果数目
    for i in range(1, len(test)):   # 逐个进行测试
        p_i = [0,0,0,0,0,0,0]
        laplas = 13.7
        for ei in range(1,7):   # 对每种情绪的概率进行计算
            p_all = emotion_clause[ei]/all_clause   # 初始概率为该情绪在训练集中的测试样例
            for j in range(3, len(test[i])):
                if test[i][j] in emotion_word_num[ei]:  # 乘以各个单词在该情绪的训练集中的条件概率，采用贝叶斯估计
                    p_all *= (emotion_word_num[ei][test[i][j]] + laplas) / (emotion_word[ei] + laplas * dif_words)
                else:
                    p_all *= laplas / (emotion_word[ei] + laplas * dif_words)
            p_i[ei] += p_all
        key = 0
        max_pi = 0
        for t3 in range(1, 7):  # 选出最大概率的情绪
            if p_i[t3] > max_pi:
                max_pi = p_i[t3]
                key = t3    # 获得最大概率对应的情绪的序号
        if key == int(test[i][1]):  # 如果与正确结果相同
            right += 1
        test[i].append(key)     # 在测试的句子末尾加入该结果，方便观察
        print(test[i])
    print(right/(len(test)-1))  # 输出正确率


if __name__ == '__main__':
    main()