# Makng Fancy? Graphs!

data <- read.csv('~/Documents/academics/projects/open-access-representation/pythonplaytime/parsed_oai.csv')


View(data)

# making a table of values for barplot()
# parenthesis around a command will print an output
(mgender <- table(data$MGender))

(cgender <- table(data$CGender))

# barplots!
barplot(mgender)
barplot(cgender)

