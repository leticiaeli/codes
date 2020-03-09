library(ggplot2)

setwd('~/codes')
#

strip = function(string, split_char='_', position=4){
  # para identificar características de geometria a partir do nome do slice
  as.character(strsplit(as.character(string),split_char)[[1]][position])
}

df = read.csv('outputs_uni_uh.csv')

# diferencas entre caso e ref
df$phft_dif = df$phft - df$phft_ref
df$cgtr_dif = df$cgtr_cooling + df$cgtr_heating - df$cgtr_cooling_ref - df$cgtr_heating_ref

#area da uh base
area_uh = 38.58

# identifica caracteristicas a partir do nome do slice
df$ratio = sapply(df$geometria, strip, position = 4)  # strsplit(as.character(df$geometria),'_')[4]
df$height = sapply(df$geometria, strip, position = 5)  # strsplit(as.character(df$geometria),'_')[[1]][5]
df$area = sapply(df$geometria, strip, position = 6)  # strsplit(as.character(df$geometria),'_')[[1]][6]
df$area = ifelse(
  substr(df$area,1,1) == '0', area_uh, ifelse(
    substr(df$area,1,1) == '1', 1.5*area_uh,
    2*area_uh
  )
)
df$cgtr_dif = df$cgtr_dif/df$area

df$somb = sapply(df$sombreamento, strip, position = 3)  # strsplit(as.character(df$sombreamento),'_')[[1]][3]
df$wwr = sapply(df$paf, strip, position = 3)  # strsplit(as.character(df$paf),'_')[[1]][3]

# separe por estado
df_SC = df[df$estado == 'SC',]
df_PR = df[df$estado == 'PR',]
df_RS = df[df$estado == 'RS',]
df_GO = df[df$estado == 'GO',]
df_MA = df[df$estado == 'MA',]
df_MG = df[df$estado == 'MG',]
df_RJ = df[df$estado == 'RJ',]
df_TO = df[df$estado == 'TO',]

# pega os 5% melhores de cada estado
df_heroes = data.frame()

for(uf in unique(df$estado)){
  df_UF = df[df$estado == uf,]
  df_heroes = rbind(df_heroes, subset(df_UF, df_UF$phft_dif > quantile(df_UF$phft_dif, .95)))
  # df_heroes = rbind(df_heroes, subset(df_UF, df_UF$cgtr_dif < quantile(df_UF$cgtr_dif, .05)))
}

# para facilitar, chamando sempre o "df"
df_base = df
# df = df_base
df_heroes_phft = df_heroes
# df_heroes_cgtr = df_heroes
df = df_heroes

ggplot(df, aes(df$wwr, df$somb, color = df$open_fac))

# plota os casos separado por estado
slices = c("ratio", "height", "area", "azimute", "veneziana", "componente", "absortancia", "vidro", "open_fac", "somb", "wwr")
df$area = as.character(df$area)

for(slice in slices){
  png(filename = paste0(slice,'_phft.png'),
  # png(filename = paste0(slice,'_cgtr.png'), 
      width = 33.8, height = 19, units = "cm", res = 500)  
  plot(
    ggplot(df, aes(df[,slice])) +
    geom_bar() +  
    ggtitle(paste('PHft',slice)) +
    # ggtitle(paste('CgTr',slice)) +
    theme(axis.text.x = element_text(angle=90)) +
    facet_grid(.~estado)
  )
  dev.off()
}
#### ----

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
