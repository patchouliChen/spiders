#!/usr/bin/env python
# -*- coding:utf-8 -*-
import argparse
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
from web_sites import web_list

root_path = os.path.join(os.path.curdir, "btsearch_spider")
log_file = os.path.join(root_path, "log")

class BtSearch:
    def __init__(self):
        self.cfg = None 

        # shadowsocks
        self.s_proxies = {'http' : 'socks5:127.0.0.1:1080', 'https': 'socks5:127.0.0.1:1080'}
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
        sub_page_code = get_page(post_url, self.proxies)
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
            print "Please Set a web site config first"
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
            sub_page_code = get_page(json_url, self.proxies)
            sub_magnets = self.get_magnets(sub_page_code)
            if len(sub_magnets) <= 0:
                time.sleep(3.0)
            else:
                for sub_magnet in sub_magnets:
                    magnet_str = "magnet:?xt=urn:btih:" + sub_magnet
                    magnets.append(magnet_str)
                return

class Oooc(BtSearch):
    def get_search_page(self, keyword, page_num):
        page_name = self.cfg["page_format"] % (keyword, 20 * (page_num - 1))
        url = '/'.join([self.cfg["home"], page_name])
        return get_page(url, self.proxies)

def main():
    # parse arguments
    parser = argparse.ArgumentParser(description="BtSearch") 
    parser.add_argument("filename", help=("keys to be searched"))
    #parser.add_argument("directory", help="Where to save the magnets")
    #parser.add_argument("-l", "--log-level", help="Log level", default='info')
    #parser.add_argument("-p", "--process", help="Number of concurrent processes to use")

    args = parser.parse_args()
    filename = args.filename

    keywords = read_lines(filename)

    magnets = set()
    for cfg in web_list:
        if cfg["active"] == False:
            continue

        class_name = cfg.get("class_name")
        if class_name == None:
            ins = BtSearch() 
        else:
            ins = globals()[class_name]()

        ins.set_cfg(cfg)
        ins.set_use_shadowsocks(True)
        magnets = magnets.union(ins.search_all(keywords))

    filename = '_'.join(keywords) + ".txt"
    output_file = os.path.join(root_path, filename)
    f = open(output_file, "wa")
    for magnet in magnets:
        if len(magnet) == 60:
            f.write(magnet + "\n")
    f.close()

if __name__ == "__main__":
    main()
