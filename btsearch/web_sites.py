#!/usr/bin/env python
# -*- coding:utf-8 -*-

web_list = [
    {
        "home" : "http://www.diaosisou.com",
        "page_format" : "list/%s/%d/rala_d",
        "post_pattern" : '<div class.*?href="(?P<post>/torrent/.*?)".*?(?P<title>.*?)</a></div>.*?<a href="(?P<magnet>magnet:\?xt=urn:btih:.*?) ">',
        "active" : True,
    },

    {
        "home" : "https://www.torrentkitty.tv",
        "page_format" : "search/%s/%d",
        "post_pattern" : '<tr><td class="name">.*?<a href="/(?P<post>information/.*?)" title="(?P<title>.*?)".*?<a href="(?P<magnet>magnet:\?xt=urn:btih:.*?)&dn=',
        "active" : True,
    },

    {
        "home" : "https://btso.pw",
        "page_format" : "search/%s/page/%d",
        "post_pattern" : '<a href="https://btso.pw/(?P<post>magnet/detail/hash/.*?)" title="(?P<title>.*?)">',
        "magnet_pattern" : 'href="(magnet:\?xt=urn:btih:.*?)&dn=',
        "active" : True,
    },

    {
        "home" : "https://bitsnoop.com",
        "page_format" : "search/all/%s/c/d/%d",
        "post_pattern" : '<li><div.*?<a href="/(?P<post>.*?-q.*?.html)(?P<title>.*?)</div></li>',
        "magnet_pattern" : '<a href="(magnet:\?xt=urn:btih:.*?)&dn=',
        "active" : True,
    },

    {
        "home" : "http://www.runbt.cc",
        "page_format" : "list/%s/%d/rala_d",
        "post_pattern" : '<div class=.*?href="http://www.runbt.cc/(?P<post>detail/.*?)">(?P<title>.*?)<a href="(?P<magnet>magnet:\?xt=urn:btih:.*?) ">',
        "magnet_pattern" : '<a href="(magnet:\?xt=urn:btih:.*?)">',
        "active" : True,
    },

    {
        "home" : "http://www.btdog.com.cn",
        "page_format" : "index.php/index/search/q/%s/p/%d.html",
        "post_pattern" : '<h3><a href="/(?P<post>index.php/index/dht/q/.*?/infohash/.*?.html)"(?P<title>.*?)<a href="(?P<magnet>magnet:\?xt=urn:btih:.*?)"',
        "active" : True,
    },

    {
        "home" : "http://www.zhaobt.org",
        "page_format" : "%s-first-asc-%d.html",
        "post_pattern" : '<div class="item-title">.*?<a href="/(?P<post>.*?.html)" rel="nofollow"(?P<title>.*?)</a>',
        "magnet_pattern" : '<a href="(magnet:\?xt=urn:btih:.*?)"',
        "active" : True,
    },

    {
        "home" : "http://www.zhongziso.com",
        "page_format" : "list/%s/%d",
        "post_pattern" : '<a href="/(?P<post>info-.*?)">(?P<title>.*?)</h4>',
        "magnet_pattern" : '<a href="(magnet:\?xt=urn:btih:.*?)"',
        "search_all" : True,
        "active" : True,
    },

    {
        "home" : "http://btdb.in",
        "page_format" : "q/%s/%d",
        "post_pattern" : '<a href="/(?P<post>torrent/.*?.html)" title="(?P<title>.*?)</a>.*?href="(?P<magnet>magnet:\?xt=urn:btih:.*?)&amp',
        "active" : True,
    },

    {
        "home" : "http://www.shenmidizhi.com",
        "page_format" : "list/%s-first-asc-%d",
        "post_pattern" : '<a class="title" href="/(?P<post>.*?)">(?P<title>.*?)href="(?P<magnet>magnet:\?xt=urn:btih:.*?)"',
        "active" : True,
    },

    {
        "home" : "http://www.bitkitty.org",
        "page_format" : "%s-first-asc-%d",
        "post_pattern" : '<div class="item-title">.*?<a href="/(?P<post>.*?.html)"(?P<title>.*?)</a>',
        "magnet_pattern" : '<a href="(magnet:\?xt=urn:btih:.*?)"',
        "active" : True,
    },

    {
        "home" : "http://www.btany.com",
        "page_format" : "search/%s-first-asc-%d",
        "post_pattern" : '<div class="item-title">.*?<a href="/(?P<post>detail/.*?)"(?P<title>.*?)<a href="(?P<magnet>magnet:\?xt=urn:btih:.*?)"',
        "proxies" : {},
        "active" : True,
    },

    {
        "home" : "https://sukebei.nyaa.se",
        "page_format" : "?page=search&term=%s&offset=%d",
        "post_pattern" : '<a href="//sukebei.nyaa.se/(?P<post>\?page=view&#38;tid=.*?)">(?P<title>.*?)</a>',
        "download_pattern" : '<a href="//sukebei.nyaa.se/(\?page=download&#38;tid=.*?)" ',
        "download_title" : '<title>(.*?)</title>',
        "active" : True,
    },

    {
        "home" : "http://cilidb.com",
        "page_format" : "page/%s/%d-0-0.shtml",
        "post_pattern" : '<dt>.*?<a href=\'http://cilidb.com/(?P<post>magnet.*?shtml)\'(?P<title>.*?)</dt>',
        "magnet_pattern" : '<a href=\'(magnet:\?xt=urn:btih:.*?)&amp;',
        "active" : True,
    },

    {
        "home" : "http://www.tokyotosho.info",
        "page_format" : "search.php?terms=%s&page=%d",
        "post_pattern" : '<a href="(?P<magnet>magnet:\?xt=urn:btih:.*?)&amp.*?type="application/x-bittorrent" href="(?P<post>.*?)">(?P<title>.*?)<span class="s">',
        "active" : True,
    },

    {
        "home" : "https://btdig.com",
        "page_format" : "search?q=%s&p=%d&order=0",
        "post_pattern" : '<a href="https://btdig.com/(?P<post>search\?info_hash=.*?)&amp.*?">(?P<title>.*?)<a href="(?P<magnet>magnet:\?xt=urn:btih:.*?)&amp',
        "page_num_type" : 2,
        "active" : True,
    },
    
    {
        "home" : "http://www.cilibaba.com",
        "page_format" : "search/%s/?c=&s=relavance&p=%d",
        "post_pattern" : '<tr><td class="x-item">.*?<a title="(?P<title>.*?)" class="title" href="(?P<post>/h/.*?)">',
        "magnet_pattern" : '"info_hash": "(.*?)",',
        "Cilibaba" : True,
        "proxies" : {},
        "active" : False,
    },
    
    {
        "home" : "http://www.zhizhucili.net",
        "page_format" : "so/%s-first-asc-%d",
        "post_pattern" : '<a href="/(?P<post>bt/.*?.html)"(?P<title>.*?)</a>',
        "magnet_pattern" : '<a href="(magnet:\?xt=urn:btih:.*?)"',
        "proxies" : {},
        "active" : True,
    },
]
