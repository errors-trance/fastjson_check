#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fastjson_check 
@File ：rw_file.py
@Author ：trance
@Date ：2021/7/2 14:33 
'''
import json


class RWFile:
    """
    指定文件全路径
    读取文件格式:
    A:B
    C:D
    """

    def __init__(self, filepath):
        self.filepath = filepath

    def read(self):
        """
        读取文件
        :return: dict
        """
        with open(self.filepath, mode='r', encoding='UTF-8') as f:
            lines = f.readlines()
            result = {}
            for line in lines:
                ua_arr = line.split(":", maxsplit=1)
                print(ua_arr)
                result.setdefault(ua_arr[0].strip(), ua_arr[1].strip())
            return result

    def reads(self):
        """
        读取文件
        :return: dict
        """
        with open(self.filepath, mode='r', encoding='UTF-8') as f:
            lines = f.readlines()
            return lines


    def write(self, data):
        """
        写入文件
        :param data:
        :return: json
        """
        with open(self.filepath, mode='w', encoding='UTF-8') as f:
            return f.write(json.dumps(data))
