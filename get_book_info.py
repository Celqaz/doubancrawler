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
headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
        'Connection': 'keep-alive',
        'Referer': 'http://www.baidu.com/'
    }
def get_book_sid(bookname):
    en_bookname = urllib.parse.quote(bookname)
    url = 'https://www.douban.com/search?cat=1001&q='+en_bookname
    req = urllib.request.Request(url=url, headers=headers)
    res = urllib.request.urlopen(req)

    html = res.read().decode('utf-8')
    
    # BS4
    soup = BeautifulSoup(html,'lxml')
    id_tag = soup.find('h3').a['onclick']
    # print(id_tag)
    sid = re.search('sid:[ ]([\d]*)',id_tag).group(1)
    # print(sid)
    # wait
    time.sleep(np.random.rand()*5)
    
    return bookname,sid
# get_book_sid('王尔德童话')



def get_book_data(sid):
    book_data = {}
    time.sleep(np.random.rand()*5)
    url = 'https://book.douban.com/subject/'+sid
    req = urllib.request.Request(url=url, headers=headers)
    res = urllib.request.urlopen(req)

    html = res.read().decode('utf-8')
    
    # BS4
    soup = BeautifulSoup(html,'lxml')
    # 评分-数字
    book_data["rating"] = float(soup.find(id='interest_sectl').find(class_='ll rating_num').get_text())
    # 评分人数-整型
    book_data["rating_people"] = int(soup.find(id='interest_sectl').find(class_='rating_people').get_text()[:-3])
    # 作者
    author = soup.find(id='info').a.get_text()
    book_data["author"] = ''.join(author.split())
    # 图书简介，作者简介 intro
    intro = soup.find_all(class_='intro')
    try:
        book_data["book_summary"] = intro[0].get_text()[1:]
    except:
        book_data["book_summary"] = "暂无图书简介"
    try:
        book_data["author_summary"] = intro[1].get_text()[1:]
    except:
        book_data["author_summary"] = "暂无作者简介"

    # book_data["book_summary"] = soup.select("#link-report > span:nth-child(1) > div:nth-child(2)")[0].get_text()
    # book_data["author_summary"] = soup.select("div.indent:nth-child(6) > div:nth-child(1) > div:nth-child(2)")[0].get_text()
    # book_data["book_summary"] = soup.find(class_='intro').get_text()
    # book_data["author_summary"] = soup.select('div.indent:nth-child(6) > div:nth-child(1) > div:nth-child(2)')[0].get_text()
    # book_data["author_summary"] = soup.findAll
    # print(book_data["book_summary"])
    # print(book_data["author_summary"]) 


    return book_data

# get_book_data('5337254')
# get_book_data('6781808')
# get_book_data('2154960')