# -*- coding=utf-8 -*-
import urllib2
import re
from bs4 import BeautifulSoup
import PyV8
import time
import sched
import sqlite3

conn = sqlite3.connect(r'database/eh.db')

def matchTV_vqq(url, title):
    content = urllib2.urlopen(url).read()
    bs = BeautifulSoup(content)
    a_list = bs.find('ul', id='mod_videolist').find_all('a')
    imgsrc = bs.find('ul')
    j = 0
    for i in a_list:
        j = j + 1
        cursor = conn.execute("SELECT id from tv where tvname = ? and episode = ? and type = ?", (title, j, 'vqq',))
        if cursor.fetchall() == []:
            conn.execute("INSERT INTO tv (tvname, episode, address, type) VALUES (?, ?, ?, ?)", (title, j, 'http://v.qq.com' + i['href'], 'vqq'));
            ticks = time.time()
            conn.execute("INSERT INTO ping (name, episode, address, time) VALUES (?, ?, ?, ?)", (title, j, 'http://v.qq.com' + i['href'], int(ticks)));

def matchTV_youku(url, title):
    try:
        content = urllib2.urlopen(url).read()
    except Exception, e:
        return
    bs = BeautifulSoup(content)
    tmp = bs.find('div', id='episode')
    if tmp:
        a_list = tmp.find_all('a')
    else:
        return
    j = len(a_list)
    a_list.reverse()
    for i in a_list:
        cursor = conn.execute("SELECT id from tv where tvname = ? and episode = ? and type = ?", (title, j, 'youku',))
        if cursor.fetchall() == []:
            conn.execute("INSERT INTO tv (tvname, episode, address, type) VALUES (?, ?, ?, ?)", (title, j, i['href'], 'youku'));
            ticks = time.time()
            conn.execute("INSERT INTO ping (name, episode, address, time) VALUES (?, ?, ?, ?)", (title, j, i['href'], int(ticks)));
        else:
            break
        j = j - 1

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

def scan():
    tv = conn.execute('select name, link_youku, link_vqq, link_iqiyi from dream');
    for i in tv:
        print i[0]
        if i[1]:
            matchTV_youku(i[1], i[0])
        if i[3]:
            matchTV_iqiyi(i[3], i[0])
        if i[2]:
            matchTV_vqq(i[2], i[0])
    conn.commit()

def init(inc):
    # schedule.enter(inc, 0, init, (inc,))
    scan()

schedule = sched.scheduler(time.time, time.sleep)
schedule.enter(0, 0, init, (30,))
schedule.run()
# matchTV_youku('http://www.youku.com/show_page/id_z6ae8ab240d5d11e4b8b7.html', '妙警贼探第六季')
# matchTV_tencent('http://v.qq.com/cover/8/8asm6qy0sj9gn4v/p0015qvsnvk.html', '再造淑女第一季')
# matchTV_iqiyi('http://www.iqiyi.com/a_19rrifrm2n.html', '爱情公寓4')
# matchTV_tudou('http://www.tudou.com/albumcover/SgcffZHoj-I.html', '神盾局特工第二季')
# matchTV_acfun('http://www.acfun.tv/a/aa1464868', u'生活大爆炸第八季')
