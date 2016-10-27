# -*- coding:utf-8 -*-
import os
import requests
import datetime

def mkdir(path):
    path = path.strip()
    isExists = os.path.exists(path)
    if not isExists:
        os.mkdir(path)
        return True
    else:
        return False

def is_file_exists(fileName):
    return os.path.exists(fileName) 

def get_page(url, proxies={}):
    url = url.replace("#38;", "")
    print "...getting page code...", url
    try:
        headers={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"}
        request = requests.get(url=url, proxies=proxies, timeout=10.0, headers = headers)
    except requests.exceptions.Timeout:
        return get_page(url, proxies)
    except requests.exceptions.ConnectionError:
        return get_page(url, proxies)
    except requests.exceptions.ContentDecodingError:
        return get_page(url, proxies)
    return request.content

def post_page(url, data={}, proxies={}):
    print "...posting page code...", url
    try:
        headers={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"}
        request = requests.post(url=url, data=data, proxies=proxies, timeout=10.0, headers = headers)
    except requests.exceptions.Timeout:
        return post_page(url, data, proxies)
    except requests.exceptions.ConnectionError:
        return post_page(url, data, proxies)
    except requests.exceptions.ContentDecodingError:
        return post_page(url, data, proxies)
    return request.content

def clean_log(fileName):
    f = open(fileName, "w")
    f.truncate()
    f.close()

def log_file(fileName, *arg):
    log_text = ''.join(arg)
    log_text += "\n"
    f = open(fileName, "a")
    f.write(log_text)
    f.close()

def get_date(dateString):
    """
    format: 1990-12-29
    """
    year, month, day = dateString.split("-")
    year = int(year)
    month = int(month)
    day = int(day)
    return datetime.date(year, month, day)

def read_lines(filename):
    f = open(filename, "r")
    keywords = f.readlines()
    keywords = [keyword.rstrip() for keyword in keywords]
    f.close()
    return keywords
