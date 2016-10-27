#!/usr/bin/env python
# -*- coding:utf-8 -*-
import argparse
import os
import re
import sys
import Queue
import threading
import time

sys.path.append("../")
from utils import *
from web_sites import web_list

class BtSearch:
    PAGE_NUM_NORMAL = 1
    PAGE_NUM_MINUS = 2
    PAGE_NUM_MULTI = 3

    MAGNET_PREFIX = "magnet:?xt=urn:btih:"

    USING_GET = 1
    USING_POST = 2

    def __init__(self, keys_file, directory, thread_num=100):
        self.keys_file = keys_file
        self.directory = directory
        self.thread_num = thread_num
        self.keywords = read_lines(self.keys_file)

        # shadowsocks
        self.proxies = {'http' : 'socks5:127.0.0.1:1080', 'https': 'socks5:127.0.0.1:1080'}
        self.magnets = [] 

        self.page_fetch_queue = Queue.Queue()
        self.magnet_fetch_queue = Queue.Queue()

    def run(self):
        for _ in xrange(self.thread_num):
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

        for _ in xrange(self.thread_num):
            magnet_thread = threading.Thread(target = self.magnet_fetcher)
            magnet_thread.daemon = True
            magnet_thread.start()

        self.magnet_fetch_queue.join()

        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        filename = '_'.join(self.keywords) + ".txt"
        output_file = os.path.join(self.directory, filename)
        f = open(output_file, "wa")
        self.magnets = [magnet.lower() for magnet in self.magnets]
        self.magnets = set(self.magnets)
        for magnet in self.magnets:
            if magnet.find(BtSearch.MAGNET_PREFIX) == -1:
                magnet = BtSearch.MAGNET_PREFIX + magnet
            if len(magnet) == 60 or len(magnet) == 52 or len(magnet) == 64:
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
                match_iter = self.get_post_match_iter(cfg, page_code)
                has_valid_post = False

                match_count = 0
                for post_match in match_iter:
                    match_count += 1
                    match_dict = post_match.groupdict()
                    title = match_dict.get("title")
                    post = match_dict.get("post")
                    magnet = match_dict.get("magnet")

                    if title != None and self.validate_title(title, keyword) == False:
                        if cfg.get("search_all") != None:
                            has_valid_post = True
                    else:
                        has_valid_post = True
                        self.add_post_job(cfg, post, magnet, keyword)

                # for some non stop web_site
                if cfg.get("per_page_count") != None:
                    if match_count < cfg["per_page_count"]:
                        has_valid_post = False

                if has_valid_post == False:
                    self.page_fetch_queue.task_done()
                    break

                page_num += 1

    def magnet_fetcher(self):
        while True:
            args = self.magnet_fetch_queue.get()
            cfg = args[0]
            post_url = args[1]
            keyword = args[2]
            self.search_one_post(cfg, post_url, keyword)
            self.magnet_fetch_queue.task_done()

    def calc_page_num(self, cfg, page_num):
        page_num_type = cfg.get("page_num_type", BtSearch.PAGE_NUM_NORMAL)
        if page_num_type == BtSearch.PAGE_NUM_MULTI:
            return 20 * (page_num - 1)
        elif page_num_type == BtSearch.PAGE_NUM_MINUS:
            return page_num - 1
        else:
            return page_num

    def get_search_page(self, cfg, keyword, page_num):
        page_num = self.calc_page_num(cfg, page_num)

        # this web_site use post
        if cfg.get("http_method") == BtSearch.USING_POST:
            page_name = cfg["page_format"] % keyword
            url = '/'.join([cfg["home"], page_name])
            data = {"text" : keyword, "page" : page_num}  
            return post_page(url, data, self.proxies)
        else:
            page_name = cfg["page_format"] % (keyword, page_num)
            url = '/'.join([cfg["home"], page_name])
            return get_page(url, self.proxies)

    def get_post_match_iter(self, cfg, page_code):
        match_iter = re.finditer(cfg["post_pattern"], page_code, re.S)
        return match_iter

    def add_post_job(self, cfg, post, magnet, keyword):
        if magnet != None:
            self.magnets.append(magnet)
        else:
            args = (cfg, post, keyword)
            self.magnet_fetch_queue.put(args)

    def validate_title(self, title, keyword):
        title = title.replace("<font color=\"red\">", "")
        title = title.replace("</font>", "")
        title = title.replace("<b>", "")
        title = title.replace("</b>", "")
        title = title.replace("<b class=srchHL>", "")
        title = title.replace("</b>", "")
        title = title.replace("<span class=\"mhl\">", "")
        title = title.replace("<span class=\"highlight\">", "")
        title = title.replace("<span class='highlight'>", "")
        title = title.replace("</span>", "")
        title = title.replace("<key>", "")
        title = title.replace("</key>", "")
        title = title.replace(" ", "")

        return title.find(keyword) != -1 \
            or title.find(keyword.replace(" ", "-")) != -1 \
            or title.find(keyword.replace(" ", "")) != -1 \
            or title.find(keyword.lower()) != -1 \
            or title.find(keyword.lower().replace(" ", "-")) != -1 \
            or title.find(keyword.lower().replace(" ", "")) != -1
            
    def search_one_post(self, cfg, post_url, keyword):
        post_url = '/'.join([cfg["home"], post_url])

        sub_page_code = get_page(post_url, self.proxies)

        if cfg.get("Cilibaba") != None:
            self.magnets.extend(self.get_magnets_cilibaba(cfg, sub_page_code))
        elif cfg.get("download_pattern") != None:
            self.download_torrent(cfg, sub_page_code)
        else:
            self.magnets.extend(self.get_magnets(cfg, sub_page_code))

    def download_torrent(self, cfg, page_code):
        title = re.findall(cfg["download_title"], page_code, re.S)[0]
        title = title.replace("/", "")
        download_url = re.findall(cfg["download_pattern"], page_code, re.S)[1]
        output_file = os.path.join(self.directory, title + ".torrent")
        torrent_data = get_page("/".join([cfg["home"], download_url]), proxies=self.proxies)
        f = open(output_file, "wb")
        f.write(torrent_data)
        f.close()

    def get_magnets(self, cfg, page_code):
        magnets = re.findall(cfg["magnet_pattern"], page_code, re.S)
        return magnets

    def get_magnets_cilibaba(self, cfg, page_code):
        hashes = re.findall('/api\/json_info\?hashes=.*?\'.*?\'(.*?)\'', page_code)[0]
        json_url = '/'.join([cfg["home"], "api", "json_info?hashes=" + hashes])
        while True:
            hash_page_code = get_page(json_url, self.proxies)

            sub_magnets = self.get_magnets(cfg, hash_page_code)
            if len(sub_magnets) <= 0:
                time.sleep(3.0)
            else:
                result = [] 
                for sub_magnet in sub_magnets:
                    magnet_str = "magnet:?xt=urn:btih:" + sub_magnet
                    result.append(magnet_str)
                return result

def main():
    # parse arguments
    parser = argparse.ArgumentParser(description="BtSearch") 
    parser.add_argument("keys_file", help="keys to be searched")
    parser.add_argument('directory', help="Where to save the magnets")
    parser.add_argument("-t", "--thread", help="Number of threads to use", type=int, dest="thread_num", default=100)

    args = parser.parse_args()

    bs = BtSearch(keys_file=args.keys_file,
            directory=args.directory,
            thread_num=args.thread_num)
    bs.run()

if __name__ == "__main__":
    main()
