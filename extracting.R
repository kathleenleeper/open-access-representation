### EXTRACTING SUBJECT DATA ###
# getting used to playing with the CSV file we'll be using.
# Main problem: How do we extract 'subject' from a cell with multiple subjects?

# reading csv
# data <- read.csv('~/Documents/Academics/Projects/open-access-representation/pythonplaytime/output-demo.csv')

View(data)
# data looks good

# an example of how we might approach this: what is the ratio of male:female authors under the subject of 'orgo'?
# the problem is that we have to extract "orgo" from the string of characters "neuro, chem, orgo"

# cool. so this takes the dataframe "data" and greps for "orgo" within the 'data$subject' column. the output should be any row that contains the subject 'orgo'.
# if we have to we can probably do the same for 'author'
orgo <- data[grep("orgo", data$subject), ]
View(orgo)

# again, ratio of m:f in orgo?
# building bb data.frame
gender <- data.frame(table(orgo$gender))
gender$Perc <- gender$Freq/sum(gender$Freq)
gender$Labels <- paste(gender$Var1, '\n', gender$Perc, '%')
gender

pie(gender$Freq, labels = gender$Labels, main = 'Gender Breakdown in Orgo') 
# YAY
# women are over-represented. typical.

