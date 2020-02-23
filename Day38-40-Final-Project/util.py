import re
import json
from article import Article
from push import Push

# 給定存檔名稱、與文章及推文資料結構，即可創建一個'存檔名稱'的json檔案
def dump_to_json(filename, article, pushes):
    if article == None or pushes == None:
        return
    
    with open(filename, 'w', encoding='utf-8') as f:
        data = json.dumps(article.__dict__)
        f.write(data + '\n')
        f.write(str(len(pushes)) + '\n')
        for push in pushes:
            data = json.dumps(push.__dict__)
            f.write(data + '\n')

# 給定讀取之json檔名，回傳Unmarshal過後的文章與推文資料結構
def load_json(filename):
    pushes = []
    article = None
    with open(filename, 'r', encoding='utf-8') as f:
        data = f.readline()
        ret = json.loads(data)
        article = Article(ret['author'], ret['board'], ret['title'], ret['date'], ret['content'])
        n = f.readline()
        for _ in range(int(n)):
            data = f.readline()
            ret = json.loads(data)
            push = Push(ret['author'], ret['date'], ret['content'], ret['push'])
            pushes.append(push)
    return article, pushes