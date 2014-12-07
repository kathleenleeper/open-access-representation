# Just some preliminary messing around with data
# downloaded from - http://doaj.org/faq#metadata

data <- read.csv('~/Desktop/meta.csv')
# loading csv file

head(data)
# checking to see how it looks
View(data)
# opens up a pop-up window...
# looks in-depth but not very broad. no info on gender.

# might be interesting to start by looking at country...
# R doesn't love categorical data so we can either make a single large frequency table or just use the table() command where necessary.


barplot(height = table(data$Language))
# first problems become apparent here...
View(table(data$Language))
# we can scroll down and see that our Language categories are a mess. one of the highest frequencies belongs to a blank space, English is spelled about six different ways, countries are often abbreviated and lumped.

# can't really think of anything useful to do until we get our categories sorted... maybe something python can tackle?
