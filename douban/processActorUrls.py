#!/usr/bin/python
# encoding: utf-8

import sys
from imp import reload

reload(sys)
sys.setdefaultencoding("utf-8")


def getActorIDs(line):
    info = []
    t = line.strip('\n').split(',')
    if (len(t) != 2):
        print
        line
        print
        'wrong!'
        return info
    actors = t[0].split('/')
    ids = t[1].split('/')
    if (len(actors) != len(ids)):
        print
        line
        print
        'wrong'
        return info
    for i in range(len(actors)):
        if (actors[i] == "NotDefined" or ids[i] == '*'):
            continue
        a_i = actors[i] + '\t' + ids[i]
        info.append(a_i)

    return info


def processDuplicatedName(actors_ids):
    a_i_copy = list(actors_ids)
    c = 0
    for i in range(1, len(actors_ids)):
        tmp = actors_ids[i].strip('\n').split('\t')
        a_i = tmp[0]
        id = tmp[1]
        a_p = actors_ids[i - 1].strip('\n').split('\t')[0]
        if (a_p == a_i):
            c += 1
            a_i = a_i + "_" + str(c)
            a_i_copy[i] = a_i + '\t' + id
        else:
            c = 0

    return a_i_copy


if __name__ == '__main__':
    actors_ids = []
    with open("douban_actors_urls.txt", "r") as f:
        count = 0
        while True:
            count = count + 1
            if count % 100 == 0:
                print(count)
            tmp = f.readline().strip('\n')
            # if (count < 39826):
            # continue
            if (tmp == ''):
                break
            dm = getActorIDs(tmp)
            if (len(dm) > 0):
                actors_ids.extend(dm)

    output = open("actors_ids.txt", "w")
    actors_ids_raw = list(set(actors_ids))
    actors_ids_raw.sort()
    actors_ids_raw = processDuplicatedName(actors_ids_raw)

    for i in actors_ids_raw:
        output.write(i + '\n')
    output.close()
