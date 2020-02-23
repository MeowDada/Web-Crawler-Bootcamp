from push import Push
from lxml import etree
from article import Article
import requests
import csv
import re
from bs4 import BeautifulSoup

PTTURL_PREFIX = 'https://www.ptt.cc'

headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Mobile Safari/537.36',
}

cookies = {
    'over18': '1'
}

# 將作者資訊的暱稱去除，僅留帳號ID
def extract_author(author):
    return re.search('[a-zA-Z0-9]+', author).group(0)

class PTTCrawler:
    def __init__(self):
        pass

    # 給定欲爬取之批踢踢看版，與欲爬取頁面深度，回傳一個陣列包含所有爬取文章之URL
    def crawl_ptt_pages(self, board, pages=5):
        
        # 定義文章連結之陣列
        article_href = []

        # 組合批踢踢看板之URL
        url = '{}/bbs/{}/index.html'.format(PTTURL_PREFIX, board)

        # 迭代爬取頁面深度
        for _ in range(pages):

            # 發起GET requests
            r = requests.get(url, headers=headers, cookies=cookies)
            
            if r.status_code != 200:
                print('crawler.crawl_ptt_pages: 爬取{}時遇到回應錯誤，錯誤碼:{}'.format(url, r.status_code))
                print('直接回傳現有結果...')
                return article_href
            
            # 用美湯找出上一頁的連結
            soup = BeautifulSoup(r.text, 'lxml')
            btn = soup.select('div.btn-group.btn-group-paging > a')

            if btn == None or len(btn) < 2:
                return article_href
            
            # 嘗試擷取上一頁之連結，若失敗，則直接回傳現有結果
            try:
                up_page_href = btn[1]['href']
                next_page_href = PTTURL_PREFIX + up_page_href
                url = next_page_href
                links = self.crawl_page(url=url)
                article_href = [*article_href, *links]
            except:
                print('擷取上一頁連結失敗，直接回傳現有結果...')
                return article_href

        return article_href

    # 給定批踢踢版面URL，爬取版上單一頁面中所有的文章連結，回傳一陣列包含該頁面所有文章URL
    def crawl_page(self, url):

        # 建立一文章連結陣列，用於儲存文章URL
        article_href = []

        # 發起GET Requests來獲得頁面內容
        r = requests.get(url, headers=headers, cookies=cookies)

        if r.status_code != 200:
            print('crawler.crawl_page: 爬取{}時遇到回應錯誤，錯誤碼:{}'.format(url, r.status_code))
            print('直接忽略爬取該頁面之所有連結...')
        
        # 用美湯擷取頁面中所有文章連結
        soup = BeautifulSoup(r.text, 'lxml')

        # 擷取文章連結
        rows = soup.select('div.title')

        if rows == None:
            return []

        for row in rows:
            a = row.select('a')
            if len(a) > 0:
                href = a[0].get('href')
                article_href.append(PTTURL_PREFIX + href)
        
        return article_href

    # 給定文章URL, 爬取文章內容並存成對應資料結構
    def crawl_article(self, url):

        # 對文章發出GET Requests
        r = requests.get(url, headers=headers, cookies=cookies)
        
        if r.status_code != 200:
            print('crawler.crawl_article: 爬取{}時遇到回應錯誤，錯誤碼:{}'.format(url, r.status_code))
            print('直接忽略爬取該文章...')
            return None, None

        # 用美湯萃取推文及文章METADATA
        soup = BeautifulSoup(r.text, 'lxml')
        
        # 用lxml的XPATH來擷取文章內容
        selector = etree.HTML(r.text)

        # 過濾文章內容
        content = selector.xpath('/html/body/div[3]/div[1]/text()')
        if content != None:
            content = content[0].strip()
        
        # 擷取Metadata
        metas = soup.select('span.article-meta-value')

        # 檢查獲取正確性，若是獲取錯誤，則直接回傳空值
        if metas == None or len(metas) < 4:
            return None, None
        
        author, board, title, date = metas[0].text, metas[1].text, metas[2].text, metas[3].text
        author = extract_author(author)

        # 建構Article實例
        article = Article(author, board, title, date, content)

        # 擷取推文
        push_records = []
        pushes = soup.select('div.push')

        if pushes == None:
            return article, []

        # 擷取所有推文，若遇到擷取錯誤，則直接嘗試擷取下則推文
        for push in pushes:
            try:
                p_status = push.select_one('span.hl.push-tag').text
                p_author = push.select_one('span.f3.hl.push-userid').text
                p_content = push.select_one('span.f3.push-content').text
                p_date = push.select_one('span.push-ipdatetime').text
                push_records.append(Push(p_status, p_author, p_content, p_date))
            except:
                continue
        
        return article, push_records