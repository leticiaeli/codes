# Return EHF from multiple simulation results of Operative Temperature

## BIBLIOTECAS
import json
from multiprocessing import Pool  # possibilita processos multithread
import numpy as np
import os  # possibilita comandos no sistema operacional
import pandas as pd  # facilita trabalhar com dataframes
# from dict_update import update  # atualiza dicionários

OCCUP = ':Schedule Value [](Hourly)'  # ':People Occupant Count [](Hourly)'  #
ZONES = ['SALA','DORM1','DORM2']
INF_LIM = 18

def schedule_name(zone, occup):
    return(zone+occup)
 # 'SCH_OCUPACAO:Schedule Value [](Hourly)'

def name_file(case,pattern,mode,epw):
    # Define o nome do arquivo.

    file_name =  pattern+'_'+case+'_'+mode+'_'+epw+'out.csv'
    # file_name =  mode+'_'+epw+'.csv'
    return(file_name)


def process_outputs(line, sup_lim):
    # Le o output do energyplus para o caso especificado e calcula a
    # temperatura operativa média, temperatura operativa máxima, a
    # média das trocas de ar por hora (ACH), e o EHF.
    # Inputs:
    # line = a linha do dataframe que especifica o caso avaliado.
    # sup_lim = limite superior de temperatura para o calculo do PHFT
    # Output:
    # df_temp = dicionario com todas as informacoes desejadas
    
    # dicioniario (dataframe) criado para adicinar as informacoes
    df_temp = {
        # 'folder': [],
        'case': [],
        # 'file_pattern': [],
        # 'floor': [],
        'zone': [],
        'epw': [],
        'ph_inf': [],
        'phft': [],
        'ph_sup': [],
        't_min': [],
        't_max': [],
        'cgtr_cooling': [],
        'cgtr_heating': []
    }
        
    # printa o nome do arquivo para podermos acompanhar o processo
    print(line['case'],' ',line['folder'])  # , end='\r')
    
    # define o nome do output do energyplus a partir do nome do idf
    vn_csv_file = name_file('{:03.0f}'.format(line['case']),line['file_pattern'],'vn',line['epw'])
    ac_csv_file = name_file('{:03.0f}'.format(line['case']),line['file_pattern'],'ac',line['epw'])
    
    # le o output como um dataframe, utilizando o pandas
    df_vn = pd.read_csv(line['folder']+'/'+vn_csv_file)
    df_ac = pd.read_csv(line['folder']+'/'+ac_csv_file)
            
    for zn in ZONES:

        if 'SALA' in zn:
            zn_occup = schedule_name('SALA',OCCUP)
        elif 'DORM' in zn:
            zn_occup = schedule_name('DORM',OCCUP)

        # df_temp['folder'].append(line['folder'])
        df_temp['case'].append(line['case'])
        # df_temp['floor'].append(line['floor'])
        df_temp['zone'].append(zn) 
        df_temp['epw'].append(line['epw'])

        df_temp['t_min'].append((df_vn[zn+':Zone Operative Temperature [C](Hourly)'][df_vn[zn_occup] > 0]).min())
        df_temp['t_max'].append((df_vn[zn+':Zone Operative Temperature [C](Hourly)'][df_vn[zn_occup] > 0]).max())

        df_vn['inf_lim'] = 0
        df_vn.loc[df_vn[zn+':Zone Operative Temperature [C](Hourly)'] < INF_LIM, 'inf_lim'] = 1
        df_temp['ph_inf'].append(df_vn['inf_lim'][df_vn[zn_occup] > 0].mean())

        df_vn['sup_lim'] = 0
        df_vn.loc[df_vn[zn+':Zone Operative Temperature [C](Hourly)'] >= sup_lim, 'sup_lim'] = 1
        df_temp['ph_sup'].append(df_vn['sup_lim'][df_vn[zn_occup] > 0].mean())
        print(sum(df_vn['sup_lim'][df_vn[zn_occup] > 0]))

        df_temp['phft'].append(1 - df_temp['ph_inf'][-1] - df_temp['ph_sup'][-1])


        df_temp['cgtr_cooling'].append(df_ac[zn+' IDEAL LOADS AIR SYSTEM:Zone Ideal Loads Zone Total Cooling Energy [J](Hourly)'][df_vn['sup_lim'] > 0].sum())
        df_temp['cgtr_heating'].append(df_ac[zn+' IDEAL LOADS AIR SYSTEM:Zone Ideal Loads Zone Total Heating Energy [J](Hourly)'][df_vn['sup_lim'] > 0].sum())
    
    return(df_temp)

def main(df_base, sup_limits, output_name):
    # Manda calcular os outputs desejados para cada caso do dataframe,
    # utilizando processos multiplos (multithread)
    # Inputs:
    # df_base = dataframe com as informações de todos os casos.
    # sup_lim = nome do arquivo com os limites superiores do PHFT.
    # output_name = nome com que o dataframe gerada sera salvo.
    
    # dicioniario (dataframe) criado para adicinar as informacoes
    df_final = {
        # 'folder': [],
        'case': [],
        # 'file_pattern': [],
        # 'floor': [],
        'zone': [],
        'epw': [],
        'ph_inf': [],
        'phft': [],
        'ph_sup': [],
        't_min': [],
        't_max': [],
        'cgtr_cooling': [],
        'cgtr_heating': []
    }
    
    # Month means ja foi calculado e eh lido como um dataframe, utilizando pandas (neste caso o clima eh sempre o mesmo)
    with open(sup_limits, 'r') as file:            
        sup_limits = json.loads(file.read())

    # o numero de clusters eh defido a partir do numero de pastas (nao precisa ser assim)
    num_cluster = len(df_base['folder'].unique())
    
    p = Pool(num_cluster)  # abre os multi processos

    # manda rodar a funcao process_outputs para os multiprocessos
    result_map = p.starmap(process_outputs, zip(
        # [df_base.query('folder == "cluster'+str(i)+'"') for i in range(num_cluster)],
        [df_base.iloc[i] for i in range(len(df_base))],
        [sup_limits[df_base['epw'][i]] for i in range(len(df_base))]
    ))
    p.close()
    p.join()

    # passa os resultados dos multi processos para o df_final
    for df_temp in result_map:
        for key in df_final.keys():
            for i in range(len(df_temp[key])):
                df_final[key].append(df_temp[key][i])
    
    # salva o df_final como csv
    df_output = pd.DataFrame(df_final)
    df_output.to_csv(output_name+'.csv', index=False)
    print('\tDone processing!')

df_base = pd.read_csv('df_base.csv')
main(df_base, 'sup_limits.csv', 'multi_outputs')
'''
phft = np.mean((l <26)*l/l)

Teste da funcao sem depender de outros codigos:

os.chdir('teste_outputprocess')
'''
