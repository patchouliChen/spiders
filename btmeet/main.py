# -*- coding:utf-8 -*-
import os
import re
import sys
import requests
import datetime
import Queue
import threading
sys.path.append("../")
from utils import *

class BtMeet:
    def __init__(self):
        self.home_page = "http://www.btmeet.com"
        self.search_page = self.home_page + "/search"
        self.root_path = "/Users/chenxiaoming/Documents/btmeet_spider/"
        #self.proxies = {'http': 'socks5:127.0.0.1:1080'}
        self.proxies = {}
        self.log_file = os.path.join(self.root_path, "log")
        self.queue = Queue.Queue()
        self.worker_num = 10
        self.num_per_page = 10

    def get_search_page(self, key_word, page_num):
        page_name = str(page_num) + "-1.html"
        url = '/'.join([self.search_page, key_word, page_name])
        return get_page(url, self.proxies)

    def get_page_count(self, page_code):
        pattern = '<span>大约 (.*?) 条结果.*?</span>'
        r = re.compile(pattern)
        total_num = r.findall(page_code)[0]
        total_num = int(total_num)
        page_count = total_num / self.num_per_page + 1
        return page_count

    def get_post_urls(self, page_code):
        pattern = '<a href="(/wiki/.*?.html)'
        r = re.compile(pattern)
        urls = r.findall(page_code)
        return urls

    def get_magnets(self, page_code):
        pattern = '<a href="(magnet:\?xt=urn:btih:.*?)">'
        r = re.compile(pattern)
        magnets = r.findall(page_code)
        return magnets

    def search_one_page(self, key_word, page_num, magnets):
        page_code = self.get_search_page(key_word, page_num)
        urls = self.get_post_urls(page_code)
        if len(urls) <= 0:
            return

        for url in urls:
            url = self.home_page + url
            sub_page_code = get_page(url)
            magnets.extend(self.get_magnets(sub_page_code))

    def worker(self):
        while True:
            args = self.queue.get()
            self.search_one_page(*args)
            self.queue.task_done()

    def search(self, key_word, magnets):
        first_page = self.get_search_page(key_word, 1)
        page_count = self.get_page_count(first_page)

        for page_num in xrange(1, page_count + 1):
            args = (key_word, page_num, magnets)
            self.queue.put(args)

    def searchAll(self, key_words):
        for i in xrange(self.worker_num):
            t = threading.Thread(target = self.worker)
            t.daemon = True
            t.start()

        magnets = []
        for key_word in key_words:
            self.search(key_word, magnets)

        self.queue.join()

        magnets = set(magnets)
        self.write_to_file(key_words, magnets)

    def write_to_file(self, key_words, magnets):
        filename = '_'.join(key_words) + ".txt"
        output_file = os.path.join(self.root_path, filename)
        f = open(output_file, "wa")
        for magnet in magnets:
            f.write(magnet + "\n")
        f.close()



usage = """
usage:
    python main.py filename
"""

if __name__ == "__main__":
    argv = sys.argv
    
    if len(argv) < 2:
        print usage 
        exit()

    keywords = read_lines(argv[1])
    btmeet = BtMeet()
    btmeet.searchAll(keywords)
