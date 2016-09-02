# -*- coding:utf-8 -*-
import os
import re
import sys
import requests
import datetime
sys.path.append("../")
from utils import *

class CL:
    def __init__(self):
        self.home_page = "http://www.t66y.com/"
        self.anime_page_prefix = self.home_page + "thread0806.php?fid=5&search=&page="
        self.torrent_path = "/Users/chenxiaoming/Documents/ts_spider" 
        self.cover_path = "/Users/chenxiaoming/Documents/cs_spider"
        self.proxies = {'http': 'socks5:127.0.0.1:1080'}
        self.cover_log = "cover"
        self.torrent_log = "torrent"

    def getCLPage(self, sub_url):
        url = self.home_page + sub_url
        return get_page(url, self.proxies)

    def getTitle(self, page_code):
        pattern = '<input.*?name="atc_title" value="Re:(.*?)"'
        r = re.compile(pattern, re.S)
        title = r.findall(page_code)
        title = title[0].decode("gbk")
        title = title.replace('/', '_')
        title = title.replace(u"(\u539f\u521b)", "")
        return title

    def getPostURLs(self, page_code):
        pattern = "htm_data\/5\/\d{4}/\d+\.html"
        r = re.compile(pattern)
        links = r.findall(page_code)
        # make unique
        links = set(links)
        return links

    def get_image_url(self, page_code):
        image_hosts = [
                "http://www.datuimg.com/images.*?.[jpg|jpeg|gif]",
                "http://img.*?.uploadhouse.com/fileuploads.*?.[jpg|jpeg|gif]",
                "http://img.*?.showhaotu.com.*?.[jpg|jpeg|gif]",
                "http://img.*?.showhaotu.xyz.*?.[jpg|jpeg|gif]",
                "https://img.*?.showhaotu.com.*?.[jpg|jpeg|gif]",
                "http://s1.s8tu.com.*?.[jpg|jpeg|gif]",
                "http://p2.imageab.com.*?.[jpg|jpeg|gif]",
                "http://.*?ultraimg.com/images.*?.[jpg|jpeg|gif]",
                "http://img.*?.imagetwist.com.*?.[jpg|jpeg|gif]",
                "http://.*?tinypic.com.*?.[jpg|jpeg|gif]",
                "http://.*?chuantupian.com.*?.[jpg|jpeg|gif]",
                "http://.*?imgur.com.*?.[jpg|jpeg|gif]",
                "https://.*?media.tumblr.com.*?.[jpg|jpeg|gif]",
                "http://.*?imagebam.com.*?.[jpg|jpeg|gif]",
                "http://.*?kepkezelo.com/images.*?.[jpg|jpeg|gif]",
                "http://.*?directupload.net.*?.[jpg|jpeg|gif]",
                "http://.*?freeimage.us/image.php?id=",
                "http://.*?picpar.com.*?.[jpg|jpeg|gif]",
                "http://.*?imgaa.com.*?.[jpg|jpeg|gif]",
                "http://.*?imagefruity.com.*?.[jpg|jpeg|gif]",
                "http://.*?ihostimg.com.*?.[jpg|jpeg|gif]",
                "http://.*?imgspice.com.*?.[jpg|jpeg|gif]",
                "http://.*?anony.ws.*?.[jpg|jpeg|gif]",

                "http://.*?imagestorming.com/images.*?.[jpg|jpeg|gif]",
                "http://.*?bigtox.com.*?.[jpg|jpeg|gif]",
                "http://.*?ninja.*?.[jpg|jpeg|gif]",
                "http://.*?showss.net.*?.[jpg|jpeg|gif]",
                "http://.*?lookpic.com.*?.[jpg|jpeg|gif]",
                "http://.*?uploadfr.com.*?.[jpg|jpeg|gif]",
                "http://.*?gagr.com.*?.[jpg|jpeg|gif]",
                "http://.*?1024.photos.*?.[jpg|jpeg|gif|png]",
        ]
        pattern = "src='(" + "|".join(image_hosts) + ".*?)'"
        r = re.compile(pattern, re.S)
        return r.findall(page_code)

    def getTorrentAndDate(self, page_code):
        """
        contains torrent_url, post date
        """
        torrent_pattern = "(http://www.rmdown.com/link.php\?hash=.{43})"
        date_pattern = "Posted:(\d{4}-\d{2}-\d{2})"

        pattern = torrent_pattern + ".*?" + date_pattern
        r = re.compile(pattern, re.S)
        items = r.findall(page_code)
        return items

    def saveImage(self, image_url, file_name):
        print image_url
        try:
            request = requests.get(image_url, proxies=self.proxies, timeout=60)
            data = request.content
            f = open(file_name, "wb")
            f.write(data)
            f.close()
        except requests.exceptions.ConnectionError, e:
            log_file(self.cover_log, "can not download image",  image_url)
        except requests.exceptions.Timeout, e:
            log_file(self.cover_log, "connect timeout", image_url)
        except UnicodeDecodeError, e:
            log_file(self.cover_log, "can not decode url", image_url)

    def getTorrentValues(self, page_code):
        pattern = '<INPUT.*?ref.*?value="(.*?)".*?reff.*?value="(.*?)"'
        r = re.compile(pattern, re.S)
        items = r.findall(page_code)
        params = items[0]

        values = {
            "ref" : params[0],
            "reff" : params[1],
            "submit" : "download",
        }

        return values

    def saveTorrent(self, post_values, file_name):
        request = requests.post("http://www.rmdown.com/download.php", data = post_values, proxies=self.proxies)
        data = request.content
        f = open(file_name, "wb")
        f.write(data)
        f.close()

    def filterURL(self, image_url):
        filters = [
            "www.imagestorming.com",
            "bigtox.com",
            "ninja",
            "showss.net",
            "lookpic.com",
            "uploadfr.com",
            "gagr.com",
            "1024.photos",
        ]

        for f in filters:
            if image_url.find(f) != -1:
                return True 

        return False

    def downloadCovers(self, page_index="1"):
        clean_log(self.cover_log)
        page_index = int(page_index)
        while True:
            begin_log = "=========================executing page" + str(page_index) + "==============================" 
            print begin_log
            log_file(self.cover_log, begin_log)
            page_url = self.anime_page_prefix + str(page_index)
            page_code = get_page(page_url, self.proxies)
            post_urls = self.getPostURLs(page_code)
            post_urls = list(post_urls)
            for url in post_urls:
                post_page_code = cl.getCLPage(url)
                title = self.getTitle(post_page_code)

                file_name = os.path.join(self.cover_path, title + ".jpg")
                if is_file_exists(file_name):
                    continue

                image_urls = self.get_image_url(post_page_code)

                if len(image_urls) == 0:
                    log_file(self.cover_log, "can not find image url: ", self.home_page, url)
                    continue

                image_url = image_urls[0].strip()

                if self.filterURL(image_url) == True:
                    continue

                if len(image_urls) > 1:
                    log_file(self.cover_log, "more than one image url: ", self.home_page, url)

                self.saveImage(image_url, file_name)
            page_index += 1

    def download_torrents(self, date_arg=datetime.date.today()):
        if type(date_arg) == str:
            date_arg = get_date(date_arg)

        clean_log(self.cover_log)
        clean_log(self.torrent_log)
        page_index = 1
        should_continue = True
        while should_continue:
            should_continue = False
            page_url = self.anime_page_prefix + str(page_index)
            page_code = get_page(page_url, self.proxies)
            post_urls = self.getPostURLs(page_code)
            post_urls = list(post_urls)
            for url in post_urls:
                post_page_code = cl.getCLPage(url)
                title = self.getTitle(post_page_code)
                items = self.getTorrentAndDate(post_page_code)
                if len(items) == 0:
                    log_file(self.torrent_log, "can not find torrent url: ", self.home_page, url)
                    continue

                torrent_url = items[0][0]
                post_date = items[0][1]
                post_date = get_date(post_date)
                if post_date >= date_arg:
                    should_continue = True
                    folder = os.path.join(self.torrent_path, str(post_date))  
                    mkdir(folder)

                    #torrent
                    torrent_page_code = get_page(torrent_url, self.proxies)
                    post_values = cl.getTorrentValues(torrent_page_code)
                    torrent_name = os.path.join(folder, title + ".torrent")
                    cl.saveTorrent(post_values, torrent_name)

                    #image
                    image_name = os.path.join(folder, title + ".jpg")
                    if is_file_exists(image_name):
                        continue
                    image_urls = self.get_image_url(post_page_code)
                    if len(image_urls) == 0:
                        log_file(self.cover_log, "can not find image url: ", self.home_page, url)
                        continue
                    image_url = image_urls[0].strip()
                    if self.filterURL(image_url) == True:
                        continue
                    if len(image_urls) > 1:
                        log_file(self.cover_log, "more than one image url: ", self.home_page, url)
                    self.saveImage(image_url, image_name)
   
            page_index += 1

usage = """
usage:
    python -b for #today download
    python -b 1990-12-29 #for specific day download
    python -c #for cover download from page 1(deprecated)
    python -c 5 #for cover download from page 5(deprecated)
    python -t path #for test
"""

if __name__ == "__main__":
    argv = sys.argv

    if len(argv) < 2:
        print usage
        exit()

    cl = CL()
    if argv[1] == "-b":
        if len(argv) < 3:
            cl.download_torrents()
        else:
            cl.download_torrents(argv[2])
    elif argv[1] == "-c":
        pass
        #if len(argv) < 3:
        #    cl.downloadCovers()
        #else:
        #    cl.downloadCovers(argv[2])
    elif argv[1] == "-t":
        print cl.get_image_url(get_page(argv[2]))
    else:
        print usage
        exit()
