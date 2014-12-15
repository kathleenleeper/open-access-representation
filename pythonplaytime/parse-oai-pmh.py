import codecs
f = codecs.open("oai-pmh-articles.xml").readlines() # file must be in local directory



for i in range(0,len(f)):
    line = f[i]
    if "<dc:title" in splitLine[0]: #if it's a title line
    splitLine = str(line).split('>')
        print splitLine[1].split('<')[0] #print the dumb title




for i in range(0,len(f)):
    line = f[i]
    splitLine = str(line).split('>')
    if "<dc:date" in splitLine[0]:
        print splitLine[1].split('T')[0]


#Title,Title Alternative,Identifier,Publisher,Language,ISSN,EISSN,Keyword,Start Year,End Year,Added on date,Subjects,Country,Publication fee,Further Information,CC License,Content in DOAJ
