import codecs
from gender_detector import GenderDetector #import genderMalev mdule
import csv
import re # regular expression searching
from ast import literal_eval
from urllib2 import urlopen

from genderComputer import GenderComputer #import gendercomputer - more fully featured
import os

f = codecs.open("oai-pmh-articles.xml").readlines() # open xml file; make sure file is local

d = GenderDetector('us') #using US for simplicity; modularizing comes later
gc = GenderComputer(os.path.abspath('./nameLists')) #make gendercomputer

def writeData(metadata): 
    with open('parsed_oai.csv', 'w') as csvfile: # this could all be embedded into the loop above for efficiency, but was easiest to draft as a second loop.
        fieldnames = ["Title","Date","Language","Author","MGender","CGender","NGender","journal","publisher","topics"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in metadata: # cycles through each artical in metadata array
            authors = i["Authors"] # handle multiple authors per artical
            Mgenders = i["Mgenders"]
            Cgenders = i["Cgenders"]
            Ngenders = i["Ngenders"]
            
            for j in range(0,len(authors)): # cycle through each to make expand csv a la Alex's output_demo.2
                author = authors[j]
                Mgender = Mgenders[j]
                Cgender = Cgenders[j]
                Ngender = Ngenders[j]
                writer.writerow({"Title": i["Title"], "Date": i["Date"],"Language": i["Language"], "Author": author, "publisher":i["publisher"], "journal":i["source"], "topics":i["subjects"], "MGender": Mgender, "CGender": Cgender, "NGender": Ngender})

metadata = [] 
                
def parseData(f):
    authors = []
    subjects = []
    lastName = []
    firstName = []
    Article = {}
    Mgenders = []
    Cgenders = []
    Ngenders = []
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
        if "subject" in splitLine[0]:
            subject = splitLine[1].split('<')[0]
            if "LCC" in subject:
                subjects.append(subject.split(":")[1])
            else:
                subjects.append(subject)
        if "source" in splitLine[0]: 
            source = splitLine[1].split('<')[0].split(',')[0]
        if "publisher" in splitLine[0]: 
            publisher = splitLine[1].split('<')[0] 
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
                        nameArray = l.split(" ")
                        if digitCheck:
                            if len(nameArray) > 2:
                                authors[j] = nameArray[1] +" "+ nameArray[2] # first then last name                     
                            else:
                                authors[j] = nameArray[0] +" "+ nameArray[1] # first then last
                        elif asteriskCheck:
                            authors[j] = nameArray[1] +" "+ nameArray[2] # first then last
                        else:
                            stripNameArray = l.strip().split(" ")
                            authors[j] = stripNameArray[0] +" "+ stripNameArray[1]
            #hacky second-tier cleanup & assigning genders
            for k in range(0,len(authors)):
                print authors
                authorFirst = authors[k].split(" ")[0]
                if re.search("\d",authorFirst):
                    authorFirst = "misparsed"
                    authors[k] = "misparsed"
                if re.search("&amp",authorFirst):
                    authorFirst = "misparsed"
                    authors[k] = "misparsed"
                if "" == authorFirst:
                    authorFirst = "misparsed"
                    authors[k] = "misparsed"
                Mgender = d.guess(authorFirst) #guess with malev code
                Mgenders.append(Mgender)
                Cgender = gc.resolveGender(unicode(authorFirst,errors='ignore'), None) #guess with gender computer
                if Cgender == None:
                    Cgender = "unknown"
                Cgenders.append(Cgender)
                namsor = "http://api.namsor.com/onomastics/api/json/gendre"
                authorFirstLast = authors[k].split(" ")
                if 3 > len(authorFirstLast) > 1: # only works with first and last name
                    if authorFirstLast[0] != "" and authorFirstLast[1] != "": # filter out arrays from strings like "usa " 
                        for l in authorFirstLast:
                            namsor = namsor + "/" + l # construct url
                        namsorString = urlopen(namsor).read() # make GET request
                        namsorDict = literal_eval(namsorString) # convert to dict
                        Ngenders.append(namsorDict['gender']) # append gender result to Ngenders
                    else:
                        Ngenders.append("misparsed") # incase of "usa " strings
                else: 
                    Ngenders.append("misparsed") # incase of 3<x or x<1
            Article = {"Title": title, "Date": date,"Language": language, "Authors": authors, "subjects":subjects, "source": source, "publisher":publisher, "Mgenders": Mgenders, "Cgenders": Cgenders, "Ngenders": Ngenders} # define article dictionary
            metadata.append(Article) # push line to metadata
            authors = []
            Mgenders = []
            Cgenders = []
            Ngenders = []
            subjects = []
    writeData(metadata)

    # writing article to CSV file (temporary until we figure out how to put R inside python
    #import csvwriter # ugly hacky way to run the csv writing script. whatever. we'll be oka

parseData(f)
