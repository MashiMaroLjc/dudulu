# coding:utf-8


import json


class Response:
    def __init__(self, status, data, info=None):
        self.status = status
        self.data = data
        self.info = info

    def to_json(self):
        temp = {
            "status": self.status,
            "data": self.data,
            "info": self.info
        }
        return json.dumps(temp)
