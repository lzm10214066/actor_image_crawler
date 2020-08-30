#!/usr/bin/python
# encoding: utf-8

import os
import stat
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

root="data"
subfolers=os.listdir(unicode(root,'utf-8'))
for f in subfolers:
    imgs=os.listdir(root+'/'+f)
    if(len(imgs)==0):
        print f
        f1=root+"/"+f
       # n=root+"/"+f.strip(' ').replace(' ','_')
       # os.rename(f1,n)
        os.rmdir(f1)