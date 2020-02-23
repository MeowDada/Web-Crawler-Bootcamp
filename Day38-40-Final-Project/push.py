#coding: utf-8
from enum import Enum

# 定義推文狀態
class PushStatus(Enum):
    REPLY = 'Reply'
    UPVOTE = 'Upvote'
    DOWNVOTE = 'Downvote'
    UNKNOWN = 'Unknown'

# 輸入字串並判定為何種推文狀態
def determine_push_status(status):
    if status == '→ ':
        return PushStatus.REPLY
    elif status == '推 ':
        return PushStatus.UPVOTE
    elif status == '噓 ':
        return PushStatus.DOWNVOTE
    return PushStatus.UNKNOWN

# 推文資料結構
class Push:
    def __init__(self, status, author, content, date):
        self.author = author
        self.date = date
        self.content = content
        self.push = determine_push_status(status).name
    