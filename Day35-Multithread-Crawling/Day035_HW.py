import _thread
import time
import requests
from bs4 import BeautifulSoup

def crawl_ptt(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html5lib')

    articles = soup.find_all(class_='r-ent')
    for article in articles:
        try:
            title = article.find(class_='title').a.text
            author = article.find(class_='meta').find(class_='author').text
            date = article.find(class_='meta').find(class_='date').text
            print('{}.{}.{}'.format(author, title, date))
        except:
            pass

def crawl_ptt_nba():
    url = 'https://www.ptt.cc/bbs/NBA/index.html'

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html5lib')

    articles = soup.find_all(class_='r-ent')
    for article in articles:
        try:
            title = article.find(class_='title').a.text
            author = article.find(class_='meta').find(class_='author').text
            date = article.find(class_='meta').find(class_='date').text
            print('{}.{}.{}'.format(author, title, date))
        except:
            pass

def crawl_ptt_savemoney():
    url = 'https://www.ptt.cc/bbs/Lifeismoney/index.html'

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html5lib')

    articles = soup.find_all(class_='r-ent')
    for article in articles:
        try:
            title = article.find(class_='title').a.text
            author = article.find(class_='meta').find(class_='author').text
            date = article.find(class_='meta').find(class_='date').text
            print('{}.{}.{}'.format(author, title, date))
        except:
            pass

def main():
    
    urls = [
        'https://www.ptt.cc/bbs/NBA/index.html',
        'https://www.ptt.cc/bbs/Lifeismoney/index.html',
    ]

    # Single thread crawling
    startTime = time.time()
    for url in urls:
        crawl_ptt(url)
    finishTime = time.time()
    print(finishTime-startTime)

    # Multithread crawling
    startTime = time.time()
    for url in urls:
        _thread.start_new_thread( crawl_ptt, (url, ) )
    finishTime = time.time()
    print(finishTime-startTime)

if __name__ == "__main__":
    main()    
    
