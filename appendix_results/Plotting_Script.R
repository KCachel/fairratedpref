library(tidyverse)
library(ggnuplot)
library(ggpubr)
library(ggthemes)



#################################### Tie Analysis Plots

tie <- read_csv("tie_analysis/tie_analysis_results.csv")%>%
  dplyr::rename(Method = method) 

tie <- tie %>%
  filter(Method != 'VanillaMC')%>%
  filter(Method != 'FairMC')

tie$Method <- factor(tie$Method, levels = c("Fair-Break", "Fair-Full", "Worst", "AVG","EPIRA-Break", "Epsilon-Break", "EPIRA-Full",
                                            "Epsilon-Full"))

tie <- tie%>%
  mutate(Method=recode(Method,
                       `Worst` = "Unfair-Break"))%>%
  mutate(Method=recode(Method,
                       `AVG` = "Random-Break"))%>%
  mutate(Method=recode(Method,
                       `Fair-Break` = "FATE-Break"))%>%
  mutate(Method=recode(Method,
                       `Fair-Full` = "FATE-Rate"))%>%
  mutate(Method=recode(Method,
                       `Epsilon-Break` = "EG-Break"))%>%
  mutate(Method=recode(Method,
                       `Epsilon-Full` = "EG"))%>%
  mutate(Method=recode(Method,
                       `EPIRA-Full` = "EPIRA"))



tie$NDKL_Value <- signif(tie$NDKL_Value, digits = 3)


# multi_colors<- c('#e15759', '#f28e2b', '#9c755f','#59a14f','#4e79a7','#76B7B2', '#B07aa1', '#edc948', '#ff9da7')
# 
# multi_shapes <- c( 16, 2, 15, 18, 8, 17, 20, 7, 1)


multi_colors<- c('#e15759', '#f28e2b','#59a14f','#4e79a7','#76B7B2', '#B07aa1', '#edc948', '#ff9da7')

multi_shapes <- c( 15, 16, 2, 7, 8, 13,  11, 1)
pt_size <- 3 #3
title_size <- 10
linesize <- 1
axistext <- 14
x_stringm <- "Tie Proportion (\U03BA)"
y_stringmf <- "NDKL (\U2193)"
y_stringmu <- "ULOSS (\U2193)"
y_stringw <- "ARUL (\U2193)"
fill_limits <- c(0,1.4)
textsize <- 3
tie_breaks <- c(0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1)


make_fairness_plot <-function(dataset, shapes, colors, x_string, x_col, bks) {
  
  data <-  dataset
  
  p <- ggplot(data, aes(color = Method, x  = data[[x_col]], y = NDKL_Value, shape = Method)) +
    geom_point(size = pt_size)+
    geom_line(size = linesize)+
    #theme_gnuplot()+
    xlab(x_string)+
    ylab(y_stringmf)+
    theme_gnuplot()+
    theme(legend.position = "top",
          legend.direction = "horizontal",
          axis.title.y = element_text(size = axistext, margin = margin(r = 1)),
          axis.title.x = element_text(size = axistext,margin = margin(t = 1)),
          axis.text.x = element_text(margin = margin(t = 3)),
          axis.text.y = element_text(margin = margin(r = 3)))+
    #ggtitle('Fairness (\U2193)')+
    scale_x_continuous(breaks=bks)+
    scale_shape_manual(values=shapes)+
    scale_color_manual(values=colors)+
    guides(color=guide_legend(nrow=1))+
    guides(shape = guide_legend(nrow = 1))+
    theme(legend.title=element_blank())
  
  return(p)
}

make_uloss_plot <-function(dataset, shapes, colors, x_string, x_col, bks) {
  
  data <-  dataset
  
  p <- ggplot(data, aes(color = Method, x  = data[[x_col]], y = ULOSS_Value, shape = Method)) +
    geom_point(size = pt_size)+
    geom_line(size = linesize)+
    #theme_gnuplot()+
    xlab(x_string)+
    ylab(y_stringmu)+
    theme_gnuplot()+
    theme(legend.position = "top",
          legend.direction = "horizontal",
          axis.title.y = element_text(size = axistext, margin = margin(r = 1)),
          axis.title.x = element_text(size = axistext,margin = margin(t = 1)),
          axis.text.x = element_text(margin = margin(t = 3)),
          axis.text.y = element_text(margin = margin(r = 3)))+
    #ggtitle('Utility (\U2191)')+
    scale_x_continuous(breaks=bks)+
    scale_shape_manual(values=shapes)+
    scale_color_manual(values=colors)+
    guides(color=guide_legend(nrow=1))+
    guides(shape = guide_legend(nrow = 1))+
    theme(legend.title=element_blank())
  
  return(p)
}


make_wuloss_plot <-function(dataset, shapes, colors, x_string, x_col, bks) {
  
  data <-  dataset
  
  p <- ggplot(data, aes(color = Method, x  = data[[x_col]], y = WULOSS_Value, shape = Method)) +
    geom_point(size = pt_size)+
    geom_line(size = linesize)+
    #theme_gnuplot()+
    xlab(x_string)+
    ylab(y_stringw)+
    theme_gnuplot()+
    theme(legend.position = "top",
          legend.direction = "horizontal",
          axis.title.y = element_text(size = axistext, margin = margin(r = 1)),
          axis.title.x = element_text(size = axistext,margin = margin(t = 1)),
          axis.text.x = element_text(margin = margin(t = 3)),
          axis.text.y = element_text(margin = margin(r = 3)))+
    #ggtitle('Utility (\U2191)')+
    scale_x_continuous(breaks=bks)+
    scale_shape_manual(values=shapes)+
    scale_color_manual(values=colors)+
    guides(color=guide_legend(nrow=1))+
    guides(shape = guide_legend(nrow = 1))+
    theme(legend.title=element_blank())
  
  return(p)
}


alt <- tie %>%
  filter(dataset == 'alternating_groups')

alt_fair <- make_fairness_plot(alt, multi_shapes, multi_colors, x_stringm, 'TIE_PROP', tie_breaks)
alt_uloss <- make_uloss_plot(alt, multi_shapes, multi_colors, x_stringm, 'TIE_PROP', tie_breaks)
alt_wuloss <- make_wuloss_plot(alt, multi_shapes, multi_colors, x_stringm, 'TIE_PROP', tie_breaks)

skew <- tie %>%
  filter(dataset == 'skewed_groups')
skew_fair <- make_fairness_plot(skew, multi_shapes, multi_colors, x_stringm, 'TIE_PROP', tie_breaks)
skew_uloss <- make_uloss_plot(skew, multi_shapes, multi_colors, x_stringm, 'TIE_PROP', tie_breaks)
skew_wuloss <- make_wuloss_plot(skew, multi_shapes, multi_colors, x_stringm, 'TIE_PROP', tie_breaks)
pdfwidth <- 10
pdfheight <- 2.4


fig_alt_tie <- ggarrange(alt_fair, alt_wuloss,
                         ncol = 2, nrow = 1, common.legend = TRUE,legend = "top")

ggsave(fig_alt_tie, filename = glue::glue("plots/alt_tie_analysis_WRTRAND.pdf"), device = cairo_pdf,
       width = pdfwidth, height = pdfheight, units = "in")

fig_skew_tie <- ggarrange(skew_fair, skew_wuloss,
                          ncol = 2, nrow = 1, common.legend = TRUE,legend = "top")

ggsave(fig_skew_tie, filename = glue::glue("plots/skew_tie_analysis_WRTRAND.pdf"), device = cairo_pdf,
       width = pdfwidth, height = pdfheight, units = "in")

# ggsave(ggarrange(alt_fair, alt_uloss,
#                  ncol = 2, nrow = 1, common.legend = TRUE,legend = "top"), filename = glue::glue("plots/alt_tie_analysis_unweighted.pdf"), device = cairo_pdf,
#        width = pdfwidth, height = pdfheight, units = "in")
# 
# 
# ggsave(ggarrange(skew_fair, skew_uloss,
#                  ncol = 2, nrow = 1, common.legend = TRUE,legend = "top"), filename = glue::glue("plots/skew_tie_analysis_unweighted.pdf"), device = cairo_pdf,
#        width = pdfwidth, height = pdfheight, units = "in")


#################################### Datasets Fairness-Utility Plots

electronics <- read_csv("electronics/results_electronics.csv")%>%
  dplyr::rename(Method = method)%>%
  filter(Method != 'VanillaMC')%>%
  filter(Method != 'FairMC')

electronics$Method <- factor(electronics$Method, levels = c("Fair-Break", "Fair-Full", "Worst", "AVG","EPIRA-Break",
                                                            "Epsilon-Break", "EPIRA-Full", "Epsilon-Full"))

electronics <- electronics%>%
  mutate(Method=recode(Method,
                       `Worst` = "Unfair-Break"))%>%
  mutate(Method=recode(Method,
                       `AVG` = "Random-Break")) %>%
  mutate(Method=recode(Method,
                       `Fair-Break` = "FATE-Break"))%>%
  mutate(Method=recode(Method,
                       `Fair-Full` = "FATE-Rate"))%>%
  mutate(Method=recode(Method,
                       `Epsilon-Break` = "EG-Break"))%>%
  mutate(Method=recode(Method,
                       `Epsilon-Full` = "EG"))%>%
  mutate(Method=recode(Method,
                       `EPIRA-Full` = "EPIRA"))


xwines <- read_csv("xwines/results_xwines.csv")%>%
  dplyr::rename(Method = method)%>%
  filter(Method != 'VanillaMC')%>%
  filter(Method != 'FairMC')

xwines$Method <- factor(xwines$Method, levels = c("Fair-Break", "Fair-Full", "Worst", "AVG","EPIRA-Break",
                                                  "Epsilon-Break", "EPIRA-Full", "Epsilon-Full"))

xwines <- xwines%>%
  mutate(Method=recode(Method,
                       `Worst` = "Unfair-Break"))%>%
  mutate(Method=recode(Method,
                       `AVG` = "Random-Break"))%>%
  mutate(Method=recode(Method,
                       `Fair-Break` = "FATE-Break"))%>%
  mutate(Method=recode(Method,
                       `Fair-Full` = "FATE-Rate"))%>%
  mutate(Method=recode(Method,
                       `Epsilon-Break` = "EG-Break"))%>%
  mutate(Method=recode(Method,
                       `Epsilon-Full` = "EG"))%>%
  mutate(Method=recode(Method,
                       `EPIRA-Full` = "EPIRA"))

xwines <- xwines%>%
  mutate(Method=recode(Method,
                       `Worst` = "Unfair-Break"))%>%
  mutate(Method=recode(Method,
                       `AVG` = "Random-Break"))%>%
  mutate(Method=recode(Method,
                       `Fair-Break` = "FATE-Break"))%>%
  mutate(Method=recode(Method,
                       `Fair-Full` = "FATE-Rate"))%>%
  mutate(Method=recode(Method,
                       `Epsilon-Break` = "EG-Break"))%>%
  mutate(Method=recode(Method,
                       `Epsilon-Full` = "EG"))%>%
  mutate(Method=recode(Method,
                       `EPIRA-Full` = "EPIRA"))


modcloth <- read_csv("modcloth/results_modcloth.csv")%>%
  dplyr::rename(Method = method)%>%
  filter(Method != 'VanillaMC')%>%
  filter(Method != 'FairMC')

modcloth$Method <- factor(modcloth$Method, levels = c("Fair-Break", "Fair-Full", "Worst", "AVG","EPIRA-Break",
                                                      "Epsilon-Break", "EPIRA-Full", "Epsilon-Full"))

modcloth <- modcloth%>%
  mutate(Method=recode(Method,
                       `Worst` = "Unfair-Break"))%>%
  mutate(Method=recode(Method,
                       `AVG` = "Random-Break"))%>%
  mutate(Method=recode(Method,
                       `Fair-Break` = "FATE-Break"))%>%
  mutate(Method=recode(Method,
                       `Fair-Full` = "FATE-Rate"))%>%
  mutate(Method=recode(Method,
                       `Epsilon-Break` = "EG-Break"))%>%
  mutate(Method=recode(Method,
                       `Epsilon-Full` = "EG"))%>%
  mutate(Method=recode(Method,
                       `EPIRA-Full` = "EPIRA"))
hr <- read_csv("hr/results_hr.csv")%>%
  dplyr::rename(Method = method)%>%
  filter(Method != 'VanillaMC')%>%
  filter(Method != 'FairMC')

hr$Method <- factor(hr$Method, levels = c("Fair-Break", "Fair-Full", "Worst", "AVG","EPIRA-Break",
                                          "Epsilon-Break", "EPIRA-Full", "Epsilon-Full"))

hr <- hr%>%
  mutate(Method=recode(Method,
                       `Worst` = "Unfair-Break"))%>%
  mutate(Method=recode(Method,
                       `AVG` = "Random-Break"))%>%
  mutate(Method=recode(Method,
                       `Fair-Break` = "FATE-Break"))%>%
  mutate(Method=recode(Method,
                       `Fair-Full` = "FATE-Rate"))%>%
  mutate(Method=recode(Method,
                       `Epsilon-Break` = "EG-Break"))%>%
  mutate(Method=recode(Method,
                       `Epsilon-Full` = "EG"))%>%
  mutate(Method=recode(Method,
                       `EPIRA-Full` = "EPIRA"))


make_fairutil_plot <-function(data, dataset, shapes, colors, x_string, X_feature) {
  
  y_string <- 'NDKL (\U2193)'
  
  p <- ggplot(data, aes(color = Method, x  = {{X_feature}}, y = NDKL_Value, shape = Method)) +
    geom_point(size = pt_size)+
    #geom_line(size = linesize)+
    #theme_gnuplot()+
    xlab(x_string)+
    ylab(y_string)+
    theme_gnuplot()+
    theme(legend.position = "top",
          legend.direction = "horizontal",
          axis.title.y = element_text(size = axistext, margin = margin(r = 1)),
          axis.title.x = element_text(size = axistext,margin = margin(t = 1)),
          axis.text.x = element_text(margin = margin(t = 3)),
          axis.text.y = element_text(margin = margin(r = 3)))+
    ggtitle(glue::glue("{dataset}"))+
    scale_shape_manual(values=shapes)+
    scale_color_manual(values=colors)+
    theme(legend.title=element_blank()) +
    guides(color=guide_legend(nrow=1))+
    guides(shape = guide_legend(nrow = 1))
  return(p)
}
#WUloss Version
wuloss_x_string <- 'ARUL (\U2193)'
electronics_p <- make_fairutil_plot(electronics, 'Electronics',  multi_shapes, multi_colors, wuloss_x_string, WULOSS_Value)
xwines_p <- make_fairutil_plot(xwines, 'XWines',  multi_shapes, multi_colors, wuloss_x_string, WULOSS_Value)
modcloth_p <- make_fairutil_plot(modcloth, 'ModCloth',  multi_shapes, multi_colors, wuloss_x_string, WULOSS_Value)
hr_p <- make_fairutil_plot(hr, 'HR',  multi_shapes, multi_colors, wuloss_x_string, WULOSS_Value)


fairutil <- ggarrange(electronics_p, xwines_p, modcloth_p, hr_p,
                      ncol = 4, nrow = 1, common.legend = TRUE, legend = "top")
pdfwidth <- 10
pdfheight <- 2.5
ggsave(fairutil, filename = glue::glue("plots/datasets_results_WRTRAND.pdf"), device = cairo_pdf,
       width = pdfwidth, height = pdfheight, units = "in")

# #ULoss Version
# uloss_x_string <- 'ULOSS (\U2193)'
# electronics_p_un <- make_fairutil_plot(electronics, 'Electronics',  multi_shapes, multi_colors, uloss_x_string, ULOSS_Value)
# xwines_p_un <- make_fairutil_plot(xwines, 'XWines',  multi_shapes, multi_colors, uloss_x_string, ULOSS_Value)
# modcloth_p_un <- make_fairutil_plot(modcloth, 'ModCloth',  multi_shapes, multi_colors, uloss_x_string, ULOSS_Value)
# hr_p_un <- make_fairutil_plot(hr, 'HR',  multi_shapes, multi_colors, uloss_x_string, ULOSS_Value)
# 
# 
# fairutil_un <- ggarrange(electronics_p_un, xwines_p_un, modcloth_p_un, hr_p_un,
#                       ncol = 4, nrow = 1, common.legend = TRUE, legend = "top")
# 
# ggsave(fairutil_un, filename = glue::glue("plots/datasets_results_unweighted.pdf"), device = cairo_pdf,
#        width = pdfwidth, height = pdfheight, units = "in")



#################################### Tie Blocks Plots

tie_blocks <- read_csv("tie_blocks/tie_blocks_results.csv")%>%
  dplyr::rename(Method = method) 

tie_blocks <- tie_blocks %>%
  filter(Method != 'VanillaMC')%>%
  filter(Method != 'FairMC')

tie_blocks$Method <- factor(tie_blocks$Method, levels = c("Fair-Break", "Fair-Full", "Worst", "AVG","EPIRA-Break", "Epsilon-Break", "EPIRA-Full",
                                                          "Epsilon-Full"))

tie_blocks <- tie_blocks%>%
  mutate(Method=recode(Method,
                       `Worst` = "Unfair-Break"))%>%
  mutate(Method=recode(Method,
                       `AVG` = "Random-Break"))%>%
  mutate(Method=recode(Method,
                       `FairMC` = "FMC"))%>%
  mutate(Method=recode(Method,
                       `Fair-Break` = "FATE-Break"))%>%
  mutate(Method=recode(Method,
                       `Fair-Full` = "FATE-Rate"))%>%
  mutate(Method=recode(Method,
                       `Epsilon-Break` = "EG-Break"))%>%
  mutate(Method=recode(Method,
                       `Epsilon-Full` = "EG"))%>%
  mutate(Method=recode(Method,
                       `EPIRA-Full` = "EPIRA"))
alt_blocks <- tie_blocks %>%
  filter(dataset == 'alternating_groups')

skew_blocks <- tie_blocks %>%
  filter(dataset == 'skewed_groups')


make_tieblock_plot <-function(dataset, shapes, colors, x_string, x_col, bks, y_string, y_col, tie_type) {
  
  data <-  dataset %>%
    filter(TIE_TYPE == .env$tie_type)
  
  p <- ggplot(data, aes(color = Method, x  = .data[[x_col]], y = .data[[y_col]], shape = Method)) +
    geom_point(size = pt_size)+
    geom_line(size = linesize)+
    #theme_gnuplot()+
    xlab(x_string)+
    ylab(y_string)+
    theme_gnuplot()+
    theme(legend.position = "top",
          legend.direction = "horizontal",
          axis.title.y = element_text(size = axistext, margin = margin(r = 1)),
          axis.title.x = element_text(size = axistext,margin = margin(t = 1)),
          axis.text.x = element_text(margin = margin(t = 3)),
          axis.text.y = element_text(margin = margin(r = 3)))+
    ggtitle(glue::glue("{tie_type}"))+
    scale_x_continuous(breaks=bks)+
    scale_shape_manual(values=shapes)+
    scale_color_manual(values=colors)+
    guides(color=guide_legend(nrow=1))+
    guides(shape = guide_legend(nrow = 1))+
    theme(legend.title=element_blank())
  
  return(p)
}

wuloss_y_string <- 'ARUL (\U2193)'
uloss_y_string <- 'ULOSS (\U2193)'
ndkl_y_string <- 'NDKL (\U2193)'
block_breaks <- c(1, 2, 3, 4,5)
block_x_string <- 'Tied Blocks (\U03B2)'

alt_top_ndkl <- make_tieblock_plot(alt_blocks, multi_shapes, multi_colors, block_x_string, 'TIE_BLOCKS',
                                   block_breaks, ndkl_y_string, 'NDKL_Value', 'Top' )
alt_top_wuloss <- make_tieblock_plot(alt_blocks, multi_shapes, multi_colors, block_x_string, 'TIE_BLOCKS',
                                     block_breaks, wuloss_y_string, 'WULOSS_Value', 'Top' )
alt_top_uloss <- make_tieblock_plot(alt_blocks, multi_shapes, multi_colors, block_x_string, 'TIE_BLOCKS',
                                    block_breaks, uloss_y_string, 'ULOSS_Value', 'Top' )
alt_alt_ndkl <- make_tieblock_plot(alt_blocks, multi_shapes, multi_colors, block_x_string, 'TIE_BLOCKS',
                                   block_breaks, ndkl_y_string, 'NDKL_Value', 'Interleaved' )
alt_alt_wuloss <- make_tieblock_plot(alt_blocks, multi_shapes, multi_colors, block_x_string, 'TIE_BLOCKS',
                                     block_breaks, wuloss_y_string, 'WULOSS_Value', 'Interleaved' )
alt_alt_uloss <- make_tieblock_plot(alt_blocks, multi_shapes, multi_colors, block_x_string, 'TIE_BLOCKS',
                                    block_breaks, uloss_y_string, 'ULOSS_Value', 'Interleaved' )
alt_bot_ndkl <- make_tieblock_plot(alt_blocks, multi_shapes, multi_colors, block_x_string, 'TIE_BLOCKS',
                                   block_breaks, ndkl_y_string, 'NDKL_Value', 'Bottom' )
alt_bot_wuloss <- make_tieblock_plot(alt_blocks, multi_shapes, multi_colors, block_x_string, 'TIE_BLOCKS',
                                     block_breaks, wuloss_y_string, 'WULOSS_Value', 'Bottom' )
alt_bot_uloss <- make_tieblock_plot(alt_blocks, multi_shapes, multi_colors, block_x_string, 'TIE_BLOCKS',
                                    block_breaks, uloss_y_string, 'ULOSS_Value', 'Bottom' )

skew_top_ndkl <- make_tieblock_plot(skew_blocks, multi_shapes, multi_colors, block_x_string, 'TIE_BLOCKS',
                                    block_breaks, ndkl_y_string, 'NDKL_Value', 'Top' )
skew_top_wuloss <- make_tieblock_plot(skew_blocks, multi_shapes, multi_colors, block_x_string, 'TIE_BLOCKS',
                                      block_breaks, wuloss_y_string, 'WULOSS_Value', 'Top' )
skew_top_uloss <- make_tieblock_plot(skew_blocks, multi_shapes, multi_colors, block_x_string, 'TIE_BLOCKS',
                                     block_breaks, uloss_y_string, 'ULOSS_Value', 'Top' )
skew_alt_ndkl <- make_tieblock_plot(skew_blocks, multi_shapes, multi_colors, block_x_string, 'TIE_BLOCKS',
                                    block_breaks, ndkl_y_string, 'NDKL_Value', 'Interleaved' )
skew_alt_wuloss <- make_tieblock_plot(skew_blocks, multi_shapes, multi_colors, block_x_string, 'TIE_BLOCKS',
                                      block_breaks, wuloss_y_string, 'WULOSS_Value', 'Interleaved' )
skew_alt_uloss <- make_tieblock_plot(skew_blocks, multi_shapes, multi_colors, block_x_string, 'TIE_BLOCKS',
                                     block_breaks, uloss_y_string, 'ULOSS_Value', 'Interleaved' )
skew_bot_ndkl <- make_tieblock_plot(skew_blocks, multi_shapes, multi_colors, block_x_string, 'TIE_BLOCKS',
                                    block_breaks, ndkl_y_string, 'NDKL_Value', 'Bottom' )
skew_bot_wuloss <- make_tieblock_plot(skew_blocks, multi_shapes, multi_colors, block_x_string, 'TIE_BLOCKS',
                                      block_breaks, wuloss_y_string, 'WULOSS_Value', 'Bottom' )
skew_bot_uloss <- make_tieblock_plot(skew_blocks, multi_shapes, multi_colors, block_x_string, 'TIE_BLOCKS',
                                     block_breaks, uloss_y_string, 'ULOSS_Value', 'Bottom' )

# pdfwidth <- 10
# pdfheight <- 2.5
# 
# 
# ggsave(ggarrange(skew_top_ndkl, skew_alt_ndkl, skew_bot_ndkl,
#                  ncol = 3, nrow = 1, common.legend = TRUE,legend = "top"), filename = glue::glue("plots/skew_tie_blocks_ndkl.pdf"), device = cairo_pdf,
#        width = pdfwidth, height = pdfheight, units = "in")
# 
# ggsave(ggarrange(alt_top_ndkl, alt_alt_ndkl, alt_bot_ndkl,
#                  ncol = 3, nrow = 1, common.legend = TRUE,legend = "top"), filename = glue::glue("plots/alt_tie_blocks_ndkl.pdf"), device = cairo_pdf,
#        width = pdfwidth, height = pdfheight, units = "in")

pdfwidth <- 10
pdfheight <- 5


ggsave(ggarrange(skew_top_ndkl, skew_alt_ndkl, skew_bot_ndkl, skew_top_wuloss, skew_alt_wuloss, skew_bot_wuloss,
                 ncol = 3, nrow = 2, common.legend = TRUE,legend = "top"), filename = glue::glue("plots/skew_tie_blocks_WRTRAND.pdf"), device = cairo_pdf,
       width = pdfwidth, height = pdfheight, units = "in")

ggsave(ggarrange(alt_top_ndkl, alt_alt_ndkl, alt_bot_ndkl, alt_top_wuloss, alt_alt_wuloss, alt_bot_wuloss,
                 ncol = 3, nrow = 2, common.legend = TRUE,legend = "top"), filename = glue::glue("plots/alt_tie_blocks_WRTRAND.pdf"), device = cairo_pdf,
       width = pdfwidth, height = pdfheight, units = "in")


# pdfwidth <- 10
# pdfheight <- 7.5
# 
# ggsave(ggarrange(skew_top_ndkl, skew_alt_ndkl, skew_bot_ndkl, skew_top_wuloss, skew_alt_wuloss, skew_bot_wuloss,
#                  skew_top_uloss, skew_alt_uloss, skew_bot_uloss,
#                  ncol = 3, nrow = 3, common.legend = TRUE,legend = "top"), filename = glue::glue("plots/skew_tie_blocks_wunweight.pdf"), device = cairo_pdf,
#        width = pdfwidth, height = pdfheight, units = "in")
# 
# ggsave(ggarrange(alt_top_ndkl, alt_alt_ndkl, alt_bot_ndkl, alt_top_wuloss, alt_alt_wuloss, alt_bot_wuloss,
#                  alt_top_uloss, alt_alt_uloss, alt_bot_uloss,
#                  ncol = 3, nrow = 3, common.legend = TRUE,legend = "top"), filename = glue::glue("plots/alt_tie_blocks_wunweight.pdf"), device = cairo_pdf,
#        width = pdfwidth, height = pdfheight, units = "in")