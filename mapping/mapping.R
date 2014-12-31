# Building Map of Representation by Country
# Going for something simple for now, maybe shading with darker vs. lighter colors

install.packages(c('ggplot2', 'maptools', 'RColorBrewer', 'classInt'))
install.packages('choroplethr')
# downloading relevant packages

library(ggplot2)
library(maptools)
library(RColorBrewer)
library(classInt)
library(cloroplethr)
# activating packages

world <- readShapePoly("yourworldshapefile")
?readShapePoly
