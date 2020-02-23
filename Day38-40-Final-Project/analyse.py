import jieba
import jieba.analyse
import numpy as np
import os
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator
from util import load_json

# 定義要讀取檔案之路徑前綴
DATADIR = 'data'

# 定義檔案前綴
FILENAME_PREFIX = 'HatePolitics'

# 定義至多要爬取多少檔案
FILENAME_INDEX_RANGE = 300

# 給定一字串與檔案名稱，將檔案內容讀取後接到該字串後面並回傳
def append_content(content, filename):

    # 嘗試讀取對應檔案，若錯誤，則直接回傳輸入之原始字串
    try:
        article, pushes = load_json(filename)
        content += '\n' + article.content
        for push in pushes:
            content += '\n' + push.content
    finally:
        return content
    
    return content

# 給定一文本內容，回傳由結巴做出之詞頻結果
def content_to_jieba(content, topK=20, allowPos=('n')):

    # 設定自訂義結巴辭典
    jieba.set_dictionary('dict.txt')

    # 設定自訂義結巴停止詞
    jieba.analyse.set_stop_words('stopwords.txt')

    # 輸入文本，計算詞頻
    tags = jieba.analyse.extract_tags(content, topK=topK, withWeight=True, allowPOS=allowPos)
    return tags

# 將結巴詞頻作為輸入，回傳一個文字雲物件
def jieba_to_wordcloud(tags):
    word_dict = {}
    for tag in tags:
        word_dict[tag[0]] = tag[1]

    font = r'msjh.ttc'
    mask = np.array(Image.open('bird.jpg'))
    wc = WordCloud(background_color="white",mask=mask,font_path=font,collocations=False, width=800, height=800, margin=2)  
    wc.generate_from_frequencies(frequencies=word_dict)
    return wc

# 給定rootpath與檔案index，回傳對應的完整檔案路徑
def get_crawl_filename(root, index):
    return os.path.join(root, DATADIR, '{}-{}.json'.format(FILENAME_PREFIX, index))

# 針對所有位於DATADIR底下之Json檔案進行讀取
# 並將文本內容整合成一個具大字串以供結巴分析
content = ''
for i in range(FILENAME_INDEX_RANGE):
    filename = get_crawl_filename(os.getcwd(), i)
    content = append_content(content, filename)

# 分析文本並產生詞頻
tags = content_to_jieba(content, topK=100)
wc = jieba_to_wordcloud(tags)

# 製作文字雲並秀出
plt.figure(figsize=(20,10), facecolor='k')
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.tight_layout(pad=0)
plt.show()