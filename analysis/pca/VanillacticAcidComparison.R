
library(ggplot2)
library(cowplot)
library(readxl)

setwd("/Users/ijmiller2/Desktop/UW_2019/UrineMetabolomics/RealTimeUrineMetabolomics/data")

observed_df <- read_excel("combined_sample_data.xlsx", sheet = "SampleData")

b <- ggplot(data = observed_df, aes(x=Datetime, y=log2(`Vanillactic acid 2 TMS`))) +
  geom_line(aes(color=Subject), alpha = 0.5, show.legend = F) +
  geom_point(aes(color=Subject), alpha = 0.5, show.legend = F) +
  scale_color_manual(values=c("red", "blue")) + 
  ylab("log2(Vanillactic acid intensity)")
b

c <- ggplot(data=observed_df, aes(Subject, log2(`Vanillactic acid 2 TMS`))) +
  geom_boxplot(aes(fill=Subject), alpha = 0.5, show.legend = F) + ylab("log2(Vanillactic acid intensity)") +
  scale_fill_manual(values=c("red", "blue"), labels=c("Subject 1", "Subject 2"))
c

d <- ggplot(data = observed_df, aes(x=PC1, y=PC2)) +
  geom_point(aes(color=Subject), alpha = 0.5, size= 5 , show.legend = F) +
  scale_color_manual(values=c("red", "blue")) +
  labs(x="PC1 (0.20)", y="PC2 (0.11)") 
d

metabolite_df = read_excel("combined_sample_data.xlsx", sheet = "MetaboliteData")

e <- ggplot(data = metabolite_df, aes(x=LoadingsOnPC1, y=LoadingsOnPC2)) +
  geom_point(aes(color=MetaboliteID=="combined_sample_data.xlsx"), alpha = 0.5, size= 2.5, show.legend = F) +
  labs(x="Loadings on PC1", y="Loadings on PC2") +
  scale_color_manual(values=c("#1F77B4", "black"))
e

# https://cran.r-project.org/web/packages/cowplot/vignettes/plot_grid.html
top_row <- plot_grid(b, c, rel_widths = c(1.5, 1.))
bottom_row <- plot_grid(d, e)
plot_grid(top_row, bottom_row, ncol = 1)

