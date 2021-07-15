#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fastjson_check 
@File ：ssh.py
@Author ：trance
@Date ：2021/7/6 20:08 
'''
import paramiko, time, keyboard


class ssh:
    """
    ssh登录 执行命令
    """

    def __init__(self, ip, username, passwd, port=22):
        self.ip = ip
        self.username = username
        self.passwd = passwd
        self.port = port
        self.bool = False
        self.ssh = self.login()

    # ssh登录
    def login(self):
        """
        ssh登录
        """
        try:
            ssh = paramiko.SSHClient()
            # 这行代码的作用是允许连接不在know_hosts文件中的主机。
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.ip, self.port, self.username, self.passwd)
            chan = ssh.invoke_shell()  # 定义ssh调用子进程
            time.sleep(1)
            result = chan.recv(100000).decode()
            print(result)
            return ssh
        except Exception as e:
            raise e

    def exec(self, cmd=None):
        """
        ssh 命令交互
        """
        while True:
            if cmd is None:
                cmd = input('请输入命令：')
            if cmd == 'exit':
                break
            else:
                stdin, stdout, stderr = self.ssh.exec_command(cmd, get_pty=True)
                while True:
                    line = stdout.readline()
                    if keyboard.is_pressed('ctrl+z'):
                        break
                    if len(line) == 0:
                        break
                    else:
                        print(line)
        self.close()

    def close(self):
        """
        关闭ssh
        """
        self.ssh.close()
