#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fastjson_check 
@File ：user_agent.py.py
@Author ：trance
@Date ：2021/7/2 14:20 
'''
import random
from utils.rw_file import RWFile


class UserAgent:
    """
    传入配置文件
    """

    def __init__(self, rw_file: RWFile = None):
        self.rwFile = rw_file
        self.__read_ua()

    def set_rw_file(self, rw_file: RWFile):
        """
        :param rw_file:
        """
        self.rwFile = rw_file
        self.ua_dict = {}
        self.__read_ua()

    def __read_ua(self):
        """
        读取UA
        """
        if self.rwFile is None:
            return
        self.ua_dict = self.rwFile.read()

    def random_agent(self):
        """
         随机生成user-agent
        :return: user-agent str
        """
        user_agent = random.choice(list(self.ua_dict.keys()))
        return self.ua_dict.get(user_agent)

    def view_gent(self):
        """
        展示keys
        :return: list
        """
        keys = self.ua_dict.keys()
        return keys

    def inupt_agent(self, key):
        """
        根据key选择对应的user-agent value
        :param key: user-agent key
        :return: user-agent value
        """
        user_agent = self.ua_dict[key]
        return user_agent
