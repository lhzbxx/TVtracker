# -*- coding=utf-8 -*-
import urllib2
import re
from bs4 import BeautifulSoup
import PyV8
import time
import sched
import sqlite3
import os
from anjuke import pinyin

conn = sqlite3.connect(r'database/eh.db')
conn.text_factory = str

converter = pinyin.Converter()
converter.load_word_file(os.path.dirname(os.path.abspath(__file__)) + '/words.txt')
tv = conn.execute('select link_youku, link_vqq, link_iqiyi from dream');


def matchTV_vqq(url, title):
    content = urllib2.urlopen(url).read()
    bs = BeautifulSoup(content)
    a_list = bs.find('ul', id='mod_videolist').find_all('a')
    j = 0
    for i in a_list:
        j = j + 1
        cursor = conn.execute("SELECT id from tv where tvname = ? and episode = ? and type = ?", (title, j, 'vqq',))
        if cursor.fetchall() == []:
            conn.execute("INSERT INTO tv (tvname, episode, address, type) VALUES (?, ?, ?, ?)", (title, j, 'http://v.qq.com' + i['href'], 'vqq'));
            ticks = time.time()
            conn.execute("INSERT INTO ping (name, episode, address, time) VALUES (?, ?, ?, ?)", (title, j, 'http://v.qq.com' + i['href'], int(ticks)));
            conn.commit()

def matchTV_youku(url):
    content = urllib2.urlopen(url).read()
    bs = BeautifulSoup(content)
    tmp = bs.find('div', id='episode')
    if tmp:
        a_list = tmp.find_all('a')
    else:
        return
    title = bs.find('span', "name").string
    enname = converter.convert(title, sc=False)
    # 标题的汉语拼音。
    imgsrc = bs.find('li', 'thumb').img['src']
    conn.execute("UPDATE dream set name = ?, enname = ?, imgsrc = ? where link_youku = ?", (title, enname, imgsrc, url));

def matchTV_iqiyi(url):
    pass


for i in tv:
    if i[0]:
        matchTV_youku(i[0])
    if i[1]:
        matchTV_vqq(i[1])
    if i[2]:
        matchTV_iqiyi(i[2])

conn.commit()