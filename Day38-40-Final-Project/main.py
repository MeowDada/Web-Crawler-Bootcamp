from crawler import PTTCrawler
from util import dump_to_json
from util import load_json
import os
import time
import random

# 定義最小爬取間隔 (sec)
MIN_CRAWL_INTERVAL = 1

# 定義最大爬取間隔 (sec)
MAX_CRAWL_INTERVAL = 3

# 定義爬取資料存放位置
DATADIR = 'data'

# 定義爬取資料存取名稱前綴
FILENAME_PREFIX = 'HatePolitics'

# 隨機等待，用於防止爬蟲程式送出請求太過頻繁而被BAN
def random_wait():
    time_to_wait = random.randint(MIN_CRAWL_INTERVAL, MAX_CRAWL_INTERVAL)
    time.sleep(time_to_wait)

# 給定rootpath與檔案index，回傳對應的完整檔案路徑
def get_crawl_filename(root, index):
    return os.path.join(root, DATADIR, '{}-{}.json'.format(FILENAME_PREFIX, index))

# 創立一個爬蟲者實例，爬取政黑板20頁的內容
worker = PTTCrawler() 
links = worker.crawl_ptt_pages(board='HatePolitics', pages=20)

# 初始化亂數種子
random.seed('pttcrawler')

# 定義爬取index
count = 0

# 建立爬取資料夾
if not os.path.exists(DATADIR):
    os.mkdir(DATADIR)

# 迭代針對每一個文章連結去爬取內容並存成合適資料結構
# 並將這些資料結構儲存成對應之Json檔案以利後續存取分析
for link in links:
    article, pushes = worker.crawl_article(url=link)
    filename = get_crawl_filename(os.getcwd(), count)
    dump_to_json(filename, article, pushes)
    count += 1
    random_wait()
    print('爬取第{}個結果... (URL = {})'.format(count, link))
