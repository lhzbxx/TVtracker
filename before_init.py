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

for i in range(1, 30):
    url = "http://www.youku.com/v_olist/c_97_g__a__sg__mt__lg__q__s_6_r__u_0_pt_0_av_0_ag_0_sg__pr__h__d_1_p_"+str(i)+".html"
    content = urllib2.urlopen(url).read()
    bs = BeautifulSoup(content)
    a_list = bs.find_all('div', 'p-link')
    for j in a_list:
        print j.a['href']
        conn.execute("INSERT INTO dream (link_youku) VALUES (?)", (j.a['href'],));
    conn.commit()