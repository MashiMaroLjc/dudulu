# usr/bin/python
# coding:utf-8
import json

import numpy as np


def load_sentence(filepath):
    """
    载入要训练的句子
    :param filepath:
    :return:
    """
    with open(filepath) as f:
        sentence = [word.replace("\n", "") for word in f.readlines()]
    return sentence


def _get_feature(sentence, key_word):
    size = len(key_word)
    feature = [0 for _ in range(size)]
    for index in range(size):
        word = key_word[index]
        value = sentence.find(word)  # 单词最初出现的位置
        feature[index] = value
    return np.array(feature)


def load_key_words(file_path):
    with open(file_path) as fp:
        lines = fp.readlines()
        lines = [line.replace("\n", "") for line in lines]
    return lines


def main():
    sentence = load_sentence("train.txt")
    key_words = load_key_words("word.txt")
    all_data = []
    for sen in sentence:
        while 1:
            print(sen + " you choose:1.积极，2消极，3，中立")
            choose = input(">>")
            try:
                choose = int(choose)
            except:
                continue
            if choose in [1, 2, 3]:
                break
        feature = _get_feature(sen, key_word=key_words).tolist()
        feature.append(choose)
        all_data.append(feature)
    with open("train_result.json", "w") as f:
        json.dump(all_data, f)
    print("OK!")


if __name__ == "__main__":
    main()
