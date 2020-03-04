library(ggplot2)

setwd('~/codes')
#

df = read.csv('outputs_uni_uh.csv')
df$phft_dif = df$phft - df$phft_ref

df_SC = df[df$estado == 'SC',]
df_PR = df[df$estado == 'PR',]
df_RS = df[df$estado == 'RS',]
df_GO = df[df$estado == 'GO',]
df_MA = df[df$estado == 'MA',]
df_MG = df[df$estado == 'MG',]
df_RJ = df[df$estado == 'RJ',]
df_TO = df[df$estado == 'TO',]

df_heroes = data.frame()

for(uf in unique(df$estado)){
  df_UF = df[df$estado == uf,]
  df_heroes = rbind(df_heroes, subset(df_UF, df_UF$phft_dif > quantile(df_UF$phft_dif, .95)))  # max(df_UF$phft_dif)
  
  # df_plot = df_UF[df_UF$phft_dif > quantile(df_UF$phft_dif, .95),]
  # 
  # ggplot(df_plot, aes(df_plot$phft)) +
  #   geom_histogram(binwidth = .05)
  # 
  # ggplot(df_plot, aes(df_plot$phft_dif, fill = df_plot$absortancia)) +
  #   geom_histogram(binwidth = .01)
  # 
  # ggplot(df_plot, aes(df_plot$phft_dif, fill = df_plot$open_fac)) +
  #   geom_histogram(binwidth = .01)
  # 
}

strip = function(string, position=4){
  as.character(strsplit(as.character(string),'_')[[1]][position])
}
strip2 = function(line, column = 'geometria', position=4){
  as.character(strsplit(as.character(line[column]),'_')[[1]][position])
}

strip(df$geometria[2])
strip2(as.character(df[3,]['wwr']))

area = sapply(df$geometria, strip)

df$ratio = sapply(df$geometria, strip, position = 4)  # strsplit(as.character(df$geometria),'_')[4]
df$height = sapply(df$geometria, strip, position = 5)  # strsplit(as.character(df$geometria),'_')[[1]][5]
df$area = sapply(df$geometria, strip, position = 6)  # strsplit(as.character(df$geometria),'_')[[1]][6]

df$somb = sapply(df$sombreamento, strip, position = 3)  # strsplit(as.character(df$sombreamento),'_')[[1]][3]
df$wwr = sapply(df$paf, strip, position = 3)  # strsplit(as.character(df$paf),'_')[[1]][3]

slices = c("ratio", "height", "area", "azimute", "veneziana", "componente", "absortancia", "vidro", "open_fac", "somb", "wwr")

for(slice in slices){
  plot(
    ggplot(df, aes(df[,slice])) +
    geom_bar() +  
    ggtitle(slice) +
    theme(axis.text.x = element_text(angle=90)) +
    facet_grid(.~estado)
  )
}

ggplot(df, aes(df$cgtr_cooling_ref, df$cgtr_cooling)) +
  geom_point() +  #col(stat= 'identity') +
  geom_point(aes(df$cgtr_heating_ref, df$cgtr_heating), color='red') +
  geom_abline() +
  xlim(c(0,95939348682))+ #(c(0,95939348682))+
  ylim(c(0,95939348682)) +
  # theme(axis.text.x = element_text(angle=90)) +
  facet_grid(.~estado)

df_UF = df_SC
df_plot = df_UF[df_UF$phft_dif > quantile(df_UF$phft_dif, .5)]

ggplot(df_plot, aes(df_plot$phft)) +
  geom_histogram(binwidth = .05)

ggplot(df_plot, aes(df_plot$phft_dif, fill = df_plot$absortancia)) +
  geom_histogram(binwidth = .05)

ggplot(df_plot, aes(df_plot$phft_dif, fill = df_plot$open_fac)) +
  geom_histogram(binwidth = .05)
