# -*- coding:utf-8 -*-
import urllib
import urllib2
import re

class QSBK:
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'

        self.headers = {'User-Agent' : self.user_agent }

        self.stories = []

        self.enable = False

    def getPage(self, pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            request = urllib2.Request(url, headers = self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('utf-8')
            return pageCode
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"连接失败，发生错误", e.reason
                return None

    def getPageItems(self, pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print u"页面加载失败...."
            return None
        pattern = re.compile('<div.*?author clearfix">.*?<div.*?content">(.*?)</div>.*?<div(.*?)stats">.*?</div>', re.S)
        items = re.findall(pattern, pageCode)
        pageStories = []
        for item in items:
            if not re.search("thumb", item[1]):
                replaceBR = re.compile('<br/>')
                text = re.sub(replaceBR, "\n", item[0])
                pageStories.append([text.strip()])

        return pageStories
    
    def loadPage(self):
        if self.enable == True:
            if len(self.stories) < 2:
                pageStories = self.getPageItems(self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex += 1

    def getOneStory(self, pageStories, page):
        for story in pageStories:
            cin = raw_input()
            self.loadPage()
            if cin == "Q":
                self.enable = False
                return
            print story[0]

    def start(self):
        self.enable = True
        self.loadPage()
        nowPage = 0
        while self.enable:
            if len(self.stories) > 0:
                pageStories = self.stories[0]
                nowPage += 1
                del self.stories[0]
                self.getOneStory(pageStories, nowPage)

s = QSBK()
s.start()
