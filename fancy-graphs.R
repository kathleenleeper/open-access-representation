############################
### Makng Fancy? Graphs! ###
############################

data <- read.csv('~/Documents/academics/projects/open-access-representation/pythonplaytime/parsed_oai.csv')

View(data)

## making a table of values for barplot()
## parenthesis around a command will print an output
# (mgender <- table(data$MGender) )
# (cgender <- table(data$CGender) )


### barplots! ###
# barplot(mgender)
# X11() # opens new graphing window
# barplot(cgender)

### fancier barplots! ###
# install.packages(ggplot2)
library(ggplot2)

ggplot(data = data, aes(MGender)) +  geom_histogram()
# basic example, now put MGender and CGender on the same graph

# ggplot2 doesn't like that we're trying to plot two columns from one dataframe onto one graph.
# melting the data should solve this... 
# install.packages('reshape2')
library(reshape2)

# which columns to melt?
names(data)
View(data)
# everything except the 'MGender' and 'CGender' so we use the 1:4, 7:9 notation to pinpoint the appropriate columns
newdata <- melt(data, id = c(1:4, 7:9))                  

names(newdata)
View(newdata)
# double-checking and everything looks good...
# now our python scripts (MGender & CGender) are themselves measures in the variable column!
# this is a pretty useful function, esp. if we run multiple scripts to determine gender.

ggplot(data = newdata, aes(x = variable, fill = value)) +
geom_histogram(position = 'dodge', colour = 'black', width = 0.85) +
labs(title = 'Gender Breakdown by Two Python Scripts',
     x = 'Script Name', 
     y = 'Count') +
scale_fill_manual(values = c('#FF9999', 'lightblue3', 'plum4',
                              'gray70'), 
                  labels = c('Female', 'Male', 'Unisex', 'Unknown'),
                  name = 'Gender' )
# wow finally.
# bottom line here is the "unknown" column. the better script produces fewer unknowns. in this case the clear winner is CGender.



   ####################################################################



## can we fit two columns of data on a single graph more simply, without invoking melt()?
## maybe with aes_string()
# ggplot(data = data,
#       aes_string(MGender, CGender)) +
##       # aes_string() allows you to pass a string to ggplot
#       # this might be a way to build the plot without using melt()
#       # keeping this for future reference
# geom_histogram(position = 'dodge')
# on second thought using aes_string () might require a for() loop, in which case it's not the easiest option.
# reference- http://stackoverflow.com/questions/13260626/selecting-data-frame-columns-to-plot-in-ggplot2


       ############################################################


# what is the gender breakdown by language?
table(newdata$Language)
# our only factors are Portugese and English...

head(data)

(lang <- table(data$CGender, data$Language))
# building table of values
# for two categorical variables we'll use a chi-square test

chisq.test(lang)
# this suggests that 'gender' is not affected by 'language' which doesn't seem right... i'll come back to this. definitely doing something wrong.


        #####################################################


## using R to match gender to names!
