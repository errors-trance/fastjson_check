#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fastjson_check 
@File ：dis_fastjaon.py
@Author ：trance
@Date ：2021/7/5 16:13 
'''
import requests
from utils.dnslog import DNSLog
from utils.user_agent import UserAgent
from utils.rw_file import RWFile


class DisFastjson:
    """
    探测是否使用fastjson
    区分fastjson和jackson
    """
    def __init__(self, url):
        self.rwfile = RWFile('../texts/user_agent')
        self.agent = UserAgent(self.rwfile).random_agent()
        self.dnslog = DNSLog('http://www.dnslog.cn', self.agent)
        self.url = url
        self.proxies={
            'http':'http://127.0.0.1:8080',
            'https':'https://127.0.0.1:8080',
        }

    def dnslog_check(self):
        """
        fastjson使用 dnslog检测
        :return: bool
        """
        domain = self.dnslog.getdomain()
        print(domain)
        pocs = self.read_poc(domain)
        headers = self.headers()
        for poc in pocs:
            self.request_post(self.url, headers, poc)
            records = self.dnslog.get_records()
            print(records)
            if len(records) > 0:
                return True
        return False

    def data_check(self, data):
        """
        生成新的data数据
        :param data:
        :return: dict
        """
        data['qf1a2e3s4f5'] = '1'
        return data

    def read_poc(self, domain):
        """
        生成 fastjson poc
        :param domain:
        :return: list
        """
        poc = list(RWFile('../texts/fastjson_dis_poc').read().values())
        pocs = []
        for v in poc:
            exp = v.replace('{0}', domain)
            pocs.append(exp)
        return pocs

    def headers(self, content_type='application/json', cookie=None):
        """
        生成headers
        :param url:
        :param content_type:
        :param cookie:
        :return: obj
        """
        if cookie is None:
            headers = {
                'user-agent': self.agent,
                'Accept-Encoding': 'gzip, deflate',
                'Accept': '*/*',
                'Content-Type': content_type
            }
        else:
            headers = {
                'user-agent': self.agent,
                'Accept-Encoding': 'gzip, deflate',
                'Accept': '*/*',
                'Content-Type': content_type,
                'Cookie': cookie
            }
        return headers

    def requests_get(self, url, headers):
        """
        get请求
        :param url:
        :param headers:
        :return:
        """
        res = requests.get(url, headers=headers, timeout=5)
        return res.status_code,res.headers,res.text,res.elapsed.microseconds

    def request_post(self, url, headers, data):
        """
        post请求
        :param url:
        :param headers:
        :param data:
        :return:
        """
        res = requests.post(url, headers=headers, data=data, timeout=5)
        return res.status_code,res.headers,res.text,res.elapsed.microseconds
