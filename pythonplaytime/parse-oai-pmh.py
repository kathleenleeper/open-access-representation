import codecs
from gender_detector import GenderDetector #import gender module

f = codecs.open("oai-pmh-articles.xml").readlines() # open xml file; make sure file is local

metadata = [] 
authors = []
lastName = []
firstName = []
Article = {}

d = GenderDetector('us') #using US for simplicity; modularizing comes later

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
    
        #pull -first- names from description
        for j in range(0,len(authors)):
            author = authors[j].split(" ")
            for l in description.split(","):
                if author[0] in l:
                    print l.split()[0] 
                    if len(l.split()) < 7:
                        authors[j] = l.split(" ",1)[1]
            
            #gender = d.guess(k)
            #print gender
        Article = {"Title": title, "Date": date,"Language": language, "LastName": lastName, "FirstName": firstName} # define article dictionary
        metadata.append(Article) # push line to metadata
        authors=[] # reset Author array
        firstName=[]


# writing article to CSV file (temporary until we figure out how to put R inside python
#import csvwriter # ugly hacky way to run the csv writing script. whatever. we'll be okay
