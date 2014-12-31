import codecs
from gender_detector import GenderDetector #import genderMalev mdule
import csv
import re # regular expression searching

from genderComputer import GenderComputer #import gendercomputer - more fully featured
import os

metadata = [] 
authors = []
lastName = []
firstName = []
Article = {}
Mgenders = []
Cgenders = []

f = codecs.open("oai-pmh-articles.xml").readlines() # open xml file; make sure file is local

d = GenderDetector('us') #using US for simplicity; modularizing comes later
gc = GenderComputer(os.path.abspath('./nameLists')) #make gendercomputer

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
    if "/record" in splitLine[0]: #stop pulling, start writing. kinda
    
        #pull first names from description
        for j in range(0,len(authors)):
            author = authors[j].split(" ")
            for l in description.split(","):
                if author[0] in l:
                    digitCheck = re.search("\d", l)  # check for digits
                    asteriskCheck = re.search("\*", l)  # check for asterisks
                    if digitCheck:
                        authors[j] = l.split(" ",)[1]
                    elif asteriskCheck:
                        authors[j] = l.split(" ")[1]
                    else:
                        authors[j] = l.strip().split(" ")[0]
        #hacky second-tier cleanup & assigning genders
        for k in range(0,len(authors)):
            author = authors[k]
            if re.search("\d",author):
               authors[k] = "misparsed"
            if "&amp" in author:
                authors[k] = "misparsed"
            if "" == author:
                authors[k] = "misparsed"
            author = authors[k]
            Mgender = d.guess(author) #guess with malev code
            Mgenders.append(Mgender)
            Cgender = gc.resolveGender(unicode(author,errors='ignore'), None) #guess with gender computer
            Cgenders.append(Cgender)
        Article = {"Title": title, "Date": date,"Language": language, "Authors": authors, "Mgenders": Mgenders, "Cgenders": Cgenders} # define article dictionary
        metadata.append(Article) # push line to metadata
        authors = []
        Mgenders = []
        Cgenders = []
# writing article to CSV file (temporary until we figure out how to put R inside python
#import csvwriter # ugly hacky way to run the csv writing script. whatever. we'll be oka

with open('parsed_oai.csv', 'w') as csvfile: # this could all be embedded into the loop above for efficiency, but was easiest to draft as a second loop.
    fieldnames = ["Title","Date","Language","Author","MGender","CGender"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in metadata: # cycles through each artical in metadata array
        authors = i["Authors"] # handle multiple authors per artical
        Mgenders = i["Mgenders"]
        Cgenders = i["Cgenders"]
        
        for j in range(0,len(authors)): # cycle through each to make expand csv a la Alex's output_demo.2
            author = authors[j]
            Mgender = Mgenders[j]
            Cgender = Cgenders[j]
            writer.writerow({"Title": i["Title"], "Date": i["Date"],"Language": i["Language"], "Author": author, "MGender": Mgender, "CGender": Cgender})
