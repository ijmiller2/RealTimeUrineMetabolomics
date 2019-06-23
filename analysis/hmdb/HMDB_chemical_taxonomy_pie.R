library(ggplot2)
library(cowplot)

setwd("/Users/ijmiller2/Desktop/UW_2019/UrineMetabolomics/RealTimeUrineMetabolomics/data")

df <- read.table("disease_metabolite_full_data.csv", sep=",", header=TRUE, row.names=NULL)

# Remove duplicate rows based on certain columns (variables):
# https://www.datanovia.com/en/lessons/identify-and-remove-duplicate-data-in-r/
library(tidyverse)

unique_metabolite_df <- df %>% distinct(metabolite, .keep_all = TRUE)  
chemical_tax_df <- as.data.frame(table(unique_metabolite_df$chemical_taxonomy))
colnames(chemical_tax_df) = c("ChemicalTaxonomy", "Count")
chemical_tax_df <- subset(chemical_tax_df, ChemicalTaxonomy != "None")

# list of 23 hexcodes from iwanthue
colors = c("#a36533",
  "#7665d6",
  "#7cbb41",
  "#c24fb6",
  "#42c25f",
  "#da4078",
  "#4e9037",
  "#8258a0",
  "#bdb83a",
  "#aa95e2",
  "#9a8b2f",
  "#5083c6",
  "#d14e34",
  "#4cbfd8",
  "#df9847",
  "#369780",
  "#d883ba",
  "#5dc596",
  "#a14561",
  "#377947",
  "#dc7b76",
  "#a5b56d")
  #"#686d2b")

chemical_tax_list <- unique(chemical_tax_df$ChemicalTaxonomy)
chemical_tax_color_df <- data.frame(
  ChemicalTaxonomy = chemical_tax_list,
  Color = colors
)
chemical_tax_df$colors = colors


bp <- ggplot(chemical_tax_df, aes(x="", y=Count, fill=ChemicalTaxonomy))+
  geom_bar(width = 1, stat = "identity") +
  scale_fill_manual(values=chemical_tax_df$colors)
bp

pie <- bp + coord_polar("y", start=0)
a <- pie + theme_void()
a + theme(legend.position = "bottom")
a <- a + theme(legend.position = "none")
### Now for just the metabolites we observed ###

library(readxl)
observed_df <- read_excel("combined_sample_data.xlsx", sheet = "MetaboliteData")
# update after id reassignment
observed_chemical_tax_df <-  as.data.frame(table(observed_df$`Chemical Taxonomy`))
colnames(observed_chemical_tax_df) = c("ChemicalTaxonomy", "Count")
# subset the above data frame based on which chemical classes are present
observed_chemical_tax_colors = subset(chemical_tax_df, ChemicalTaxonomy %in% observed_chemical_tax_df$ChemicalTaxonomy)
observed_chemical_tax_df <- subset(observed_chemical_tax_df, ChemicalTaxonomy != "NA")

bp <- ggplot(observed_chemical_tax_df, aes(x="", y=Count, fill=ChemicalTaxonomy))+
  geom_bar(width = 1, stat = "identity") +
  scale_fill_manual(values=observed_chemical_tax_colors$colors)
bp

pie <- bp + coord_polar("y", start=0)
b <- pie + theme_void()
b <- b + theme(legend.position = "none")

p <- plot_grid(b, a, labels = c("a", "b"), hjust = 0, vjust = 1,
               scale = c(1., 1., 1., 1.))
p
