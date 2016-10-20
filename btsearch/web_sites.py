#!/usr/bin/env python
# -*- coding:utf-8 -*-

web_list = [
    {
        "home" : "http://www.btcrawler.com",
        "page_format" : "%s-first-asc-%d",
        "post_pattern" : '<a href="/(.*?)" target="_blank">',
        "magnet_pattern" : '(magnet:\?xt=urn:btih:.*?)&dn=',
        "active" : False,
    },

    {
        "home" : "http://www.zhongziso.com",
        "page_format" : "list/%s/%d",
        "post_pattern" : '<a href="/(info-.*?)">',
        "magnet_pattern" : '<a href="(magnet:\?xt=urn:btih:.*?)"',
        "active" : False,
    },

    {
        "home" : "http://www.shenmidizhi.com",
        "page_format" : "list/%s-first-asc-%d",
        "post_pattern" : '<a class="title" href="/(.*?)">',
        "magnet_pattern" : 'href=\'(magnet:\?xt=urn:btih:.*?)\'>',
        "active" : True,
    },

    {
        "home" : "http://www.cilibaba.com",
        "page_format" : "search/%s/?c=&s=create_time&p=%d",
        "post_pattern" : '<a title=".*?" class="title" href="/h/(.*?)">',
        "magnet_pattern" : '"info_hash": "(.*?)",',
        "active" : True,
        "Cilibaba" : True,
    },

    {
        "home" : "http://www.diaosisou.com",
        "page_format" : "list/%s/%d/time_d",
        "post_pattern" : 'href="/(torrent/.*?)">',
        "magnet_pattern" : '<a href="(magnet:\?xt=urn:btih:.*?)">',
        "active" : True,
    },

    {
        "home" : "http://bt2.bt87.cc",
        "page_format" : "search/%s_ctime_%d.html",
        "post_pattern" : 'target="_blank" href="/(.*?.html)',
        "magnet_pattern" : 'href="(magnet:\?xt=urn:btih:.*?)"', 
        "active" : True,
    },

    {
        "home" : "http://www.bitkitty.org",
        "page_format" : "%s-first-asc-%d",
        "post_pattern" : '<a href="/(.*?.html)"',
        "magnet_pattern" : '<a href="(magnet:\?xt=urn:btih:.*?)"',
        "active" : True,
    },

    {
        "home" : "https://btso.pw",
        "page_format" : "search/%s/page/%d",
        "post_pattern" : '<a href="https://btso.pw/(magnet/detail/hash/.*?)"',
        "magnet_pattern" : 'href="(magnet:\?xt=urn:btih:.*?)&dn=',
        "active" : True,
    },

    {
        "home" : "https://bitsnoop.com",
        "page_format" : "search/all/%s/c/d/%d",
        "post_pattern" : '<a href="/(.*?-q.*?.html)',
        "magnet_pattern" : '<a href="(magnet:\?xt=urn:btih:.*?)&dn=',
        "active" : True,
    },

    {
        "home" : "http://www.zhaobt.org",
        "page_format" : "%s-first-asc-%d.html",
        "post_pattern" : '<a href="/(.*?.html)" rel="nofollow"',
        "magnet_pattern" : '<a href="(magnet:\?xt=urn:btih:.*?)"',
        "active" : True,
    },


    {
        "home" : "http://www.btbadboy.com",
        "page_format" : "search.php?keyword=%s&p=%d&mode=1",
        "post_pattern" : '<a href="/(torrent/.*?)"',
        "magnet_pattern" : '<a href="(magnet:\?xt=urn:btih:.*?)&xl=',
        "active" : True,
    },

    {
        "home" : "http://www.bt177.net",
        "page_format" : "word/%s_%d.html",
        "post_pattern" : '<a href="/(read/.*?.html)"',
        "magnet_pattern" : '<a href="http://ggo.la/(magnet:\?xt=urn:btih:.*?)">',
        "active" : True,
    },

    {
        "home" : "http://www.btany.com",
        "page_format" : "search/%s-first-asc-%d",
        "post_pattern" : '<a href="/(detail/.*?)"',
        "magnet_pattern" : '<a href="(magnet:\?xt=urn:btih:.*?)">',
        "active" : True,
    },
    
    {
        "home" : "http://www.zhizhu88.com",
        "page_format" : "so/%s-first-asc-%d",
        "post_pattern" : '<a href="/(bt/.*?.html)"',
        "magnet_pattern" : 'href="(magnet:\?xt=urn:btih:.*?)&dn=',
        "active" : True,
    },

    {
        "home" : "http://www.oooc.net",
        "page_format" : "?q=%s&offset=%d",
        "post_pattern" : '<a href="/(.*?/.*?.html)"',
        "magnet_pattern" : '<a href="(magnet:\?xt=urn:btih:.*?)&amp;',
        "active" : True,
        "Oooc" : True,
    },

    {
        "home" : "http://www.runbt.cc",
        "page_format" : "list/%s/%d",
        "post_pattern" : 'href="http://www.runbt.cc/(detail/.*?)">',
        "magnet_pattern" : '<a href="(magnet:\?xt=urn:btih:.*?)">',
        "active" : True,
    },
]
