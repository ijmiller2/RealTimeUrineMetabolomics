
library(ggplot2)
library(cowplot)

setwd("/Users/ijmiller2/Desktop/UW_2019/UrineMetabolomics/RealTimeUrineMetabolomics/")

PCA_df = read.table("data/PC1and2WithVolumesRunOrder.tsv", header = TRUE, sep = "\t")

ggplot(data=PCA_df, aes(x=PC1, y=PC2)) +
  geom_point(aes(col=RunOrder, size = Volume))

a <- ggplot(data=PCA_df, aes(x=PC1, y=PC2)) +
  geom_point(aes(col=RunDay, size = Volume))
a

ggplot(data=PCA_df, aes(RunDay, PC1)) +
  geom_boxplot(aes(fill=RunDay))

ggplot(data=PCA_df, aes(x=RunOrder, y=PC1)) +
  geom_point(aes(col=RunDay, size = Volume))

ggplot(data=PCA_df, aes(x=RunOrder, y=PC2)) +
  geom_point(aes(col=RunDay, size = Volume))


### QC plot ### 

# A. color by user, size by volume
a <- ggplot(data=PCA_df, aes(x=PC1, y=PC2)) +
  geom_point(aes(col=Individual, size = Volume), alpha = 0.5) +
  scale_colour_manual(values=c("#0000FF", "#FF0000"), 
                    name="Subject", 
                    labels=c("Subject 1", "Subject 2"))

# B. density plot of volumes
b <- ggplot(data=PCA_df, aes(Volume)) +
  geom_density(aes(fill=Individual), alpha=0.5) +
  scale_fill_manual(values=c("#0000FF", "#FF0000"), 
                      name="Subject", 
                      labels=c("Subject 1", "Subject 2"))

# comparing volumes
t.test(subset(PCA_df, Subject=="Subject1")$Volume, subset(PCA_df, Subject=="Subject2")$Volume, var.equal = F)

# C. color by run number
c <- ggplot(data=PCA_df, aes(x=PC1, y=PC2)) +
  geom_point(aes(col=RunOrder), alpha = 0.8, size=5)

# D. Color by run day
d <- ggplot(data=PCA_df, aes(x=PC1, y=PC2)) +
  geom_point(aes(col=factor(RunDay)), alpha = 0.8, size=5)

p <- plot_grid(a, b, c, d, labels = "AUTO", hjust = 0, vjust = 1,
               scale = c(1., 1., 1., 1.))
p
