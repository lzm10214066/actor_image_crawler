import codecs


def readMovieUrl(fileObject):
    try:
        line = fileObject.readline().rstrip("\n").rstrip(",").split(",")
        n = len(line)
        name = ','.join(line[0:n - 1])
        url = line[-1]
        # print("%s,%s"%(name, url))
        return name, url
    except StopIteration:
        print("StopIteration:You have read the end of the file.")
        return False


output = open("test.csv", "w")
output.write(codecs.BOM_UTF8)

with open("douban_movie_by_year.csv", "r") as f:
    count = 0
    while True:
        count = count + 1
        if count % 100 == 0:
            print(count)
        name, url = readMovieUrl(f)
        name = str(name).replace(',', '-')
        if name == '':
            break
        output.write(name + ',' + url + '\n')
