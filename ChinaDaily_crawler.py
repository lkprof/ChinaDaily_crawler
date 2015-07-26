#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import re
import requests
from bs4 import BeautifulSoup

from multiprocessing import Pool

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'}

def create_urls():
    urls = []
    url_start = "http://searchen.chinadaily.com.cn/search?sortBy=-publishtime&"\
    "view=allsitesppublished&classify=en&navigation=&drillDown=&drillUp=&"\
    "offset="
    url_end = "&query=movie"
    for i in range(1,140):
        url = url_start + str(i) + url_end
        urls.append(url)
    #print urls
    return urls

def download_page(url):

    try:
        page = requests.get(url,timeout = 10,headers = headers)
        page.encoding = 'utf-8'
        page = page.content
        soup = BeautifulSoup(page)
        # page_use_soup_text = soup.get_text()


        enpproperty_patt = r'<!--enpproperty([\s\S]*?)/enpproperty-->'
        enpproperty = re.findall(enpproperty_patt, str(soup))
        # print enpproperty
        enpproperty_content = enpproperty[0]
        # print enpproperty_content.decode('gbk').encode('utf-8')

        enpcontent_patt = r'<!--enpcontent-->([\s\S]*?)<!--/enpcontent-->'
        enpcontent = re.findall(enpcontent_patt, str(soup))
        # print enpcontent
        enpcontent_content = enpcontent[0]


        title_patt = r'<title>(.*?)</title>'
        time_patt = r'<date>(.*?)</date>'
        author_patt = r'<author>(.*?)</author>'
        # author_name_patt = ur'<meta name="author" content="([\s\S]*?)"/>'
        content_patt = r'<p(.*?)>(.*?)</p>'
        keyword_patt = r'<keyword>(.*?)</keyword>'

        title = re.findall(title_patt, str(enpproperty_content))
        time = re.findall(time_patt, str(enpproperty_content))

        author = re.findall(author_patt, str(enpproperty_content))
        author = author[0]
        # if author=='':
        #     author_name = re.findall(author_name_patt, str(soup))
        #     print author_name

        keyword = re.findall(keyword_patt, str(enpproperty_content))
        content = re.findall(content_patt, str(enpcontent_content))
        # print title[0]
        # print author[0]
        # print content[0]
        article = ''
        for part_article in content:
            # print part_article[1]
            article += part_article[1] + '\n'
        text_content = title[0] + '\n' + time[0] + '\n' + author + '\n' + keyword[0] + '\n' + article
        # print text_content
        title_s = str(title[0])
        title_s = title_s.replace('\\','')
        title_s = title_s.replace('/','')
        title_s = title_s.replace('*','')
        title_s = title_s.replace('<','')
        title_s = title_s.replace('>','')
        title_s = title_s.replace(':','')
        title_s = title_s.replace('|','')
        title_s = title_s.replace('"','')
        title_s = title_s.replace('?','')
        text_name = title_s + '.txt'
        # print 'downloading...'
        with open(text_name,'w') as fw:
            fw.write(text_content)
        print 'downloading finish'
    except requests.HTTPError, e:
        print HTTPError,':',e

def crawl_ChinaDaily(url):
    try:
        page = requests.get(url,timeout = 10,headers = headers)
        page.encoding = 'utf-8'
        page = page.content
        soup = BeautifulSoup(page)
        urls_names_patt = r'<div class="cs_sear_list_tit"><a href="(.*?)" target="_blank">'
        urls_names = re.findall(urls_names_patt, str(soup))
        for url in urls_names:
            if url=='':
                pass
            else:
                # print url
                download_page(url)
            # pathname = 'D://python_learn//ChinaDaily_crawler//' + url[-12:]
            # urllib.urlretrieve(url, pathname)

    except Exception , what:
        print what

if __name__ == '__main__':
    urls = create_urls()

    pool = Pool(20)
    pool.map(crawl_ChinaDaily, urls)
    pool.close()
    pool.join()

