# 定義文章之資料結構
class Article:
    def __init__(self, author, board, title, date, content):
        self.author = author
        self.board = board
        self.title = title
        self.date = date
        self.content = content