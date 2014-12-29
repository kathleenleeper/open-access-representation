import csv

#write article to CSV file
#script in own file because modularity!
#definitely needs some abstraction ouch
with open('parsed_oai.csv', 'w') as csvfile:
    fieldnames = ["Title","Date","Language","Author"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in metadata: # cycles through each article in array
        authors = i["Author"]
        for j in authors: # cycle through each to make expand csv a la Alex's output_demo.2
            writer.writerow({"Title": i["Title"], "Date": i["Date"],"Language": i["Language"], "Author": j})

