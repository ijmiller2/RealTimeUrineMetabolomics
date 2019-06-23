library(ggplot2)
library(cowplot)

setwd("/Users/ijmiller2/Desktop/UW_2019/UrineMetabolomics/RealTimeUrineMetabolomics/data")

#### Disease Category Tree Map ####
library(treemapify)
library(ggplotify)

df <- read.delim("hmdb_disease_metabolite_count.tsv", header=TRUE, row.names=NULL)
df <- subset(df, General.Category != "NA")

ggplot(df, aes(area = metabolite_count, fill = General.Category, label = disease, 
               subgroup = General.Category, subgroup2 = disease)) +
  geom_treemap(show.legend = FALSE) + 
  geom_treemap_subgroup_text(place = "bottom", 
                             grow = T, 
                             alpha = 0.5, 
                             colour = "black", 
                             fontface = "italic", 
                             min.size = 0) +
  geom_treemap_text(colour = "white", 
                    place = "topleft", 
                    reflow = T)

