# coding: utf-8
import urllib.request, urllib.parse
from bs4 import BeautifulSoup
import re
import numpy as np
import time

def get_book_list():
    book_list = []
    f = open("books.txt")
    lines = f.readlines()
    for line in lines:
        book_list.append(line.strip('\n'))

    return book_list

def get_book_sid(bookname):
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
        'Connection': 'keep-alive',
        'Referer': 'http://www.baidu.com/'
    }
    # bookname = '孽子'
    time.sleep(np.random.rand()*5)
    en_bookname = urllib.parse.quote(bookname)
    url = 'https://www.douban.com/search?cat=1001&q='+en_bookname
    req = urllib.request.Request(url=url, headers=headers)
    res = urllib.request.urlopen(req)

    html = res.read().decode('utf-8')

    # BS4
    soup = BeautifulSoup(html,'lxml')
    id = soup.find('h3').a['onclick']
    sid = re.search('sid:([ ][\d]*)',id).group(1)
    
    return bookname,sid

bl = get_book_list()
# print(bl)
for i in bl:
    print(get_book_sid(i))