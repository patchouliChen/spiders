# -*- coding:utf-8 -*-
import os
import re
import sys
import requests
import datetime
import Queue
import threading
import time
sys.path.append("../")
from utils import *

root_path = os.path.join(os.path.curdir, "btsearch_spider")
log_file = os.path.join(root_path, "log")

class BtSearch:
    def __init__(self):
        self.cfg = None 

        # shadowsocks
        self.s_proxies = {'http': 'socks5:127.0.0.1:1080'}
        self.proxies = {}

        self.magnet_queue = Queue.Queue()
        self.magnet_worker = 10

    def set_cfg(self, cfg):
        self.cfg = cfg

    def set_use_shadowsocks(self, is_use):
        if is_use == True:
            self.proxies = self.s_proxies
        else:
            self.proxies = {}

    def get_search_page(self, keyword, page_num):
        page_name = self.cfg["page_format"] % (keyword, page_num)
        url = '/'.join([self.cfg["home"], page_name])
        return get_page(url, self.proxies)

    def get_post_urls(self, page_code):
        r = re.compile(self.cfg["post_pattern"])
        urls = r.findall(page_code)
        return urls

    def get_magnets(self, page_code):
        r = re.compile(self.cfg["magnet_pattern"])
        magnets = r.findall(page_code)
        return magnets

    def search_one_post(self, post_url, magnets):
        post_url = '/'.join([self.cfg["home"], post_url])
        sub_page_code = get_page(post_url)
        magnets.extend(self.get_magnets(sub_page_code))

    def worker(self):
        while True:
            args = self.magnet_queue.get()
            self.search_one_post(*args)
            self.magnet_queue.task_done()

    def search(self, keyword, magnets):
        page_num = 1
        while True:
            page_code = self.get_search_page(keyword, page_num)
            post_urls = self.get_post_urls(page_code)
            if len(post_urls) > 0:
                for post_url in post_urls:
                    args = (post_url, magnets)
                    self.magnet_queue.put(args)
                page_num += 1
            else:
                break

    def search_all(self, keywords):
        if self.cfg == None:
            print "Plaase Set a web site config first"
            return

        magnets = []
        for keyword in keywords:
            self.search(keyword, magnets)

        for _ in xrange(self.magnet_worker):
            t = threading.Thread(target = self.worker)
            t.daemon = True
            t.start()

        self.magnet_queue.join()

        magnets = set(magnets)
        return magnets


class Cilibaba(BtSearch):
    def search_one_post(self, post_url, magnets):
        json_url = '/'.join([self.cfg["home"], "api", "json_info?hashes=" + post_url])
        while True:
            sub_page_code = get_page(json_url)
            sub_magnets = self.get_magnets(sub_page_code)
            if len(sub_magnets) <= 0:
                time.sleep(3.0)
            else:
                for sub_magnet in sub_magnets:
                    magnet_str = "magnet:?xt=urn:btih:" + sub_magnet
                    magnets.append(magnet_str)
                return

usage = """
usage:
    python main.py filename
"""

web_list = [
    {
        "home" : "http://www.btcrawler.com",
        "page_format" : "%s-first-asc-%d",
        "post_pattern" : '<a href="/(.*?)" target="_blank">',
        "magnet_pattern" : '(magnet:\?xt=urn:btih:.*?)&dn='
    },

    {
        "home" : "http://www.shenmidizhi.com",
        "page_format" : "list/%s-first-asc-%d",
        "post_pattern" : '<a class="title" href="/(.*?)">',
        "magnet_pattern" : 'href=\'(magnet:\?xt=urn:btih:.*?)\'>' 
    },

    {
        "home" : "http://www.cilibaba.com",
        "page_format" : "search/%s/?c=&s=create_time&p=%d",
        "post_pattern" : '<a title=".*?" class="title" href="/h/(.*?)">',
        "magnet_pattern" : '"info_hash": "(.*?)",'
    },
]

if __name__ == "__main__":
    argv = sys.argv
    
    if len(argv) < 2:
        print usage 
        exit()

    keywords = read_lines(argv[1])

    cb = Cilibaba()
    cb.set_cfg(web_list[2])
    cb.set_use_shadowsocks(True)
    magnets = cb.search_all(keywords)

    btsearch = BtSearch()
    btsearch.set_cfg(web_list[0])
    magnets = magnets.union(btsearch.search_all(keywords))

    btsearch = BtSearch()
    btsearch.set_cfg(web_list[1])
    magnets = magnets.union(btsearch.search_all(keywords))
    
    filename = '_'.join(keywords) + ".txt"
    output_file = os.path.join(root_path, filename)
    f = open(output_file, "wa")
    for magnet in magnets:
        f.write(magnet + "\n")
    f.close()
