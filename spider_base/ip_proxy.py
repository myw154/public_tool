import requests
import random
import logging
import time
import json

class IPManager:
    def __init__(self, api_url):
        self.api_url = api_url
        self.usage_counts = {}
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.logger = logging.getLogger(__file__)

    def fetch_ips(self):
        """ 从API获取新的IP列表，并重置使用次数 """
        while True:
            try:
                response = requests.get(self.api_url)
                if response.json()["code"] == 200:
                    ip_list = response.json()['data']['proxy_list']
                    self.logger.info("获取到的代理为：%s" % str(ip_list))
                    if not ip_list:
                        self.logger.info("没有获取到有效的代理IP")
                        time.sleep(3)
                        continue
                    self.usage_counts = {ip: 0 for ip in ip_list}
                    break
                else:
                    self.logger.info("没有获取到有效的代理IP")
                    time.sleep(3)
            except Exception as err:
                self.logger.info('获取代理异常重新获取')
                time.sleep(3)
                continue


    def get_ip(self):
        """ 返回使用次数最少的IP，并增加其使用次数。如果没有IP，则从API获取新的IP列表。 """
        if not self.usage_counts:
            self.fetch_ips()
        min_usage = min(self.usage_counts.values())
        if min_usage >= 15:
            self.usage_counts = {}
            self.fetch_ips()

        candidates = [ip for ip, count in self.usage_counts.items() if count < 15]

        # 从候选IP中随机选择一个，避免总是选择相同的IP
        selected_ip = random.choice(candidates)

        # 增加IP的使用次数
        self.usage_counts[selected_ip] += 1
        return selected_ip


