# -*- coding=utf-8 -*-
import urllib2
import re
from bs4 import BeautifulSoup
import PyV8

f = open('TVtracker.html', 'w')

def matchTV_tencent(url, title):
    content = urllib2.urlopen(url).read()
    bs = BeautifulSoup(content)
    a_list = bs.find('ul', id='mod_videolist').find_all('a')
    j = 0
    for i in a_list:
        j = j + 1
        print 'http://v.qq.com' + i['href']

def matchTV_youku(url, title):
    content = urllib2.urlopen(url).read()
    bs = BeautifulSoup(content)
    a_list = bs.find('div', id='episode').find_all('a')
    j = 0
    for i in a_list:
        j = j + 1
        print i['href']

def matchTV_iqiyi(url, title):
    content = urllib2.urlopen(url).read()
    bs = BeautifulSoup(content)
    a_list = bs.find_all('a', rseat='jj-list-text-video-0923')
    j = 0
    for i in a_list:
        j = j + 1
        print i['href']

def matchTV_tudou(url, title):
    # 妈了个屯，土豆用的JS动态生成的网页，先放弃这个源。
    content = urllib2.urlopen(url).read()
    bs = BeautifulSoup(content)
    a_list = bs.find('div', class_='series_panel current').find_all('a')
    j = 0
    for i in a_list:
        j = j + 1
        print i['href']

def matchTV_acfun(url, title):
    # ACFUN和土豆一个尿性，先放弃。
    content = urllib2.urlopen('http://static.acfun.mm111.net/dotnet/20130418/??script/jquery.2.1.1.min.js,script/prepare.0.0.5.min.js').read() + urllib2.urlopen('http://static.acfun.mm111.net/dotnet/20130418/??script/core.0.3.14.min.js,script/ready.0.3.23.min.js').read() + urllib2.urlopen('http://static.acfun.mm111.net/dotnet/20130418/script/album/album.min.js?date=1415866626945').read()
    ctxt = PyV8.JSContext()
    ctxt.enter()
    func = ctxt.eval(content.decode('utf-8'))
    print func()
    # bs = BeautifulSoup(content)
    # a_list = bs.find('div', id='block-list-sp').find_all('a')
    # j = 0
    # for i in a_list:
    #     j = j + 1
    #     print i['href']

# matchTV_youku('http://www.youku.com/show_page/id_z6ae8ab240d5d11e4b8b7.html', '妙警贼探第六季')
# matchTV_tencent('http://v.qq.com/cover/8/8asm6qy0sj9gn4v/p0015qvsnvk.html', '再造淑女第一季')
# matchTV_iqiyi('http://www.iqiyi.com/a_19rrifrm2n.html', '爱情公寓4')
# matchTV_tudou('http://www.tudou.com/albumcover/SgcffZHoj-I.html', '神盾局特工第二季')
# matchTV_acfun('http://www.acfun.tv/a/aa1464868', u'生活大爆炸第八季')
