# coding:utf-8

# 自动根据高频词汇生成keyword

import jieba
import numpy as np
from sklearn.externals import joblib
from sklearn.naive_bayes import GaussianNB


split_tag = "----"
jieba.load_userdict("word.txt")

def load_key_words(file_path):
    with open(file_path, encoding="utf-8") as fp:
        lines = fp.readlines()
        lines = [line.replace("\n", "") for line in lines]
    return lines


def build_key_word(path):
    """
    通过词频产生key word
    :param path:
    :return:
    """
    d = {}
    with open(path, encoding="utf-8") as fp:
        for line in fp:
            for word in jieba.cut(line.strip()):
                if len(word) > 1:  # 避免大量无意义的词语进入统计范围
                    d[word] = d.get(word, 0) + 1
    kw_list = sorted(d, key=lambda x: d[x], reverse=True)
    # 取前0.5名
    size = int(len(kw_list) * 0.2)
    return kw_list[:size]


def _get_feature(sentence, key_word):
    size = len(key_word)
    feature = [0 for _ in range(size)]
    for index in range(size):
        word = key_word[index]
        value = sentence.find(word)  # 单词最初出现的位置
        if value != -1:
            feature[index] = 1
    return np.array(feature)


def get_feature(path, kw_list):
    features = []
    # lines = []
    label = []
    with open(path, encoding="utf-8") as fp:
        for line in fp:
            temp = line.strip()
            try:
                s = temp.split(split_tag)
                sentence = s[0]
                label.append(int(s[1]))
                features.append(_get_feature(sentence, kw_list))
            except Exception:
                print(temp + " error")
                continue
    return features, label


def script_run():
    # 产生keyword
    kw_list = build_key_word("train.txt")
    # 保存数据
    fp = open("new_word.txt", encoding="utf-8", mode="w")
    for word in kw_list:
        fp.write(word + "\n")
    fp.close()
   # kw_list = load_key_words("word.txt")
    feature, label = get_feature("train.txt", kw_list)
    gnb = GaussianNB()
    gnb = gnb.fit(feature, label)
    joblib.dump(gnb, 'model/gnb.model')
    print("训练完成")
    # print(feature,label)


def test(test_data, model_name):
    kw_list = load_key_words("new_word.txt")
    feature_list = []
    for data in test_data:
        feature_list.append(_get_feature(data, kw_list))
    gnb = joblib.load(model_name)
    result = gnb.predict(feature_list)
    for i in range(len(test_data)):
        print(test_data[i], "----", result[i])


if __name__ == "__main__":
    #script_run()
    test(["叼你啊", "你去吃屎啦", "我叼你啊", "萌萌哒","现在的年轻人，连点小事都做不好","想摸你屁股","默默看书"], "model/gnb.model")
