# library
library(ggplot2)
library(ggExtra)
library(gridExtra)

#Acessa a pasta do csv
# setwd("C:/Users/LabEEE_4-8/Documents/NBR_2020/variacao_areas")

## Acessa o csv

# a <- read.csv("variacao.csv")
a = df_vn

a$area_app = NA
a$area_app[a$APP == 'sala'] = 18.96 * a$x[a$APP == 'sala'] * a$y[a$APP == 'sala'] * a$area_fac[a$APP == 'sala']
a$area_app[a$APP == 'dorm1'] = 8.85 * a$x[a$APP == 'dorm1'] * a$y[a$APP == 'dorm1'] * a$area_fac[a$APP == 'dorm1']
a$area_app[a$APP == 'dorm2'] = 8.3 * a$x[a$APP == 'dorm2'] * a$y[a$APP == 'dorm2'] * a$area_fac[a$APP == 'dorm2']

a$CgTr_m = a$CgTr/(3600000*a$area_app)

a$xy = NA
a$xy[a$APP == 'sala'] = (a$x[a$APP == 'sala']*3.87)/(a$y[a$APP == 'sala']*4.9)
a$xy[a$APP == 'dorm1'] = (a$x[a$APP == 'dorm1']*2.75)/(a$y[a$APP == 'dorm1']*3.2)
a$xy[a$APP == 'dorm2'] = (a$x[a$APP == 'dorm2']*2.75)/(a$y[a$APP == 'dorm2']*3)

climas = unique(a$epw)
apps = unique(a$APP)

for(clima in climas){
  for(app in apps){
    df_plot = subset(a, a$APP == app & a$epw == clima)
    
    cgtr = ggplot(df_plot,aes(df_plot$area_app,df_plot$CgTr_m, color= df_plot$xy, shape = as.factor(df_plot$z))) +
      geom_point() +
      ggtitle(paste(clima,app,'CgTr'))
    
    phft = ggplot(df_plot,aes(df_plot$area_app,df_plot$PHFT, color= df_plot$xy, shape = as.factor(df_plot$z))) +
      geom_point() +
      ggtitle(paste(clima,app,'PHFT'))
    show(cgtr)
    show(phft)
  }
}

# grafico basicao CgTr ----

graf_areas_gen <- ggplot(a, aes(x=a$area_app,y=a$CgTr_m,color=factor(a$APP))) + 
  geom_point(alpha=1/2) + 
  labs(colour = "APP") +
  xlab("Area") +
  ylab("CT (kWh/m?)")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior

graf_areas_gen <- ggplot(a, aes(x=a$area_app,y=a$CgTr_m,color=factor(a$epw))) + 
  geom_point(alpha=1/2) +
  labs(colour = "EPW") +
  xlab("Area") +
  ylab("CT (kWh/m?)")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior

# grafico basicao PHFT

graf_areas_gen <- ggplot(a, aes(x=a$area_app,y=a$PHFT,color=factor(a$APP))) + 
  geom_point(alpha=1/2) +
  labs(colour = "APP") +
  xlab("Area") +
  ylab("PHFT")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior

graf_areas_gen <- ggplot(a, aes(x=a$area_app,y=a$PHFT,color=factor(a$epw))) + 
  geom_point(alpha=1/2) + 
  labs(colour = "EPW") +
  xlab("Area") +
  ylab("PHFT")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior

# grafico basicao PHFT X CgTr

graf_areas_gen <- ggplot(a, aes(x=a$CgTr_m,y=a$PHFT,color=factor(a$epw))) + 
  geom_point(alpha=1/2) + 
  labs(colour = "EPW") +
  xlab("CgTr") +
  ylab("PHFT")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior

graf_areas_gen <- ggplot(a, aes(x=a$CgTr_m,y=a$PHFT,color=factor(a$APP))) + 
  geom_point(alpha=1/2) + 
  labs(colour = "APP") +
  xlab("CgTr") +
  ylab("PHFT")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior

graf_areas_gen <- ggplot(a, aes(x=a$CgTr_m,y=a$PHFT,color=factor(a$area_app))) + 
  geom_point(alpha=1/2) + 
  labs(colour = "Area") +
  xlab("CgTr") +
  ylab("PHFT")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior



####### alongamentos x y e z  vs area  ----

# grafico por alongamento X PHFT

graf_areas_gen <- ggplot(a, aes(x=a$area_app,y=a$PHFT,color=factor(a$x))) + 
  geom_point(alpha=1/2) + 
  labs(colour = "x") +
  xlab("Area") +
  ylab("PHFT")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior

# grafico por alongamento X CgTr_m

graf_areas_gen <- ggplot(a, aes(x=a$area_app,y=a$CgTr_m,color=factor(a$x))) + 
  geom_point(alpha=1/2) +
  labs(colour = "x") +
  xlab("Area") +
  ylab("CgTr(kWh/m?)")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior

# grafico por alongamento y PHFT

graf_areas_gen <- ggplot(a, aes(x=a$area_app,y=a$PHFT,color=factor(a$y))) + 
  geom_point(alpha=1/2) +
  labs(colour = "y") +
  xlab("Area") +
  ylab("PHFT")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior

# grafico por alongamento y CgTr_m

graf_areas_gen <- ggplot(a, aes(x=a$area_app,y=a$CgTr_m,color=factor(a$y))) + 
  geom_point(alpha=1/2) + 
  xlab("Area") +
  ylab("CgTr(kWh/m?)")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior


# grafico por alfa PHFT

graf_areas_gen <- ggplot(a, aes(x=a$area_app,y=a$PHFT,color=factor(a$area_fac))) + 
  geom_point(alpha=1/2) +
  labs(colour = "alfa") +
  xlab("Area") +
  ylab("PHFT")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior

# grafico por fator alfa CgTr_m

graf_areas_gen <- ggplot(a, aes(x=a$area_app,y=a$CgTr_m,color=factor(a$area_fac))) + 
  geom_point(alpha=1/2) + 
  labs(colour = "alfa") +
  xlab("Area") +
  ylab("CgTr(kWh/m?)")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior

# grafico por alteracao total da area PHFT

a$tot = a$y*a$x*a$area_fac
graf_areas_gen <- ggplot(a, aes(x=a$area_app,y=a$PHFT,color=factor(a$tot))) + 
  geom_point(alpha=1/2) + 
  labs(colour = "alfa*x*y") +
  xlab("Area") +
  ylab("CgTr(kWh/m?)")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior


# grafico por alteracao total da area CgTr_m

a$tot = a$y*a$x*a$area_fac
graf_areas_gen <- ggplot(a, aes(x=a$area_app,y=a$CgTr_m,color=factor(a$tot))) + 
  geom_point(alpha=1/2) + 
  labs(colour = "alfa*x*y") +
  xlab("Area") +
  ylab("CgTr(kWh/m?)")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior




##### FAZENDO POR EPW CgTr ----

GO = subset(a,subset = a[,8] == "GO")
MA = subset(a,subset = a[,8] == "MA")
MG = subset(a,subset = a[,8] == "MG")
PR = subset(a,subset = a[,8] == "PR")
RJ = subset(a,subset = a[,8] == "RJ")
RS = subset(a,subset = a[,8] == "RS")
SC = subset(a,subset = a[,8] == "SC")
TO = subset(a,subset = a[,8] == "TO")

df_plot = subset(a, a$epw == clima)
df_plot = subset(df_plot, df_plot$APP == app)

ggplot(df_plot,aes(df_plot$area_app,df_plot$CgTr_m, color= df_plot$xy, shape = as.factor(df_plot$z))) +
  geom_point() +
  ggtitle(paste(clima,app,'CgTr'))

ggplot(df_plot,aes(df_plot$area_app,df_plot$PHFT, color= df_plot$xy, shape = as.factor(df_plot$z))) +
  geom_point() +
  ggtitle(paste(clima,app,'PHFT'))

graf_areas_gen <- ggplot(GO, aes(x=GO$area_app,y=GO$CgTr_m,color=factor(GO$APP))) + 
  geom_point(alpha=1/2) + 
  labs(colour = "APP") +
  xlab("Area") +
  ylab("GO - CT (kWh/m?)")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior

graf_areas_gen <- ggplot(MA, aes(x=MA$area_app,y=MA$CgTr_m,color=factor(MA$APP))) + 
  geom_point(alpha=1/2) + 
  labs(colour = "APP") +
  xlab("Area") +
  ylab("MA - CT (kWh/m?)")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior

graf_areas_gen <- ggplot(MG, aes(x=MG$area_app,y=MG$CgTr_m,color=factor(MG$APP))) + 
  geom_point(alpha=1/2) + 
  labs(colour = "APP") +
  xlab("Area") +
  ylab("MG - CT (kWh/m?)")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior

graf_areas_gen <- ggplot(PR, aes(x=PR$area_app,y=PR$CgTr_m,color=factor(PR$APP))) + 
  geom_point(alpha=1/2) + 
  labs(colour = "APP") +
  xlab("Area") +
  ylab("PR - CT (kWh/m?)")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior

graf_areas_gen <- ggplot(RJ, aes(x=RJ$area_app,y=RJ$CgTr_m,color=factor(RJ$APP))) + 
  geom_point(alpha=1/2) + 
  labs(colour = "APP") +
  xlab("Area") +
  ylab("RJ - CT (kWh/m?)")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior

graf_areas_gen <- ggplot(RS, aes(x=RS$area_app,y=RS$CgTr_m,color=factor(RS$APP))) + 
  geom_point(alpha=1/2) + 
  labs(colour = "APP") +
  xlab("Area") +
  ylab("RS - CT (kWh/m?)")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior

graf_areas_gen <- ggplot(SC, aes(x=SC$area_app,y=SC$CgTr_m,color=factor(SC$APP))) + 
  geom_point(alpha=1/2) + 
  labs(colour = "APP") +
  xlab("Area") +
  ylab("SC - CT (kWh/m?)")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior

graf_areas_gen <- ggplot(TO, aes(x=TO$area_app,y=TO$CgTr_m,color=factor(TO$APP))) + 
  geom_point(alpha=1/2) + 
  labs(colour = "APP") +
  xlab("Area") +
  ylab("TO - CT (kWh/m?)")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior

#### CONCLUSAO DESSES PRIMEIROS POR APP: POSSUEM O MESMO COMPORTAMENTO PARA TODOS OS ARQUIVOS CLIMATICOS
#### E O MOTIVO PRA ELE DAR EXATAMENTE DUAS CURVAS PARA CADA APP ? O Z, CONFORME SEGUE ABAIXO ... 
#### SO O Z QUE CRIOU ESSA TENDENCIA TAO BEM DEFINIDA COMO DEMONSTRADO ABAIXO !


graf_areas_gen <- ggplot(GO, aes(x=GO$area_app,y=GO$CgTr_m,color=factor(GO$z))) + 
  geom_point(alpha=1/2) + 
  labs(colour = "APP") +
  xlab("Area") +
  ylab("GO - CT (kWh/m?)")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior


graf_areas_gen <- ggplot(GO, aes(x=GO$area_app,y=GO$CgTr_m,color=factor(GO$x))) + 
  geom_point(alpha=1/2) + 
  labs(colour = "APP") +
  xlab("Area") +
  ylab("GO - CT (kWh/m?)")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior


graf_areas_gen <- ggplot(GO, aes(x=GO$area_app,y=GO$CgTr_m,color=factor(GO$y))) + 
  geom_point(alpha=1/2) + 
  labs(colour = "APP") +
  xlab("Area") +
  ylab("GO - CT (kWh/m?)")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior


graf_areas_gen <- ggplot(GO, aes(x=GO$area_app,y=GO$CgTr_m,color=factor(GO$tot))) + 
  geom_point(alpha=1/2) + 
  labs(colour = "APP") +
  xlab("Area") +
  ylab("GO - CT (kWh/m?)")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior


#### FAZENDO A PARTIR DO VOLUME:

#Acessa a pasta do csv

setwd("C:/Users/LabEEE_4-8/Documents/NBR_2020/variacao_areas")

## Acessa o csv

a <- read.csv("variacao_v.csv")
a$area_fac = a$area_fac*a$area_fac

# library
library(ggplot2)
library(ggExtra)
library(gridExtra)


# grafico basicao CgTr

graf_areas_gen <- ggplot(a, aes(x=a$vol_app,y=a$CgTr_v,color=factor(a$APP))) + 
  geom_point(alpha=1/2) + 
  labs(colour = "APP") +
  xlab("Volume") +
  ylab("CT (kWh/m?)")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior

graf_areas_gen <- ggplot(a, aes(x=a$vol_app,y=a$CgTr_v,color=factor(a$epw))) + 
  geom_point(alpha=1/2) +
  labs(colour = "EPW") +
  xlab("Volume") +
  ylab("CT (kWh/m?)")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior

# grafico basicao PHFT

graf_areas_gen <- ggplot(a, aes(x=a$vol_app,y=a$PHFT,color=factor(a$APP))) + 
  geom_point(alpha=1/2) +
  labs(colour = "APP") +
  xlab("Volume") +
  ylab("PHFT")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior

graf_areas_gen <- ggplot(a, aes(x=a$vol_app,y=a$PHFT,color=factor(a$epw))) + 
  geom_point(alpha=1/2) + 
  labs(colour = "EPW") +
  xlab("Volume") +
  ylab("PHFT")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior

# grafico basicao PHFT X CgTr

graf_areas_gen <- ggplot(a, aes(x=a$CgTr_v,y=a$PHFT,color=factor(a$epw))) + 
  geom_point(alpha=1/2) + 
  labs(colour = "EPW") +
  xlab("CgTr") +
  ylab("PHFT")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior

graf_areas_gen <- ggplot(a, aes(x=a$CgTr_v,y=a$PHFT,color=factor(a$APP))) + 
  geom_point(alpha=1/2) + 
  labs(colour = "APP") +
  xlab("CgTr") +
  ylab("PHFT")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior

graf_areas_gen <- ggplot(a, aes(x=a$CgTr_v,y=a$PHFT,color=factor(a$vol_app))) + 
  geom_point(alpha=1/2) + 
  labs(colour = "Volume") +
  xlab("CgTr") +
  ylab("PHFT")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior



####### alongamentos x y e z  vs area 

# grafico por alongamento X PHFT

graf_areas_gen <- ggplot(a, aes(x=a$vol_app,y=a$PHFT,color=factor(a$x))) + 
  geom_point(alpha=1/2) + 
  labs(colour = "x") +
  xlab("Volume") +
  ylab("PHFT")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior

# grafico por alongamento X CgTr_v

graf_areas_gen <- ggplot(a, aes(x=a$vol_app,y=a$CgTr_v,color=factor(a$x))) + 
  geom_point(alpha=1/2) +
  labs(colour = "x") +
  xlab("Volume") +
  ylab("CgTr(kWh/m?)")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior

# grafico por alongamento y PHFT

graf_areas_gen <- ggplot(a, aes(x=a$vol_app,y=a$PHFT,color=factor(a$y))) + 
  geom_point(alpha=1/2) +
  labs(colour = "y") +
  xlab("Volume") +
  ylab("PHFT")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior

# grafico por alongamento y CgTr_v

graf_areas_gen <- ggplot(a, aes(x=a$vol_app,y=a$CgTr_v,color=factor(a$y))) + 
  geom_point(alpha=1/2) + 
  xlab("Volume") +
  ylab("CgTr(kWh/m?)")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior


# grafico por alfa PHFT

graf_areas_gen <- ggplot(a, aes(x=a$vol_app,y=a$PHFT,color=factor(a$area_fac))) + 
  geom_point(alpha=1/2) +
  labs(colour = "alfa") +
  xlab("Volume") +
  ylab("PHFT")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior

# grafico por fator alfa CgTr_v

graf_areas_gen <- ggplot(a, aes(x=a$vol_app,y=a$CgTr_v,color=factor(a$area_fac))) + 
  geom_point(alpha=1/2) + 
  labs(colour = "alfa") +
  xlab("Volume") +
  ylab("CgTr(kWh/m?)")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior

# grafico por alteracao total da area PHFT

a$tot = a$y*a$x*a$area_fac
graf_areas_gen <- ggplot(a, aes(x=a$vol_app,y=a$PHFT,color=factor(a$tot))) + 
  geom_point(alpha=1/2) + 
  labs(colour = "alfa*x*y") +
  xlab("Volume") +
  ylab("CgTr(kWh/m?)")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior


# grafico por alteracao total da area CgTr_v

a$tot = a$y*a$x*a$area_fac
graf_areas_gen <- ggplot(a, aes(x=a$vol_app,y=a$CgTr_v,color=factor(a$tot))) + 
  geom_point(alpha=1/2) + 
  labs(colour = "alfa*x*y") +
  xlab("Volume") +
  ylab("CgTr(kWh/m?)")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior




##### FAZENDO POR EPW CgTr ----->>> OBJETIVO: VERIFICAR AS CURVAS QUANDO A CARGA FOR POR UN. VOLUME
##### DESFAZER O PERFIL DE CURVAS DUPLAS QUANDO VERIFICOU-SE APENAS A AREA

GO = subset(a,subset = a[,8] == "GO")
MA = subset(a,subset = a[,8] == "MA")
MG = subset(a,subset = a[,8] == "MG")
PR = subset(a,subset = a[,8] == "PR")
RJ = subset(a,subset = a[,8] == "RJ")
RS = subset(a,subset = a[,8] == "RS")
SC = subset(a,subset = a[,8] == "SC")
TO = subset(a,subset = a[,8] == "TO")

graf_areas_gen <- ggplot(GO, aes(x=GO$vol_app,y=GO$CgTr_v,color=factor(GO$APP))) + 
  geom_point(alpha=1/2) + 
  labs(colour = "APP") +
  xlab("Volume") +
  ylab("GO - CT (kWh/m?)")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior

graf_areas_gen <- ggplot(MA, aes(x=MA$vol_app,y=MA$CgTr_v,color=factor(MA$APP))) + 
  geom_point(alpha=1/2) + 
  labs(colour = "APP") +
  xlab("Volume") +
  ylab("MA - CT (kWh/m?)")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior

graf_areas_gen <- ggplot(MG, aes(x=MG$vol_app,y=MG$CgTr_v,color=factor(MG$APP))) + 
  geom_point(alpha=1/2) + 
  labs(colour = "APP") +
  xlab("Volume") +
  ylab("MG - CT (kWh/m?)")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior

graf_areas_gen <- ggplot(PR, aes(x=PR$vol_app,y=PR$CgTr_v,color=factor(PR$APP))) + 
  geom_point(alpha=1/2) + 
  labs(colour = "APP") +
  xlab("Volume") +
  ylab("PR - CT (kWh/m?)")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior

graf_areas_gen <- ggplot(RJ, aes(x=RJ$vol_app,y=RJ$CgTr_v,color=factor(RJ$APP))) + 
  geom_point(alpha=1/2) + 
  labs(colour = "APP") +
  xlab("Volume") +
  ylab("RJ - CT (kWh/m?)")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior

graf_areas_gen <- ggplot(RS, aes(x=RS$vol_app,y=RS$CgTr_v,color=factor(RS$APP))) + 
  geom_point(alpha=1/2) + 
  labs(colour = "APP") +
  xlab("Volume") +
  ylab("RS - CT (kWh/m?)")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior

graf_areas_gen <- ggplot(SC, aes(x=SC$vol_app,y=SC$CgTr_v,color=factor(SC$APP))) + 
  geom_point(alpha=1/2) + 
  labs(colour = "APP") +
  xlab("Volume") +
  ylab("SC - CT (kWh/m?)")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior

graf_areas_gen <- ggplot(TO, aes(x=TO$vol_app,y=TO$CgTr_v,color=factor(TO$APP))) + 
  geom_point(alpha=1/2) + 
  labs(colour = "APP") +
  xlab("Volume") +
  ylab("TO - CT (kWh/m?)")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior

#### CONCLUSAO DESSES PRIMEIROS POR APP: POSSUEM O MESMO COMPORTAMENTO PARA TODOS OS ARQUIVOS CLIMATICOS
#### E O MOTIVO PRA ELE DAR EXATAMENTE DUAS CURVAS PARA CADA APP ? O Z, CONFORME SEGUE ABAIXO ... 
#### SO O Z QUE CRIOU ESSA TENDENCIA TAO BEM DEFINIDA COMO DEMONSTRADO ABAIXO !


graf_areas_gen <- ggplot(GO, aes(x=GO$vol_app,y=GO$CgTr_v,color=factor(GO$z))) + 
  geom_point(alpha=1/2) + 
  labs(colour = "APP") +
  xlab("Volume") +
  ylab("GO - CT (kWh/m?)")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior


graf_areas_gen <- ggplot(GO, aes(x=GO$vol_app,y=GO$CgTr_v,color=factor(GO$x))) + 
  geom_point(alpha=1/2) + 
  labs(colour = "APP") +
  xlab("Volume") +
  ylab("GO - CT (kWh/m?)")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior


graf_areas_gen <- ggplot(GO, aes(x=GO$vol_app,y=GO$CgTr_v,color=factor(GO$y))) + 
  geom_point(alpha=1/2) + 
  labs(colour = "APP") +
  xlab("Volume") +
  ylab("GO - CT (kWh/m?)")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior


graf_areas_gen <- ggplot(GO, aes(x=GO$vol_app,y=GO$CgTr_v,color=factor(GO$tot))) + 
  geom_point(alpha=1/2) + 
  labs(colour = "APP") +
  xlab("Volume") +
  ylab("GO - CT (kWh/m?)")
final_mdcp_inferior <- ggMarginal(graf_areas_gen, type="histogram", margins = c("x"))
graf_areas_gen
final_mdcp_inferior
