library(ggplot2)

setwd('~/codes')
#### ----
# df_uni1 = read.csv('uni1/outputs_uni1_03-02-20_13-44_final.csv')
# df_uni2 = read.csv('uni2/outputs_uni2_31-01-20_18-45_final.csv')
# df_uni3 = read.csv('uni3/outputs_uni3_31-01-20_18-46_final.csv')
# 
# df_multi1 = read.csv('multi1/outputs_multi1_03-02-20_13-45_final.csv')
# df_multi2 = read.csv('multi2/outputs_multi2_31-01-20_18-45_final.csv')
# df_multi3 = read.csv('multi3/outputs_multi3_31-01-20_18-45_final.csv')
# df_multi4 = read.csv('outputs_multi4_03-02-20_16-06_final.csv')
# df_multi5 = read.csv('outputs_multi5_03-02-20_16-05_final.csv')
# df_multi6 = read.csv('outputs_multi6_03-02-20_16-04_final.csv')
# df_multi7 = read.csv('outputs_multi7_03-02-20_16-03_final.csv')
# 
# df_ref_uni = read.csv('refs_uni/outputs_refs_uni_06-02-20_15-47.csv')
# df_ref_multi = read.csv('refs_multi/outputs_refs_multi_07-02-20_09-34.csv')
# 
# df_uni = rbind(df_uni1,df_uni2,df_uni3)
# df_multi = rbind(df_multi1,df_multi2,df_multi3,df_multi4,df_multi5,df_multi6,df_multi7)
# 
# write.csv(df_multi, 'outputs_multi.csv', row.names = FALSE)
# write.csv(df_uni, 'outputs_uni.csv', row.names = FALSE)
#### ----

df_uni = read.csv('outputs_uni.csv')
df_multi = read.csv('outputs_multi.csv')
df_ref_uni = read.csv('refs_uni/outputs_refs_uni_06-02-20_15-47.csv')
df_ref_multi = read.csv('refs_multi/outputs_refs_multi_07-02-20_09-34.csv')

df_ref_uni$geometria = substr(df_ref_uni$geometria,12,29)
df_ref_uni$azimute = substr(df_ref_uni$azimute,8,23)

df_ref_multi$geometria = substr(df_ref_multi$geometria,14,31)
df_ref_multi$azimute = substr(df_ref_multi$azimute,8,23)

# unique(df_ref_uni$geometria)
# unique(df_uni$geometria)

# df = df_multi
# df_ref = df_ref_multi

df = df_uni
df_ref = df_ref_uni

df$ph_inf_ref = NA
df$ph_sup_ref = NA
df$phft_ref = NA
df$t_min_ref = NA
df$t_max_ref = NA
df$cgtr_cooling_ref = NA
df$cgtr_heating_ref = NA

# for(line in 1:nrow(df)){
#   df$ph_inf_ref[line] = df_ref$ph_inf[df_ref$epw == df$epw[line] & df_ref$zone == df$zone[line] &
#                                           df_ref$geometria == df$geometria[line] & df_ref$azimute == df$azimute[line]][1]
#   df$ph_sup_ref[line] = df_ref$ph_sup[df_ref$epw == df$epw[line] & df_ref$zone == df$zone[line] &
#                                           df_ref$geometria == df$geometria[line] & df_ref$azimute == df$azimute[line]][1]
#   df$phft_ref[line] = df_ref$phft[df_ref$epw == df$epw[line] & df_ref$zone == df$zone[line] &
#                                           df_ref$geometria == df$geometria[line] & df_ref$azimute == df$azimute[line]][1]
#   df$t_min_ref[line] = df_ref$t_min[df_ref$epw == df$epw[line] & df_ref$zone == df$zone[line] &
#                                           df_ref$geometria == df$geometria[line] & df_ref$azimute == df$azimute[line]][1]
#   df$t_max_ref[line] = df_ref$t_max[df_ref$epw == df$epw[line] & df_ref$zone == df$zone[line] &
#                                           df_ref$geometria == df$geometria[line] & df_ref$azimute == df$azimute[line]][1]
#   df$cgtr_cooling_ref[line] = df_ref$cgtr_cooling[df_ref$epw == df$epw[line] & df_ref$zone == df$zone[line] &
#                                           df_ref$geometria == df$geometria[line] & df_ref$azimute == df$azimute[line]][1]
#   df$cgtr_heating_ref[line] = df_ref$cgtr_heating[df_ref$epw == df$epw[line] & df_ref$zone == df$zone[line] &
#                                           df_ref$geometria == df$geometria[line] & df_ref$azimute == df$azimute[line]][1]
# }

for(line in 1:nrow(df_ref)){
  df$ph_inf_ref[
    df$epw == df_ref$epw[line] & df$zone == df_ref$zone[line] & 
      df$geometria == df_ref$geometria[line] & df$azimute == df_ref$azimute[line]
    ] = df_ref$ph_inf[line]
  
  df$ph_sup_ref[
    df$epw == df_ref$epw[line] & df$zone == df_ref$zone[line] & 
      df$geometria == df_ref$geometria[line] & df$azimute == df_ref$azimute[line]
    ] = df_ref$ph_sup[line]
  
  df$phft_ref[
    df$epw == df_ref$epw[line] & df$zone == df_ref$zone[line] & 
      df$geometria == df_ref$geometria[line] & df$azimute == df_ref$azimute[line]
    ] = df_ref$phft[line]
  
  df$t_min_ref[
    df$epw == df_ref$epw[line] & df$zone == df_ref$zone[line] & 
      df$geometria == df_ref$geometria[line] & df$azimute == df_ref$azimute[line]
    ] = df_ref$t_min[line]
  
  df$t_max_ref[
    df$epw == df_ref$epw[line] & df$zone == df_ref$zone[line] & 
      df$geometria == df_ref$geometria[line] & df$azimute == df_ref$azimute[line]
    ] = df_ref$t_max[line]
  
  df$cgtr_cooling_ref[
    df$epw == df_ref$epw[line] & df$zone == df_ref$zone[line] & 
      df$geometria == df_ref$geometria[line] & df$azimute == df_ref$azimute[line]
    ] = df_ref$cgtr_cooling[line]
  df$cgtr_heating_ref[
    df$epw == df_ref$epw[line] & df$zone == df_ref$zone[line] & 
      df$geometria == df_ref$geometria[line] & df$azimute == df_ref$azimute[line]
    ] = df_ref$cgtr_heating[line]
}

df$ph_inf_ref[
  df$epw == df_ref$epw & df$zone == df_ref$zone & 
    df$geometria == df_ref$geometria & df$azimute == df_ref$azimute
  ] = df_ref$ph_inf[
    df$epw == df_ref$epw & df$zone == df_ref$zone &
      df$geometria == df_ref$geometria & df$azimute == df_ref$azimute
    ]

df$ph_inf_ref[
  df_ref$epw == df$epw & df_ref$zone == df$zone & 
    df_ref$geometria == df$geometria & df_ref$azimute == df$azimute
  ] = df_ref$ph_inf[
    df_ref$epw == df$epw & df_ref$zone == df$zone &
      df_ref$geometria == df$geometria & df_ref$azimute == df$azimute
    ]

# write.csv(df, 'dados_uni.csv')
write.csv(df, 'dados_multi.csv')

df_plot = subset(df, grepl('_SC_',df$epw) & grepl('DORM',df$zone))

phft_diff = df_plot$phft - df_plot$phft_ref

ggplot(df_plot, aes(df_plot$phft_ref)) +
  geom_histogram(binwidth = .05)

ggplot(df_plot, aes(df_plot$phft)) +
  geom_histogram(binwidth = .05)

ggplot(df_plot, aes(phft_diff)) +
  geom_histogram(binwidth = .05)
