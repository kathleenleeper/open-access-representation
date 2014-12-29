import codecs
import csv

f = codecs.open("oai-pmh-articles.xml").readlines() # file must be in local directory for this to run properly

metadata = [] 
authors = []
Article = {}

for i in range(0,len(f)):
    line = f[i]
    splitLine = str(line).split('>')
    # start pulling data and assigning to variables
    if "title" in splitLine[0]:
        title = splitLine[1].split('<')[0] 
    if "date" in splitLine[0]: 
        date = splitLine[1].split('T')[0] 
    if "description" in splitLine[0]:  
        description = splitLine[0].split('<')[0] 
    if "creator" in splitLine[0]: 
        authors.append(splitLine[1].split('<')[0]) 
    if "language" in splitLine[0]:
        language = splitLine[1].split('<')[0] 
        if language == "EN": # convert "EN" to English
            language = "English"
    if "/record" in splitLine[0]: #stop pulling, start writing
    
        #pull -first- names from description
        for j in range(0,len(authors)):
            author = authors[j].split(" ")
            for l in description.split(","):
                    if author[0] in l:
                        if len(l.split(" ")) < 7:
                            authors[j] = l.split(" ",1)[1]
        Article = {"Title": title, "Date": date,"Language": language, "Author": authors} # define article dictionary
        metadata.append(Article) # push line to metadata
        authors=[] # reset Author array


