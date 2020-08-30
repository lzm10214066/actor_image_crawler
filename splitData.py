#!/usr/bin/python
# encoding: utf-8

n = 2
data = "douban/actors_ids.txt"
f = open(data, 'r')
all = f.readlines()
d = len(all) // n
for i in range(n):
    name = data.split('.')[0].split('/')[-1]
    out = open(name + str(i) + ".txt", 'w')
    s = i * d
    e = (i + 1) * d
    if (i == n - 1):
        e = len(all)
    for j in range(s, e):
        out.write(all[j])

    out.close()
