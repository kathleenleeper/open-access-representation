############################
### Makng Fancy? Graphs! ###
############################

# 1. make fancy graphs --DONE--
# 2. gender breakdown by language - run stats? --IN PROGRESS--
  ## best done when we've 'decided' on a final gender breakdown
# 3. use R to figure out gender --IN PROGRESS--
  ## package 'gender' has three or four databases to call from...
  ## try a few of them and see which is most accurate
# 4. produce a 'cleaned up' version of code that loads the latest version of 'parsed_oai.csv' with fewer comments / building code.

###########################  1  ################################


rm(list = ls())
# clearing work directory

data <- read.csv('~/Documents/projects/open-access-representation/pythonplaytime/parsed_oai.csv')
View(data)
head(data)

# making a table of values for barplot()
# parenthesis around a command will print an output
(mgender <- table(data$MGender) )
(cgender <- table(data$CGender) )
(ngender <- table(data$NGender) )
# NGender has unknowns and "parse errors"
# can they be folded into unknowns?


### fancier barplots! ###
# install.packages('ggplot2')
library(ggplot2)

# ggplot2 won't like that we're trying to plot two columns from one dataframe onto one graph.
# melting the data should solve this... 
# install.packages('reshape2')
library(reshape2)
# which columns to melt?
names(data)

# everything except the 'MGender' and 'CGender' so we use the 1:4, 7:9 notation # to pinpoint the appropriate columns
newdata <- melt(data, id = c(1:4, 8:10))

names(newdata)
View(newdata)
# now our python scripts (MGender & CGender) are themselves measures in the variable column!

ggplot(data = newdata, aes(x = variable, fill = value)) +
geom_histogram(position = 'dodge', colour = 'black', width = 0.85) +
   labs(title = 'Gender Breakdown by Two Python Scripts',
        x = 'Script Name',
        y = 'Count') +
scale_fill_manual(values = c('#FF9999', 'lightblue3', 'plum4',
                            'gray70', 'pink'),
                 labels = c('Female', 'Male', 'Unisex', 'Unknown'),
                 name = 'Gender' )

# wow finally.
# bottom line here is the "unknown" column. the better script produces fewer unknowns. in this case the clear winner is CGender.



   ####################################################################



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


# using R to match gender to names!
# maybe
# so far i've come across two packages that can do this...
## 'gender'
## 'babynames'


### R-GENDER ###

# install.packages('devtools')
## allows us to install from github?
library(devtools)

# install.packages("gender")
# works now but i spent 4 hours trying to make it work earlier, nbd.
library(gender)
# devtools::install_github("lmullen/gender-data-pkg")
## necessary data that for some reason doesn't come with the package itself

# to use, simply give gender() a name
# gender('Alex')
# gender('Skippy')

data$Author <- as.character(data$Author)
# function gender() needs a character vector

# vignette(topic = "predicting-gender", package = "gender")
## tells you exactly how to convert list of lists to dataframe!
library(dplyr)
# need 'dplyr' package to use piping commands (%>%)

# gender.data <- gender(data$Author) %>%
#     do.call(rbind.data.frame, .)
# this code comes directly from the vignette
# first line passes gender() function over data$Author and pipes the output to the second line which converts the output to a dataframe.

# head(gender.data)
# View(gender.data)
# YAYY!

# table(gender.data$gender)
# 90 female, 73 male, lots of unkowns but it's not telling us that.
# now put this into our previous graph....

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

ggplot(data = newdata, aes(x = variable, fill = value)) +
geom_histogram(position = 'dodge', colour = 'black', width = 0.85) +
labs(title = 'Gender Breakdown by Two Python Scripts',
      x = 'Script Name', 
      y = 'Count') +
scale_fill_manual(values = c('#FF9999', 'lightblue3', 'plum4',
                              'gray70'), 
                   labels = c('Female', 'Male', 'Unisex', 'Unknown'),
                   name = 'Gender' )


### WRITING NEW CSV WITH RGENDER DATA  ###


# View(data)
# write.csv(data, file = 'parsed_oai.csv')
## writes to current work directory


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
