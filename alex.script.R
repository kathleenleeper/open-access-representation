#################################
### Messing with Journal Data ###
#################################

# data from - http://doaj.org/faq#metadata

data <- read.csv('~/Documents/Academics/Projects/open-access-representation/journals.csv')
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
# we can scroll down and see that our Language categories are a mess. one of the highest frequencies belongs to a blank space, 'English' is spelled about six different ways, countries are often abbreviated and lumped.

# can't really think of anything useful to do until we get our categories sorted... maybe something python can tackle?



#########################################
### Turns out R can harvest OAI data! ###
#########################################

# using package 'OAIHarvester' and pretty much following vignette at:
# http://cran.r-project.org/web/packages/OAIHarvester/vignettes/oaih.pdf

# install.packages('OAIHarvester')
# installing package, commented out for now

library(OAIHarvester)
# turning on package

baseurl <- "http://doaj.org/oai"
# assigning our target url to an object

oaih_identify(baseurl)
# retrieves information about the data repository itself

oaih_list_metadata_formats(baseurl)
# lists, well, available metadata formats

sets <- oaih_list_sets(baseurl)
rbind(head(sets, 3L), tail(sets, 3L))
# first we create an object of the data's "sets"
# rbind(), head(), and tail() are used to present the info in a nice summary
# it seems like "sets" are used to organize the data and can help us selectively harvest. we want the entire dataset though...


spec <- unlist (sets [sets [, "setName"] == "LCC:Zoology", "setSpec"])
# i think this is the crucial piece of code that sets us up to extract data based on setName. by editing this part we might be able to extract everything. for now i'll just use "LCC:Zoology".

x <- oaih_list_records(baseurl, set = spec)
# this grabs all the records by the parameters specified in the previous piece of code. in our case, LCC:Zoology

head(x)
# quick preview of the data. still doesn't look like i expected it to... are we getting there?

m <- x[, "metadata"]
# apparently this removes any empty metadata? sure.

m <- oaih_transform(m[sapply(m, length) > 0L])
# finally! oaih_transform() makes things look more friendly...
# note that we call the function only on the metadata column... so can we skip to this step earlier in the process?
# think about extracting the metadata column earlier, if that makes sense

View(m)
# close enough for now.  noticing that 'creator' doesn't look right, neither does 'description' or 'format'


##########################################################################


### from here - check other subsets (Religion, Acoustics, etc) to see if problem  of "character (0)" persists.
### check the doaj URL and use verbs in-browser to double check data there
### figure out how to download data in one go. might have to append multiple subdatasets otherwise.
