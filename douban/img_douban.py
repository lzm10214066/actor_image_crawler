# coding=utf-8

import urllib
import re
import os
import sys
import random
import time
from bs4 import BeautifulSoup
from imp import reload

reload(sys)
sys.setdefaultencoding("utf-8")

save_root = "data"
no_valid_ac = open("no_valid.txt", 'r')
no_need_ac = set(no_valid_ac.readlines())
no_valid_ac.close()

no_valid_ac = open("no_valid.txt", 'a')


def auto_down(url, filename):
    try:
        urllib.urlretrieve(url, filename)
    except urllib.ContentTooShortError:
        print('Network conditions is not good.Reloading.')
        auto_down(url, filename)


def downOnePerson(actor_id):
    if (actor_id in no_need_ac):
        print("not valid")
        return -1
    tmp = actor_id.strip('\n').split('\t')
    a = tmp[0]
    a = a.strip(' ').replace(' ', '_')
    id = tmp[1]

    save_path = save_root + "/" + a
    if (os.path.exists(save_path, 'utf-8')):
        return -2
    else:
        os.makedirs(save_path, 'utf-8')

    y = 1
    x = 0
    # 设置下载页数，进行循环，当前为3页
    for y in range(1, 16):
        page = (y - 1) * 40
        url = "http://movie.douban.com/celebrity/" + id + "/photos/?type=C&start=%s&sortby=vote&size=a&subtype=a" % page
        content = urllib.urlopen(url).read()
        # print content

        soup = BeautifulSoup(content, "lxml")
        img_all = soup.find_all("img", src=re.compile('.doubanio.com/view/photo'))
        if (y == 1 and len(img_all) < 20):
            print(len(img_all), " images")
            no_valid_ac.write(actor_id)
            no_valid_ac.flush()
            break
        elif (len(img_all) == 0):
            break
        # 下载链接头中有img3,img5，故正则时不写进去

        print("正下载第%s页" % y)
        for img in img_all:
            img_str = img["src"]
            img_b = img_str.replace("thumb", "photo")
            img_name = "%s-%s.jpg" % (y, x)
            path = save_path + "/" + img_name  # 保存图片路径
            # urllib.urlretrieve(img_b, unicode(path,'utf-8'))
            try:
                auto_down(img_b, path)
            except:
                print("the image fails")
            delay = random.random() * 0.01
            time.sleep(delay)
            x += 1
        y += 1
        delay = random.random() * 1 + 1
        print(delay, 's')
        time.sleep(delay)
    return 1


if __name__ == '__main__':
    f = open(sys.argv[1], 'r')
    i = 0
    while True:
        if ((i + 1) % 10 == 0):
            print(i)
            # break
        ac_id = f.readline()
        i += 1
        print("download ", ac_id)
        res = downOnePerson(ac_id)
        if (res == 1):
            delay = random.random() * 2 + 2
            print(delay, 's')
            time.sleep(delay)
    f.close()
    no_valid_ac.close()
