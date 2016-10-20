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
    def __init__(self, keys_file):
        self.keys_file = keys_file
        self.keywords = read_lines(self.keys_file)

        # shadowsocks
        self.proxies = {'http' : 'socks5:127.0.0.1:1080', 'https': 'socks5:127.0.0.1:1080'}
        self.magnets = set()

        self.page_fetch_queue = Queue.Queue()
        self.page_worker = 10

        self.magnet_fetch_queue = Queue.Queue()
        self.magnet_worker = 10

    def run(self):
        for _ in xrange(self.page_worker):
            page_thread = threading.Thread(target = self.page_fetcher)
            page_thread.daemon = True
            page_thread.start()

        for cfg in web_list:
            if cfg["active"] == False:
                continue
            for keyword in self.keywords:
                args = (cfg, keyword)
                self.page_fetch_queue.put(args)

        self.page_fetch_queue.join()

        for _ in xrange(self.magnet_worker):
            magnet_thread = threading.Thread(target = self.magnet_fetcher)
            magnet_thread.daemon = True
            magnet_thread.start()

        self.magnet_fetch_queue.join()

        filename = '_'.join(self.keywords) + ".txt"
        output_file = os.path.join(root_path, filename)
        f = open(output_file, "wa")
        for magnet in self.magnets:
            if len(magnet) == 60:
                f.write(magnet + "\n")
        f.close()

    def page_fetcher(self):
        while True:
            args = self.page_fetch_queue.get()
            cfg = args[0]
            keyword = args[1]
            page_num = 1
            while True:
                page_code = self.get_search_page(cfg, keyword, page_num)
                post_urls = self.get_post_urls(cfg, page_code)
                if len(post_urls) > 0:
                    for post_url in post_urls:
                        args = (cfg, post_url)
                        self.magnet_fetch_queue.put(args)
                    page_num += 1
                else:
                    self.page_fetch_queue.task_done()
                    break

    def magnet_fetcher(self):
        while True:
            args = self.magnet_fetch_queue.get()
            cfg = args[0]
            post_url = args[1]
            self.search_one_post(cfg, post_url)
            self.magnet_fetch_queue.task_done()

    def get_search_page(self, cfg, keyword, page_num):
        if cfg.get("Oooc") != None:
            page_name = cfg["page_format"] % (keyword, 20 * (page_num - 1))
        else:
            page_name = cfg["page_format"] % (keyword, page_num)

        url = '/'.join([cfg["home"], page_name])
        return get_page(url, self.proxies)

    def get_post_urls(self, cfg, page_code):
        urls = re.findall(cfg["post_pattern"], page_code)
        return urls

    def get_magnets(self, cfg, page_code):
        magnets = re.findall(cfg["magnet_pattern"], page_code)
        return magnets

    def search_one_post(self, cfg, post_url):
        if cfg.get("Cilibaba") != None:
            self.search_one_post_cilibaba(cfg, post_url)
        else:
            self.search_one_post_common(cfg, post_url)

    def search_one_post_cilibaba(self, cfg, post_url):
        json_url = '/'.join([cfg["home"], "api", "json_info?hashes=" + post_url])
        while True:
            sub_page_code = get_page(json_url, self.proxies)
            sub_magnets = self.get_magnets(cfg, sub_page_code)
            if len(sub_magnets) <= 0:
                time.sleep(3.0)
            else:
                for sub_magnet in sub_magnets:
                    magnet_str = "magnet:?xt=urn:btih:" + sub_magnet
                    self.magnets.add(magnet_str)
                return

    def search_one_post_common(self, cfg, post_url):
        post_url = '/'.join([cfg["home"], post_url])
        sub_page_code = get_page(post_url, self.proxies)
        self.magnets = self.magnets.union(set(self.get_magnets(cfg, sub_page_code)))

def main():
    # parse arguments
    parser = argparse.ArgumentParser(description="BtSearch") 
    parser.add_argument("keys_file", help=("keys to be searched"))
    #parser.add_argument("directory", help="Where to save the magnets")
    #parser.add_argument("-l", "--log-level", help="Log level", default='info')
    #parser.add_argument("-p", "--process", help="Number of concurrent processes to use")

    args = parser.parse_args()

    bs = BtSearch(args.keys_file)
    bs.run()

if __name__ == "__main__":
    main()
