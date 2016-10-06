# coding:utf-8


import json

import numpy as np
import numpy.linalg as la

POSITIVE = 1  # 正面词语
NEGATIVE = 2  # 反面词语
NEUTRAL = 3  # 客观词语


def load_key_words(file_path):
    with open(file_path) as fp:
        lines = fp.readlines()
        lines = [line.replace("\n", "") for line in lines]
    return lines


class DateSet:
    def __init__(self, data, label):
        self.data = np.array(data)
        self.label = label

    def Data(self):
        return self.data

    def Label(self):
        return self.label


def load_date_sets(file_path):
    with open(file_path) as f:
        data_list = json.load(f)
    temp = []
    for data in data_list:
        # 前面是特征向量，后面最后一个是标签
        label = data[-1]
        feature = data[:-1]
        d = DateSet(feature, label)
        temp.append(d)
    return temp


# 欧式距离,1表示100%，越接近0表示越不相似
def _ecl_sim(inA, inB):
    return 1.0 / (1.0 + la.norm(inA - inB))


# 皮尔逊相关系数,范围-1->+1， 越大越相似
def _pears_sim(inA, inB):
    if len(inA) < 3:
        return 1.0
    return 0.5 + 0.5 * np.corrcoef(inA, inB, rowvar=0)[0][1]


# 余弦相关范围-1->+1 越大越相似
def _cos_sim(inA, inB):
    num = float(inB * inA.T)
    de_nom = la.norm(inA) * la.norm(inB)
    return 0.5 + 0.5 * (num / de_nom)


def _get_feature(sentence, key_word):
    size = len(key_word)
    feature = [0 for _ in range(size)]
    for index in range(size):
        word = key_word[index]
        value = sentence.find(word)  # 单词最初出现的位置
        feature[index] = value
    return np.array(feature)


def get_mood(sentence, key_word, data_sets, k=30):
    feature = _get_feature(sentence, key_word)
    similars = []
    for data in data_sets:
        similar = _ecl_sim(feature, data.Data())
        similars.append(similar)
    # print(similars)
    sorted_index = np.argsort(similars).tolist()
    sorted_index.reverse()  # 从大到小后排序后取下标
    # print(sorted_index)

    size = len(sorted_index)
    cut_size = int(size * 0.8) if size < k else k  # 列表若不超过k，只能拿8成，否则每个结果的标签都一样的，导致百分比一样
    labels = [data_sets[sorted_index[i]].Label() for i in range(cut_size)]
    # print(labels)
    # print("==========")
    result = {
        "positive": labels.count(POSITIVE) / cut_size,
        "negative": labels.count(NEGATIVE) / cut_size,
        "neutral": labels.count(NEUTRAL) / cut_size
    }
    return result
