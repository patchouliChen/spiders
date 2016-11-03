# -*- coding:utf-8 -*-
import os
import requests
import datetime
import logging

logger = None

def setup_logging(name="Default"):
    global logger
    logger = logging.getLogger(name) 
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)

def log(*strings, **kwargs):
    global logger
    if logger == None:
        setup_logging()

    level = kwargs.pop("level", logging.INFO)
    logger.log(level, " ".join(s for s in strings))

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
    url = url.replace("#38;", "")
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
    lines = f.readlines()
    lines = [line.rstrip() for line in lines]
    f.close()
    return lines
