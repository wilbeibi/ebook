#!/usr/bin/env python
# coding=utf-8
import os
import sys
import requests
import json

class DoubanBookApi:
    base_url = 'https://api.douban.com/v2/book/'
    keyword = 'bookname'
    search_url = base_url + 'search?q=' + keyword + '&fields=id,title,rating,url' 
    subject_url = 'https://book.douban.com/subject/'
    @classmethod
    def SearchUrl(cls, bookname):
        return cls.search_url.replace(cls.keyword, bookname) 

    @classmethod
    def BookUrl(cls, bookid):
        return cls.subject_url + str(bookid)

class DoubanBook:
    def __init__(self, name):
        self.name = name.decode('gbk').encode('utf8')
    def SearchBook(self):
        try:
            response =  requests.get(DoubanBookApi.SearchUrl(self.name))
            json_data = json.loads(response.text)
            books = json_data['books']
            first = books[0]
            self.rating = first['rating']['average']
            self.id = first['id']
            self.url = first['url']
        except Exception as e:
            print e.message, e.args
            self.rating = None
            self.id = None
            self.url = None
    def Name(self):
        return self.name
    def Rating(self):
        return self.rating
    def Id(self):
        return self.id
    def Url(self):
        return DoubanBookApi.BookUrl(self.id)

class TOC:
    scriptName = os.path.basename(__file__)
    scriptDir = os.path.dirname(os.path.realpath(__file__))
    output_file = 'readme.md'
    output_path = os.path.join(scriptDir, output_file)
    exclude_files = [output_file, scriptName]
    exclude_dirs = []
    preface = '''
# 计算机专业书籍

**注：尊重知识产权，购买正版！这些电子文档均来自网络，如有侵权，请联系我予以删除。**

******
    '''
    
    @classmethod
    def generate(cls):
        fd = file(cls.output_path, 'w')
        orig_stdout = sys.stdout
        sys.stdout = fd
        print cls.preface
        startpath = cls.scriptDir
        for root, dirs, files in os.walk(startpath):
            files = [f for f in files if f[0] != '.' and f not in cls.exclude_files]
            dirs[:] = [d for d in dirs if d[0] != '.' and d not in cls.exclude_dirs]
    
            level = root.replace(startpath, '').count(os.sep)
            header = '#' * (level+1) + ' '
            print('\n{}{}/'.format(header, os.path.basename(root)))
            list_n = 0
            for f in files:
                list_n += 1
                f = os.path.splitext(f)[0]
                a = DoubanBook(f)
                a.SearchBook()
                item = '{}. {} [Douban {}]({})'.format(list_n, f, a.Rating(), a.Url())
                print item.decode('gbk').encode('utf-8')   
        sys.stdout = orig_stdout
        
TOC.generate()