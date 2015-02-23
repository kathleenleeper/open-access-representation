                        ############################
                        ###        R Code        ###
                        ############################

# 1. use R to figure out gender  -- IN PROGRESS --
  # will come back to this later...
  # R doesn't like current name format (Paul C). can we use github to revert
  # back to the older format of first name only?
# 2. make fancy graphs  --IN PROGRESS -- 
# 3. take consensus of API scripts.
# 4. produce a 'cleaned up' version of code that loads the latest version of 'parsed_oai.csv' with fewer comments / building code.  -- IN PROGRESS--
# 5. create RPubs document / markdown file!

      ######################## DATA PREP #############################


rm(list = ls())
# clearing work directory

data <- read.csv('~/Documents/projects/open-access-representation/pythonplaytime/parsed_oai_COPY.csv')
# working with a stable copy now.
View(data)
head(data)

# installing necessary packages... comment in as necessary
# install.packages('gender')
# install.packages('devtools')
# install.packages('dplyr')
# install.packages('ggplot2')
# install.packages('reshape')
# devtools::install_github("lmullen/gender-data-pkg")

library(devtools)
library(gender)
library(dplyr) # for piping commands (%>%)
library(ggplot2)
library(reshape) # such an important package to this process



     #############################  1  ################################


# simply give gender() a name
gender('Alex')

data$Author <- as.character(data$Author)
# function gender() needs a character vector so we convert our author list

gender.data <- gender(data$Author) %>% do.call(rbind.data.frame, .)
# this code comes directly from the vignette
# first line passes gender() function over data$Author and pipes the output to the second line which converts the output to a dataframe.

View(gender.data)
# not working, more than likely because 'Author' data is not a single name.
# not difficult to fix, we can split the data in that column

### use colsplit() from reshape package. 



     #############################  2  ################################


# start by exploring the existing gender breakdown in tabular format
(table(data$MGender))
(table(data$CGender))
(table(data$NGender))
# we can see that CGender has a "unisex" variable and NGender has an "misparsed" variable. both might get in the way

# let's convert 'misparsed' to 'unknown' in NGender column
data$NGender[data$NGender == 'misparsed'] <- 'unknown'
table(data$NGender)

data$NGender <- factor(data$NGender)
# gets rid of annoying 'misparsed' category with zero values

# next, melting data allows us to put things in proper format for ggplot2
# what to melt?
names(data)
# everything except the gender APIs so we use the 1:4, 7:9 notation to pinpoint the appropriate columns
newdata <- melt(data, id = c(1:4, 8:10))

View(newdata)
# now our python APIs are themselves measures in the variable column!


# plotting all the API data
ggplot(data = newdata, aes(x = variable, fill = value)) +
geom_histogram(position = 'dodge', colour = 'black', width = 0.85) + 
labs(title = 'Gender Breakdown by Three Python Scripts',
     x = 'Script Name',
     y = 'Count') +
scale_fill_manual(values = c('#FF9999', 'lightblue3', 'plum4', 'gray70'), 
                 labels = c('Female', 'Male', 'Unknown', 'Unisex', 'Misparsed'),
                 name = 'Gender')

# ggsave(filename = 'python-APIs.png', path = '~/Desktop')

# bottom line here is the "unknown" column. the better script produces fewer unknowns. in this case the clear winner is CGender.



#######################################################################

## can we fit two columns of data on a single graph more simply, without invoking melt()?
## maybe with aes_string()
# ggplot(data = data,
#      aes_string(MGender, CGender)) +
       # aes_string() allows you to pass a string to ggplot
       # this might be a way to build the plot without using melt()
       # keeping this for future reference
# geom_histogram(position = 'dodge')
# on second thought using aes_string () might require a for() loop, in which case it's not the easiest option.
# reference- http://stackoverflow.com/questions/13260626/selecting-data-frame-columns-to-plot-in-ggplot2



       ###########################  2  #################################


# what is the gender breakdown by language?
table(newdata$Language)
# our only factors are Portugese and English...

(lang <- table(data$CGender, data$Language))
# building table of values
# for two categorical variables we'll use a chi-square test

chisq.test(lang)
# this suggests that 'gender' is not affected by 'language' which doesn't seem right... i'll come back to this. definitely doing something wrong.


       ###########################  3  ##################################


# we want a consensus of API scripts, or a way to summarize what each is telling us.
# e.g. 75% of our python scripts say Paul is male.

census <- data[4:7]
head(census)
# taking a subset of data to make melting easier

census2 <- melt(census, id = Author)
head(census2)
# melting so that each API's gender assignment is a value

census3 <- as.data.frame(table(census2$Author, census2$value))
head(census3)
# creating a table then outputting it as a dataframe.

# plotting....
ggplot(data = census2, aes(x = Author, fill = value)) +
geom_bar(position = 'dodge')
# don't think this lends itself to graphing...
# ideal output would probably be a table of sorts. even better: write a function that outputs the 'correct' gender based on frequency taken from the different API scripts.


#################################################
# this should probably be in Section 1 but i'll #
# leave it here for now. might contain useful   #
# code.                                         #
#################################################

# View(data)
# data$RGender <- gender.data$gender
# put into original dataframe


# levels(data$RGender) <- c(levels(data$RGender), "unknown")
# because factors suck we have to add a factor level in order to convert our NAs to unknowns
# data$RGender[is.na(data$RGender)] = 'unknown'
# table(data$RGender)

# newdata <- melt(data, id = c(1:4, 7:9))                  
# remelting data; we actually don't have to change the previous code!
# View(newdata)


# turns out the gender package can use multiple data sources to determine gender....
## ssa method
## ipums method
## kantrowitz method
## genderize method, which comes from social networks!
## demo method, demo only and 'not suitable for research purposes'


##### genderize ######

genderize <- gender(data$Author, mode = 'genderize') %>%
    do.call(rbind.data.frame, .)
# doesn't work when mode is called... outputs error
# Error in if (result$gender == "female") { : argument is of length zero
table(genderize$gender)


### BABYNAMES ###

# install.packages('babynames')
library(babynames)
# for now it looks like 'babynames' just provides a few more datasets to pull gender data from, some of which we've already accessed...
