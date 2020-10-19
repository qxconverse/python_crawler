from bs4 import BeautifulSoup
import requests
import json

from tkinter import *

song_url = 'http://music.163.com/song?id='
comment_url = 'https://music.163.com/weapi/comment/resource/comments/get?csrf_token='

headers = {
    "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
}


def deleteUnicodeError(s):
    astral = re.compile(r'([^\u0000-\uffff])')
    newc = ''
    for i, ss in enumerate(re.split(astral, s)):
        if not i % 2:
            newc += ss
    return newc


def get_hot_comments(song_id):
    param = {
        'params': 'S/V0WRmwivlAQqAw2N3qIZMz/lsilqmQ3v7aTQLwdO35QqL2bGwtlksZ3s61J9ULl9BUydsh1uGP+hPlTpsfP0/yuvZ2zGnO0D8m8era3Vmw49dsLdRuzbCWECBWlDcHFrPIKT7yezpxbqMsEvpbocccqXAogOmbVuZ8uEtzUHExITmPcHQHitvgO20DFR7IlVtox8cEHhsZibXszVYNJcbjSVXkgYn30j7SKFQzCSVn03NZBxYUhoPqRcUIIo2mbPC5VbyYrZ0H1XT1XTunif/yWtwbY34q1HJoplIZFxk=',
        'encSecKey': '086d937530dced660da4d8b8ca9d944a602708a1809f72b503f095efa4d937ecef707c8afae6ace1f79dc3a1414316b33701be0c878a50f927fe8d9d2aa23366e98313aea9e930eda07f833404ddf45873d62a3f3be353cbe4d2534808de36d127d02874a02045f84747451a29bf850b7efa40a6b0292a14c10fdd71af0365d1'}
    url = comment_url + song_id
    web_data = requests.post(url, param)
    data = json.loads(web_data.text)
    print(data)
    hot_comments = data['data']['hotComments']
    return hot_comments


def get_song_name(song_id):
    url = song_url + song_id
    web_data = requests.get(url, headers=headers)
    data = BeautifulSoup(web_data.text, "lxml")
    title = data.find_all("em", class_="f-ff2")
    if len(title) == 0:
        return "None"
    else:
        return title[0].string


class WidgetsDemo:
    def __init__(self):
        window = Tk()
        window.title("获取网易云音乐Top15热评")
        frame2 = Frame(window)
        frame2.pack()
        label = Label(frame2, text="请输入歌曲ID")
        self.song_id = StringVar()
        entryName = Entry(frame2, textvariable=self.song_id)
        btGetName = Button(frame2, text="获取热评", command=self.getHotComments)
        label.grid(row=1, column=1)
        entryName.grid(row=1, column=2)
        btGetName.grid(row=1, column=3)
        self.text = Text(window)
        # self.text.configure(state="disabled")
        self.text.pack()
        window.mainloop()

    def getHotComments(self):
        self.text.delete(0.0, END)
        title = get_song_name(self.song_id.get())
        if title != "None":
            self.text.insert(INSERT, "歌曲名为：" + title + "\n")
            hot_comments = get_hot_comments(self.song_id.get())
            if len(hot_comments) != 0:
                self.text.insert(INSERT, "共有" + str(len(hot_comments)) + "条热评\n")
                for i in range(len(hot_comments)):
                    user_name = hot_comments[i]['user']['nickname']
                    likes = hot_comments[i]['likedCount']
                    comment = hot_comments[i]['content']
                    # print(comment)
                    # print(deleteUnicodeError(comment))
                    self.text.insert(INSERT,
                                     "--------------------------------------------------------------------------------\n")
                    self.text.insert(INSERT, "第" + str(i + 1) + "条\n")
                    self.text.insert(INSERT, "用户昵称：" + user_name + " 点赞数：" + str(likes) + "\n")
                    self.text.insert(INSERT, "评论内容：" + deleteUnicodeError(comment) + "\n\n")
            else:
                self.text.insert(INSERT, "对不起，该歌曲暂无热门评论。\n")
        else:
            self.text.insert(INSERT, "对不起，未找到相关歌曲。\n")


WidgetsDemo()
