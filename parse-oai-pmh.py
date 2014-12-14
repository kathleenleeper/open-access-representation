import codecs
f = codecs.open("oai-pmh-articles.xml").readlines() # file must be in local directory


for i in range(0,len(f)):
    line = f[i]
    splitLine = str(line).split('>')
    if "<dc:title" in splitLine[0]:
        print splitLine[1].split('<')[0]
