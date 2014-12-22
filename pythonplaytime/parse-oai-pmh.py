import codecs
import csv

f = codecs.open("oai-pmh-articles.xml").readlines() # file must be in local directory for this to run properly

metadata = [] 
authors = []
Article = {}

for i in range(0,len(f)):
    line = f[i]
    splitLine = str(line).split('>')
    if "title" in splitLine[0]:# if it's a title line
        title = splitLine[1].split('<')[0] # set title variable
    if "date" in splitLine[0]: # if its the date
        date = splitLine[1].split('T')[0] # set date variable
    if "description" in splitLine[0]: #  
        description = splitLine[0].split('<')[0] # set date variable
    if "creator" in splitLine[0]: 
        authors.append(splitLine[1].split('<')[0]) 
    if "language" in splitLine[0]:
        language = splitLine[1].split('<')[0] 
        if language == "EN": # convert "EN" to English
            language = "English"
    if "/record" in splitLine[0]: # if end of record
        for j in range(0,len(authors)):
            author = authors[j].split(" ")
            for l in description.split(","):
                    if author[0] in l:
                        if len(l.split(" ")) < 7:
                            authors[j] = l.split(" ",1)[1]
        Article = {"Title": title, "Date": date,"Language": language, "Author": authors} # define article dictionary
        metadata.append(Article) # push artical dictionary to metadata array
        authors=[] # reset Author array

with open('parsed_oai.csv', 'w') as csvfile: # this could all be embedded into the loop above for efficiency, but was easiest to draft as a second loop.
    fieldnames = ["Title","Date","Language","Author"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in metadata: # cycles through each artical in metadata array
        authors = i["Author"] # handle multiple authors per artical
        for j in authors: # cycle through each to make expand csv a la Alex's output_demo.2
            writer.writerow({"Title": i["Title"], "Date": i["Date"],"Language": i["Language"], "Author": j})

# CSV header format Title,Title Alternative,Identifier,Publisher,Language,ISSN,EISSN,Keyword,Start Year,End Year,Added on date,Subjects,Country,Publication fee,Further Information,CC License,Content in DOAJ
