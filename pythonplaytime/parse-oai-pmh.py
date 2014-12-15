import codecs
f = codecs.open("oai-pmh-articles.xml").readlines() # file must be in local directory for this to run properly

metadata = [] 
author = []
Article = {}

for i in range(0,len(f)):
    line = f[i]
    splitLine = str(line).split('>')
    if "title" in splitLine[0]:# if it's a title line
        title = splitLine[1].split('<')[0] #print the dumb titl      
    if "date" in splitLine[0]:
        date = splitLine[1].split('T')[0] #print the dumb titl      
    if "creator" in splitLine[0]:
        author.append(splitLine[1].split('<')[0]) #print the dumb titl
    if "language" in splitLine[0]:
        language = splitLine[1].split('<')[0] #print the dumb title
        print language
    if "/record" in splitLine[0]:
        Article = {"Title": title, "Date": date,"Language": language, "Author": author}
        author=[]
        metadata.append(Article)

print len(metadata)
print metadata[1]



# CSV header format Title,Title Alternative,Identifier,Publisher,Language,ISSN,EISSN,Keyword,Start Year,End Year,Added on date,Subjects,Country,Publication fee,Further Information,CC License,Content in DOAJ
