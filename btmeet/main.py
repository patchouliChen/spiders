# -*- coding:utf-8 -*-
import os
import re
import sys
import requests
import datetime
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

    def get_search_page(self, key_word, page_num):
        page_name = str(page_num) + "-1.html"
        url = '/'.join([self.search_page, key_word, page_name])
        return get_page(url, self.proxies)

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

    def search(self, key_word):
        magnets = []
        page_num = 1
        while(1):
            page_code = self.get_search_page(key_word, page_num)
            urls = self.get_post_urls(page_code)
            if len(urls) <= 0:
                break

            for url in urls:
                url = self.home_page + url  
                sub_page_code = get_page(url)
                magnets.extend(self.get_magnets(sub_page_code))
           
            page_num += 1

        return magnets

    def writeToFile(self, key_words, magnets):
        filename = '_'.join(key_words) + ".txt"
        output_file = os.path.join(self.root_path, filename)
        f = open(output_file, "wa")
        for magnet in magnets:
            f.write(magnet + "\n")
        f.close()

    def searchAll(self, key_words):
        magnets = []
        for key_word in key_words:
            magnets.extend(self.search(key_word))

        magnets = set(magnets)
        self.writeToFile(key_words, magnets)

usage = """
usage:
    python main.py keyword(s)
"""

if __name__ == "__main__":
    argv = sys.argv
    
    if len(argv) < 2:
        print usage 
        exit()

    keywords = argv[1:len(argv)]
    btmeet = BtMeet()
    btmeet.searchAll(keywords)
