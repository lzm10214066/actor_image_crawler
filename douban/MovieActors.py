#!/usr/bin/python
# encoding: utf-8
import requests
from lxml import etree
from functools import reduce
import time
import random
import sys
from imp import reload

reload(sys)
sys.setdefaultencoding("utf-8")


# url = open("urls", 'r')
def op(s):
    a = s.strip('/').split('/')
    if (len(a) == 2):
        return a[1]
    return '*'


def getMovieInfo(url):
    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
               "Accept-Encoding": "gzip, deflate, sdch, br",
               "Accept-Language": "zh-CN,zh;q=0.8",
               "Connection": "keep-alive",
               "Cookie": """bid=kpxCiW7R8hs; gr_user_id=8f0e789b-73f6-4cb1-9a24-5b869a75a210; _vis_opt_s=1%7C; _vwo_uuid=2AFCCB8D3179301BA1F82CBA5E5C3019; _vis_opt_exp_32_combi=1; _vis_opt_exp_31_combi=1; _vis_opt_exp_31_goal_1=1; nlsrid228272=2; enable_push_desktop_noty=1; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1483159666%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; ll="108296"; ps=y; ue="betasdeng1992@sina.cn"; dbcl2="61295987:Gj+YkB6qPjU"; ck=rOkM; _vwo_uuid_v2=C950AFE94CFE50C746119810AF4030E2|c2a5cd204eef39355588d689285bfb0d; ap=1; __utmt=1; push_noty_num=0; push_doumail_num=0; __utmt_douban=1; __utma=30149280.160500193.1479529210.1483030234.1483159666.19; __utmb=30149280.17.10.1483159666; __utmc=30149280; __utmz=30149280.1482247417.13.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=30149280.6129; __utma=223695111.1509095869.1479529229.1483030234.1483159666.17; __utmb=223695111.0.10.1483159666; __utmc=223695111; __utmz=223695111.1482236291.9.9.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_id.100001.4cf6=ce737c7a0a3f1960.1479529230.17.1483162912.1483032917.; _pk_ses.100001.4cf6=*""",
               "DNT": "1",
               "Host": "movie.douban.com",
               "Upgrade-Insecure-Requests": "1",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
               }
    html = requests.get(url, headers=headers).content.decode("utf-8")
    selector = etree.HTML(html)
    strCat = lambda x, y: x + "/" + y

    # movie actor(s)
    tmp = selector.xpath("//a[@rel='v:starring']/text()")
    actors = len(tmp) == 0 and "NotDefined" or reduce(strCat, tmp)

    # actor urls
    tmp = selector.xpath("//a[@rel= 'v:starring']/@href")
    if (len(tmp) == 0):
        actors_urls = "NotDefined"
    else:
        tmp = map(op, tmp)
        actors_urls = len(tmp) == 0 and "NotDefined" or reduce(strCat, tmp)

    movie_info = {
        "actors": actors,
        "actors_urls": actors_urls
    }
    return movie_info


if __name__ == '__main__':
    strCat = lambda x, y: x + "," + y
    output = open("douban_actors_urls.txt", "a")
    with open(sys.argv[1], "r") as f:
        count = 0
        while True:
            count = count + 1
            # if(count3):
            # break
            if count % 10 == 0:
                print(count)
            url = f.readline().strip('\n')
            if (count < 4120):
                continue
            dm = getMovieInfo(url)

            infos = [
                dm["actors"],
                dm["actors_urls"]
            ]
            print(infos)
            output.write(reduce(strCat, infos))
            output.write("\n")
            delay = random.random() * 2 + 1
            print(delay, 's')
            time.sleep(delay)

    output.close()
