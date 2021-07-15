#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fastjson_check 
@File ：dnslog.py.py
@Author ：trance
@Date ：2021/7/2 14:14 
'''
import requests,random
from utils.user_agent import UserAgent


class DNSLog:
    """
    dnslog 服务
    """
    def __init__(self, url, user_agent:UserAgent):
        self.url = url
        self.s = requests.session()
        self.headers = {
            "user-agent": user_agent,
            "Content-Type": "text/html; charset=UTF-8"
        }
        self.proxies = {
            'http': 'http://127.0.0.1:8080',
            'https': 'https://127.0.0.1:8080',
        }

    def getdomain(self):
        """
        获取 dns domian
        :return: str
        """
        try:
            url = self.url + '/getdomain.php?t=' + str(random.random())
            #res = self.request(url, headers=self.headers, proxies=self.proxies, timeout=5)
            res = self.s.get(url, headers=self.headers, proxies=self.proxies, timeout=5)
            return res.text
        except Exception as e:
            return e

    def get_records(self):
        """
        获取结果
        :return: json
        """
        try:
            url = self.url + '/getrecords.php?t=' + str(random.random())
            # res = requests.get(url, headers=self.headers, proxies=self.proxies, timeout=5)
            res = self.s.post(url, headers=self.headers, proxies=self.proxies, timeout=5)
            return res.json()
        except Exception as e:
            return e