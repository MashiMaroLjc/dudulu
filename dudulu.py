# usr/bin/python
# coding:utf-8


import logging

from flask import Flask
from flask import render_template
from flask import request

from response import Response
from word import *

app = Flask(__name__)
FAILED = "failure"
SUCCEED = "successful"
MAX_WORD = 200  # 句子最大长度
MIN_WORD = 1  # 句子最少长度

KEY_WORD = load_key_words("train/new_word.txt")  # tool.py脚本产生的关键字列表，用于提取特征
MODEL_NAME = "train/model/gnb.model"  # 已经训练好的数据集

SENTENCE_FILE = open("logs/sentence.log", "a")  # 接受到的句子日志

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s  %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='logs/app.log',
    filemode='a'
)


@app.route("/", methods=["GET"])
def home_page():
    return render_template("index.html")


@app.route("/cut", methods=["GET"])
def cut_word():
    """
    分词
    :return:
    """
    sentence = request.args.get("sentence")
    cut_method = request.args.get("method")
    if not sentence:
        return Response(FAILED, None, info="Miss Params").to_json()
    if len(sentence) > MAX_WORD or len(sentence) < MIN_WORD:
        return Response(FAILED, None, info="The Sentence "
                                           "is too long.It should be %s to %s." % (MIN_WORD, MAX_WORD)).to_json()
    if not cut_method or cut_method not in CUT_METHODS:
        cut_method = "default"
    result = CUT_METHODS.get(cut_method)(sentence)
    return Response(SUCCEED, result).to_json()


@app.route("/count", methods=["GET"])
def count_word():
    """
    分词后计算
    :return:
    """
    cut_method = request.args.get("method")
    sentence = request.args.get("sentence")
    if not sentence:
        return Response(FAILED, None, "Miss Params").to_json()
    if len(sentence) > 10000 or len(sentence) < 1:
        return Response(FAILED, None, info="The Sentence "
                                           "is too long.It should be %s to %s." % (1, 10000)).to_json()

    if not cut_method or cut_method not in CUT_METHODS:
        cut_method = "default"
    result = word_count(sentence, cut_method)
    return Response(SUCCEED, result).to_json()


@app.route("/mood", methods=["GET"])
def mood():
    """
    情绪分析
    :return:
    """
    ip = request.remote_addr
    sentence = request.args.get("sentence")
    if not sentence:
        return Response(FAILED, None, info="Miss Params").to_json()
    if len(sentence) > MAX_WORD or len(sentence) < MIN_WORD:
        return Response(FAILED, None, info="The Sentence "
                                           "is too long.It should be %s to %s." % (MIN_WORD, MAX_WORD)).to_json()
    result = get_mood(sentence, key_word=KEY_WORD, model_name=MODEL_NAME)
    print("ip: %s | sentence: %s | positive: %s | negative: %s | neutral: %s" % (ip, sentence,
                                                                                 result["positive"], result["negative"],
                                                                                 result["neutral"]), file=SENTENCE_FILE)
    SENTENCE_FILE.flush()
    return Response(SUCCEED, result).to_json()


if __name__ == "__main__":
    port = 8888
    DEBUG = None
    if not DEBUG:
        host ="0.0.0.0"
    else:
        host = "localhost"
    print("listen %s port: %s"%(host,port))
    app.run(host=host,port=port,debug=DEBUG)
    SENTENCE_FILE.close()
    # lines = load_key_words("train/word.txt")
    # print(lines)
