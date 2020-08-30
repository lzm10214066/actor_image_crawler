#!/usr/bin/env python
# encoding: utf-8
import urllib2
import re
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def img_spider(name_file):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
    headers = {'User-Agent':user_agent}
    #读取名单txt，生成包括所有人的名单列表
    with open(name_file) as f:
        name_list = [name.rstrip().decode('utf-8') for name in f.readlines()]
        f.close()
    #遍历每一个人，爬取30张关于他的图，保存在以他名字命名的文件夹中
    for name in name_list:
        #生成文件夹（如果不存在的话）
        if not os.path.exists('E:/celebrity/img_data/' + name):
            os.makedirs('E:/celebrity/img_data/' + name)
            try:
                #有些外国人名字中间是空格，要把它替换成%20，不然访问页面会出错。
                url = "http://image.baidu.com/search/avatarjson?tn=resultjsonavatarnew&ie=utf-8&word=" + name.replace(' ','%20') + "&cg=girl&rn=60&pn=60"
                req = urllib2.Request(url, headers=headers)
                res = urllib2.urlopen(req)
                page = res.read()
                #print page
                #因为JSON的原因，在浏览器页面按F12看到的，和你打印出来的页面内容是不一样的，所以匹配的是objURL这个东西，对比一下页面里别的某某URL，那个能访问就用那个
                img_srcs = re.findall('"objURL":"(.*?)"', page, re.S)
                print name,len(img_srcs)
            except:
                #如果访问失败，就跳到下一个继续执行代码，而不终止程序
                print name," error:"
                continue
            j = 1
            src_txt = ''

            #访问上述得到的图片路径，保存到本地
            for src in img_srcs:
                with open('E:/celebrity/img_data/' + name + '/' + str(j)+'.jpg','wb') as p:
                    try:
                        print "downloading No.%d"%j
                        req = urllib2.Request(src, headers=headers)
                        #设置一个urlopen的超时，如果3秒访问不到，就跳到下一个地址，防止程序卡在一个地方。
                        img = urllib2.urlopen(src,timeout=3)
                        p.write(img.read())
                    except:
                        print "No.%d error:"%j
                        p.close()
                        continue
                    p.close()
                src_txt = src_txt + src + '\n'
                if j==300:
                    break
                j = j+1
            #保存30个图片的src路径为txt，我要一行一个，所以加换行符
           # with open('E:/celebrity/img_data/' + name + '/' + name +'.txt','wb') as p2:
            #    p2.write(src_txt)
            #    p2.close()
           #     print "save %s txt done"%name

#主程序，读txt文件开始爬
if __name__ == '__main__':
    name_file = "celeb.txt"
    img_spider(name_file)