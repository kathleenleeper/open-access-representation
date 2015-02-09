rm(list = ls())
# clearing directory

data <- read.csv('~/Documents/projects/open-access-representation/pythonplaytime/parsed_oai.csv')
# reading data


library(ggplot2)
library(reshape2)
library(devtools)
library(gender)
library(dplyr)
