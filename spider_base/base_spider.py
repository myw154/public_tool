# -*- coding: utf-8 -*-
import sys
import hashlib
import asyncio
import time
import json
import requests
from requests import request
from queue import Queue
from threading import Thread, Lock
from requests.exceptions import *
from datetime import datetime
from pathlib import Path
from abc import ABCMeta, abstractmethod

BASE_PATH = Path(__file__).parent
sys.path.append(BASE_PATH)


from ip_proxy import IPManager

class BaseSpider(object):
    """爬虫基类"""
    def __init__(self, thread_num=4, proxy_flag=True, ip_url=''):
        self.headers = {
            'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E217 MicroMessenger/6.8.0(0x16080000) NetType/WIFI Language/en Branch/Br_trunk MiniProgramEnv/Mac',
            }
        self.thread_num = thread_num
        self.thread_list = []  # 线程开启对象
        self.end_all_flag = False
        self.ip_url = ip_url
        self.ip_user = ""
        self.ip_key = ""

        if proxy_flag:
            if ip_url:
                self.ip_manager = IPManager(self.ip_url)
            else:
                print('获取代理IP的URL错误')


    def send_rquest_get(self, url, headers=None):
        """发送get请求"""
        if not headers:
            headers = self.headers
        count = 0
        while True and not self.end_all_flag:
            try:
                # requests.packages.urllib3.disable_warnings()
                if proxy_flag and self.ip_url:
                    ip_port = self.ip_manager.get_ip()
                    proxies_dict = {
                        "http": "http://{}:{}@".format(self.ip_user, self.ip_key)+ip_port+'/',
                        "https": 'http://{}:{}@'.format(self.ip_user, self.ip_key)+ip_port+'/',
                    }
                    res = request(method='get', url=url, timeout=30, verify=False, headers=headers, proxies=proxies_dict)
                else:
                    res = request(method='get', url=url, timeout=30, verify=False, headers=headers)
                try:
                    html_str = res.content.decode(encoding='utf-8')
                except Exception as err:
                    try:
                        html_str = res.content.decode(encoding='GBK')
                    except Exception as err:
                        try:
                            html_str = res.content.decode(encoding='GB2312')
                        except Exception as err:
                            html_str = res.content.decode(encoding='GB18030')
            except (ProxyError, SSLError, HTTPError, TooManyRedirects, ConnectionError, Timeout) as err:
                count += 1
                if count <= 20:
                    continue
                else:
                    raise Exception('more request Exception unknow')
            return html_str


    def send_rquest_post(self, url, data=None, headers=None, cookies=None, timeout=10, plate=None, json_str=None, proxy_flag=False):
        """发送post请求"""
        if not headers:
            headers = self.headers
        count = 0
        while True:
            try:
                if self.end_all_flag:
                    return ''
                # requests.packages.urllib3.disable_warnings()
                if proxy_flag and self.ip_url:
                    ip_port = self.ip_manager.get_ip()
                    proxies_dict = {
                        "http": "http://{}:{}@".format(self.ip_user, self.ip_key)+ip_port+'/',
                        "https": 'http://{}:{}@'.format(self.ip_user, self.ip_key)+ip_port+'/',
                    }
                    res = requests.post(url, headers=headers, cookies=cookies, data=data, proxies=proxies_dict, verify=False,
                                        timeout=timeout, json=json_str)
                else:
                    res = request(method='post', url=url, data=data, headers=headers, timeout=timeout, verify=False, cookies=cookies, json=json_str)
                try:
                    html_str = res.content.decode(encoding='utf-8')
                except Exception as err:
                    try:
                        html_str = res.content.decode(encoding='GBK')
                    except Exception as err:
                        try:
                            html_str = res.content.decode(encoding='GB2312')
                        except Exception as err:
                            html_str = res.content.decode(encoding='GB18030')
            except (ProxyError, SSLError, HTTPError, TooManyRedirects, ConnectionError, Timeout) as err:
                count += 1
                if count <= 20:
                    continue
                else:
                    raise Exception('more request Exception unknow')
            return html_str

    def hash_string(self, input_string):
        """字符串转加密字符串"""
        hash_object = hashlib.sha256()
        hash_object.update(input_string.encode('utf-8'))
        hex_dig = hash_object.hexdigest()
        return hex_dig

    def cookie_string_to_dict(self, cookie_str):
        """ cookie字符串转dict """
        cookie_dict = {}
        pairs = cookie_str.split(';')
        for pair in pairs:
            key_value = pair.strip().split('=', 1)
            if len(key_value) == 2:
                key, value = key_value
                cookie_dict[key] = value
            elif len(key_value) > 2:
                key, *value = key_value
                cookie_dict[key] = "".join(value)
        return cookie_dict

    @abstractmethod
    def run_thread_list(self):
        """自类中实现此方法"""
        self.thread_name_list = []
        self.more_thread_name_list = []


    def run(self):
        """
        parameter:
            thread_name_list   # 开启单线程的任务列表
            more_thread_name_list   # 开启多线程列表
        """
        self.run_thread_list()
        for t in self.thread_name_list:
            self.thread_list.append(Thread(target=t))

        start_time = datetime.now()
        for t in self.more_thread_name_list:
            for j in range(self.thread_num):
                 self.thread_list.append(Thread(target=t))

        for t in self.thread_list:
            t.setDaemon(True)
            t.start()


        for t in self.thread_list:
            t.join()

        end_time = datetime.now()
        print('采集开始时间：：：%s' % start_time)
        print('采集结束时间：：：%s' % end_time)


