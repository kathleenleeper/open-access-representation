import codecs
f = codecs.open("oai-pmh-articles.xml").readlines() # file must be in local directory for this to run properly

metadata = [] 
author = []
Article = {}

for i in range(0,len(f)):
    line = f[i]
    splitLine = str(line).split('>')
    if "title" in splitLine[0]:# if it's a title line
        title = splitLine[1].split('<')[0] # set title variable
    if "date" in splitLine[0]: # if its the date
        date = splitLine[1].split('T')[0] # set date variable      
    if "creator" in splitLine[0]: 
        author.append(splitLine[1].split('<')[0]) 
    if "language" in splitLine[0]:
        language = splitLine[1].split('<')[0] 
        if language == "EN": # convert "EN" to English
            language = "English"
    if "/record" in splitLine[0]: # if end of record
        Article = {"Title": title, "Date": date,"Language": language, "Author": author} # define article dictionary
        metadata.append(Article) # push artical dictionary to metadata array
        author=[] # reset Author array

print len(metadata)
print metadata[1]



# CSV header format Title,Title Alternative,Identifier,Publisher,Language,ISSN,EISSN,Keyword,Start Year,End Year,Added on date,Subjects,Country,Publication fee,Further Information,CC License,Content in DOAJ
