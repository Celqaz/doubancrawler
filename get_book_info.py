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
    try:
        # 评分-数字
        book_data["rating"] = float(soup.find(id='interest_sectl').find(class_='ll rating_num').get_text())
        # 评分人数-整型
        book_data["rating_people"] = int(soup.find(id='interest_sectl').find(class_='rating_people').get_text()[:-3])
    except:
        book_data["rating"] = -1
        book_data["rating_people"] = 0
    # 作者
    author = soup.find(id='info').a.get_text()
    book_data["author"] = ''.join(author.split())
    # 图书简介 intro
    # debug
    # try:  
    #     # 有 展开全部
    #     book_data["book_summary"] = soup.select('#link-report > span:nth-child(2) > div:nth-child(1) > div:nth-child(2)')[0].get_text().replace("\n", "")
    # except:
    #     try:
    #         intro = soup.find_all(class_='intro')
    #         book_data["book_summary"] = intro[1].get_text()[1:].replace("\n", "")
    #     except:
    #         book_data["book_summary"] = "暂无图书简介"
    
    # # 作者简介
    # try:
    #     # 有 展开全部
    #     book_data["author_summary"] = soup.select('div.indent:nth-child(6) > span:nth-child(2) > div:nth-child(2)')[0].get_text().replace("\n", "")
    # except:
    #     try:
    #         intro = soup.find_all(class_='intro')
    #         book_data["author_summary"] = intro[3].get_text()[1:].replace("\n", "")
    #     except:
    #         book_data["author_summary"] = "暂无作者简介"

    # ddddddd
    intro = soup.find_all(class_='intro')
    # print(len(intro))
    # intro = soup.find_all(class_='intro')
    # try:  
    #     # 有 展开全部
    #     # intro = soup.find_all(class_='intro')
    #     book_data["book_summary"] = intro[0].get_text()[1:].replace("\n", "")
    #     if book_data["book_summary"][-6:] == '(展开全部)':
    #         book_data["book_summary"] = intro[1].get_text()[1:].replace("\n", "")
    #         book_data["author_summary"] = intro[2].get_text()[1:].replace("\n", "")
    #         if book_data["author_summary"][-6:] == '(展开全部)':
    #             book_data["author_summary"] = intro[3].get_text()[1:].replace("\n", "")
    #     else:
    #         book_data["author_summary"] = intro[1].get_text()[1:].replace("\n", "")
    # except:
    #     print(intro)
    #     book_data["book_summary"] = "暂无图书简介"
    
    # test
    cont_n = 0
    cont_title = soup.find_all('h2')[0].get_text().replace("\n", "")
    # print(cont_title[0:4])
    if cont_title[0:4] == '内容简介':
        try:
            book_data["book_summary"] = intro[cont_n].get_text()[1:].replace("\n", "")
            if book_data["book_summary"][-6:] == '(展开全部)':
                cont_n = 1
                book_data["book_summary"] = intro[cont_n].get_text()[1:].replace("\n", "")
            # print(book_data["book_summary"])
        except:
            cont_n = -1
            book_data["book_summary"] = "暂无图书简介"
            # print(book_data["book_summary"])
        try: 
            book_data["author_summary"] = intro[cont_n+1].get_text()[1:].replace("\n", "")
            if book_data["author_summary"][-6:] == '(展开全部)':
                book_data["author_summary"] = intro[cont_n+2].get_text()[1:].replace("\n", "")
        except:
            book_data["author_summary"] = "暂无作者简介"
    if cont_title[0:4] == '作者简介':
        book_data["book_summary"] = "暂无图书简介"
        try:
            book_data["author_summary"] = intro[cont_n].get_text()[1:].replace("\n", "")
            if book_data["author_summary"][-6:] == '(展开全部)':
                # cont_n = 1
                book_data["author_summary"] = intro[cont_n+1].get_text()[1:].replace("\n", "")
        except:
            cont_n = -1
            book_data["author_summary"] = "暂无作者简介"
    if  (cont_title[0:4] != '内容简介') and (cont_title[0:4] != '作者简介'):
        book_data["book_summary"] = "暂无图书简介"
        book_data["author_summary"] = "暂无作者简介"

    # cont_n = 0
    # try:
    #     book_data["book_summary"] = intro[cont_n].get_text()[1:].replace("\n", "")
    #     if book_data["book_summary"][-6:] == '(展开全部)':
    #         cont_n = 1
    #         book_data["book_summary"] = intro[cont_n].get_text()[1:].replace("\n", "")
    # except:
    #     cont_n = -1
    #     book_data["book_summary"] = "暂无图书简介"
    
    # try: 
    #     book_data["author_summary"] = intro[cont_n+1].get_text()[1:].replace("\n", "")
    #     if book_data["author_summary"][-6:] == '(展开全部)':
    #         book_data["author_summary"] = intro[cont_n+2].get_text()[1:].replace("\n", "")
    # except:
    #     book_data["author_summary"] = "暂无作者简介"
    

    
    # try:
    #     .intro
    #     book_data["book_summary"] = ('#link-report > span:nth-child(1) > div:nth-child(2)')[0].get_text().replace("\n", "")
    #     if book_data["book_summary"][-6:] == '(展开全部)':
    #         book_data["book_summary"] = ('span.all > div:nth-child(1) > div:nth-child(2)')[0].get_text().replace("\n", "")
    # except:
    #     book_data["book_summary"] = "暂无内容简介"
    
    # try:
    #     book_data["author_summary"] = ('div.indent:nth-child(5) > div:nth-child(1) > div:nth-child(2)')[0].get_text().replace("\n", "")
    #     if book_data["author_summary"][-6:] == '(展开全部)':
    #         book_data["author_summary"] = ('div.indent:nth-child(5) > span:nth-child(2) > div:nth-child(2)')[0].get_text().replace("\n", "")
    # except:
    #     book_data["author_summary"] = "暂无作者简介"
    # 作者简介
    # try:
    #     # 有 展开全部
    #     book_data["author_summary"] = soup.select('div.indent:nth-child(6) > span:nth-child(2) > div:nth-child(2)')[0].get_text().replace("\n", "")
    # except:
    #     try:
    #         intro = soup.find_all(class_='intro')
    #         book_data["author_summary"] = intro[3].get_text()[1:].replace("\n", "")
    #     except:
    #         book_data["author_summary"] = "暂无作者简介"


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
# get_book_data('1902852')