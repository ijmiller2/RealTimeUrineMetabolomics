
library(pheatmap)
library(RColorBrewer)
library(readxl)
# for "inferno"
library(viridis)

# set workding directory
setwd("/Users/ijmiller2/Desktop/UW_2019/UrineMetabolomics/RealTimeUrineMetabolomics/data")

### load data from p-val filtered .csv ###
biometric_correlations_filtered_df <- read.table("combined_correlations_w_metadat_colsorted_identified.csv", sep=",", header=TRUE)
matrix = as.matrix(as.data.frame(lapply(biometric_correlations_filtered_df[,2:14], as.numeric)))
matrix_rownames = as.matrix(as.data.frame(lapply(biometric_correlations_filtered_df[,1], as.character)))
rownames(matrix) = matrix_rownames

# set up colors for chemical taxonomy
mat_colors <- list(ChemicalTaxonomy = brewer.pal(10, "Set3"))
taxonomies <- list(ChemicalTaxonomy = unique(biometric_correlations_filtered_df$Chemical.Taxonomy))
names(mat_colors$ChemicalTaxonomy) = taxonomies$ChemicalTaxonomy
# sort chemical taxonomy names alphabetically (to put "unknown" at end of legend)
names(mat_colors$ChemicalTaxonomy) = sort(names(mat_colors$ChemicalTaxonomy))

# make "unknown" grey and "homogenous" non-metals purple
mat_colors$ChemicalTaxonomy[[3]] = "#BC80BD"
mat_colors$ChemicalTaxonomy[[9]] = "#CCEBC5"
mat_colors$ChemicalTaxonomy[[10]] = "#D9D9D9"

# set up dataframe with row annotations
mat_row <- data.frame(ChemicalTaxonomy = biometric_correlations_filtered_df$Chemical.Taxonomy)
rownames(mat_row) = matrix_rownames

pheatmap(
  mat               = matrix,
  color             = inferno(10),
  border_color      = NA,
  show_colnames     = TRUE,
  show_rownames     = TRUE,
  annotation_row    = mat_row,
  annotation_colors = mat_colors,
  drop_levels       = TRUE,
  fontsize          = 14,
  main              = "Biometric Correlation Analysis"
)



# now let's add column groups (for Repeated Measures vs. Spearman's Rho)

# set column colors, add to matrix colors data object
column_colors = c("#a01f1a","#3cda63")
mat_colors$Correlation = column_colors
names(mat_colors$Correlation) = c("Repeated Measures", "Spearman's Rho")

# manually assign column names to coefficient type
column_names = names(biometric_correlations_filtered_df[,2:14])
Correlation = c("Repeated Measures", "Repeated Measures", "Repeated Measures", "Repeated Measures", "Repeated Measures", "Repeated Measures", "Repeated Measures", "Repeated Measures", "Repeated Measures", "Repeated Measures", "Repeated Measures", "Spearman's Rho", "Spearman's Rho")

# create dataframe for column name and type connection
mat_col = as.data.frame(Correlation)
rownames(mat_col) = column_names

pheatmap(
  mat               = matrix,
  color             = inferno(10),
  border_color      = NA,
  show_colnames     = TRUE,
  show_rownames     = TRUE,
  cluster_cols      = FALSE,
  annotation_row    = mat_row,
  annotation_colors = mat_colors,
  annotation_col    = mat_col,
  drop_levels       = TRUE,
  fontsize          = 14,
  main              = "Biometric Correlation Analysis",
  gaps_col          = as.vector(c(11))
)

# regular colors, no row names

pheatmap(
  mat               = matrix,
  border_color      = NA,
  show_colnames     = TRUE,
  show_rownames     = FALSE,
  cluster_cols      = FALSE,
  annotation_row    = mat_row,
  annotation_colors = mat_colors,
  annotation_col    = mat_col,
  drop_levels       = TRUE,
  fontsize          = 14,
  gaps_col          = as.vector(c(11))
)


