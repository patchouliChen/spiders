#!/usr/bin/env python
# -*- coding:utf-8 -*-

backup = [
    {
        "home" : "https://www.nyaa.se/",
        "page_format" : "\?page=search&term=%soffset=%d",
        "post_pattern" : '<a href="//sukebei.nyaa.se/(\?page=view&#38;tid=.*?)">',
        "magnet_pattern" : '',
        "active" : True,
    },

    {
        "home" : "http://www.picktorrent.com",
        "page_format" : "torrents/%s",
        "post_pattern" : '<td>.*?<a href="/(?P<post>download/.*?.html)">(?P<title>.*?)</td>',
        "magnet_pattern" : 'href="(magnet:\?xt=urn:btih:.*?)&dn=',
        "page_num_type" : 2,
        "http_method" : 2,
        "active" : False,
    },

    {
        "home" : "http://filedron.com",
        "page_format" : "%s",
        "post_pattern" : '<td>.*?<a href="/(?P<post>info/.*?.html)">(?P<title>.*?)</td>',
        "magnet_pattern" : 'href="(magnet:\?xt=urn:btih:.*?)&dn=',
        "page_num_type" : 2,
        "active" : False,
        "http_method" : 2,
    },
]
