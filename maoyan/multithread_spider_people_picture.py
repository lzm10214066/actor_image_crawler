# -*- coding: utf-8 -*-
import threading
import time
import requests
import json
import random
import os
import sys
from imp import reload

reload(sys)
sys.setdefaultencoding('utf-8')

all_people = []
f = open('all_people-part2')
line = f.readline()
while line:
    # print line
    sp = line.strip().split("\t")
    name = sp[1]
    id = sp[0]
    # print name
    all_people.append(line.strip())
    line = f.readline()
f.close()

save_root = "maoyan"

user_agent_raw = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/"
cookie_raw = "1A6E888B4A4B29B16FBA1299108DBE9C8D5D76EF96601D4AE70AAE0E310AD1A2; _lx_utm=; __mta=255646263.1500865298924.1500865926476.1500867182165.36; _lxsdk_s=dfbfa40b9016004dffd2be1a4ba5%7C%7C87"

url = "http://maoyan.com/films/celebrity/ajax/photos/"  # 1/celebrities.json"

headers = {
    "Content-Type": "application/json; charset=utf-8",
    "Accept-Encoding": "gzip, deflate",
    # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    # "Host": "frodo.douban.com",
    # "Connection": "Keep-Alive",
    # "Content-Encoding": "gzip",
    "User-Agent": "",
    "Cookie": "uuid=1A6E888B4A4B29B16FBA1299108DBE9C8D5D76EF96601D4AE70AAE0E310AD1A2; _lx_utm=; __mta=255646263.1500865298924.1500865926476.1500867182165.36; _lxsdk_s=dfbfa40b9016004dffd2be1a4ba5%7C%7C87"
}


def download_one_img(img_url, save_path, count):
    try:
        pic = requests.get(img_url, timeout=10)
    except Exception as e:
        print
        '[Download Error]', img_url, e
    index = str(img_url).rfind(".")
    img_path = os.path.join(save_path, str(count) + str(img_url)[index:].split("@")[0])
    try:
        fp = open(img_path, 'utf-8', 'wb')
        fp.write(pic.content)
        fp.close()
    except Exception as e:
        print("[Save exception]", img_path, e)


def download_pictures(id, name):
    headers["User-Agent"] = user_agent_raw + str(random.random() * 1000)
    headers["Cookie"] = "uuid=" + str(int(random.random() * 1000)) + cookie_raw
    try:
        print(url + str(id))
        ret = requests.get(url + str(id), headers=headers)
        ret = json.loads(ret.text)
        print(ret['photos'])

        if len(ret['photos']) == 0:
            return

        save_path = os.path.join(save_root, "images", id + "_" + name + "_" + str(len(ret['photos'])))
        try:
            os.makedirs(save_path, 'utf-8')
        except:
            pass

        count = 0

        photos_100 = ret['photos'][0:100]
        for i in range(len(photos_100)):
            img_url = photos_100[i]['olink'].replace("/w.h", "")
            t = threading.Thread(target=download_one_img, args=(img_url, save_path, i))
            t.setDaemon(True)  # 把子进程设置为守护线程，必须在start()之前设置
            t.start()
        t.join()

        # for one in ret['photos']:
        #
        #     print img_url
        #
        #
        #     count += 1
        #     if count > 100:
        #         break
        # print "save ", img_path, "done"
    except Exception as e:
        print("[Outer exception]", id, e, ret.text)


# ret = download_pictures("28587", "杨颖")
# print ret
#
# img_url = 'http://p0.meituan.net/movie/07045f14d1270c73963d98b687dafe716272467.gif'


def run(n, N):
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Host": "frodo.douban.com",
        "Connection": "Keep-Alive",
        "Content-Encoding": "gzip",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/",
        "Cookie": "uuid=1A6E888B4A4B29B16FBA1299108DBE9C8D5D76EF96601D4AE70AAE0E310AD1A2; _lx_utm=; __mta=255646263.1500865298924.1500865926476.1500867182165.36; _lxsdk_s=dfbfa40b9016004dffd2be1a4ba5%7C%7C87"
    }
    # time.sleep(0.1 * i)
    # print("task", n)
    start = len(all_people) / N * n
    to = (len(all_people) / N * (n + 1))
    if n == N - 1:
        to = len(all_people)
    print(n, start, to, len(all_people))

    for index in range(start, to):
        try:
            sp = all_people[index].strip().split("\t")
            id = sp[0]
            name = sp[1]
            print("will download ", name)
            download_pictures(id, name)
            time.sleep(2)
        except:
            pass


for i in range(1):
    t = threading.Thread(target=run, args=(i, 1))
    t.setDaemon(True)  # 把子进程设置为守护线程，必须在start()之前设置
    t.start()

t.join()

# os.makedirs(unicode("哈哈哈",'utf-8'))
