#coding:utf-8
import urllib2
import re
from bs4 import BeautifulSoup

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
    content = urllib2.urlopen(url)
    pattern = re.compile(r'<div id="episode">([\s\S]*?)</div></div>')
    html = content.read()
    match = pattern.search(html)
    html = match.group()
    pattern = re.compile(r'<li>([\s\S]*?)</li>')
    match = pattern.search(html)
    f.write('<h3>'+title+'</h3><ul>')
    f.write(match.group())
    f.write('</ul>')

matchTV_youku('http://www.youku.com/show_page/id_z6ae8ab240d5d11e4b8b7.html', '妙警贼探')
matchTV_tencent('http://v.qq.com/cover/8/8asm6qy0sj9gn4v/p0015qvsnvk.html', '再造淑女')
