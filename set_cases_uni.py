
import datetime
import json
import os
import pandas as pd

import dict_update
from idf_bundler import idf_bundler
import sample_gen
# import idf_creator_floor as whole_gen
# import singlezone_diss
import runep_subprocess
import output_processing
# import other_crack_fac

update = dict_update.update
        
start_time = datetime.datetime.now()

# Globals
FOLDER = 'uni_test'  # 'ann_whole_validation'  # 'ann_whole'  #  
SIZE =  10  # 
SAMPLE_NAME = 'sample_'+FOLDER  # 'sample_ann_whole_validation'  # 'sample_ann_whole'  # 
NUM_CLUSTERS = int(os.cpu_count()/2)
NAME_STDRD = 'U'
EXTENSION = 'idf'
REMOVE_ALL_BUT = [EXTENSION, 'csv', 'err']
EPW_NAMES = [
    'BRA_GO_Itumbiara.867740_INMET.epw','BRA_MG_Uberlandia.867760_INMET.epw','BRA_PR_Curitiba.838420_INMET.epw'
]#,
#     'BRA_RJ_Duque.de.Caxias-Xerem.868770_INMET.epw','BRA_RS_Santa.Maria.839360_INMET.epw','BRA_SC_Florianopolis.838970_INMET.epw',
#     'BRA_MA_Sao.Luis.817150_INMET.epw','BRA_TO_Palmas.866070_INMET.epw'
# ]
SUP_LIMITS = 'sup_limits.csv'
OUTPUT_PROCESSED = 'outputs_'+FOLDER
SOBOL = True  # False  # 

SLICE = 'slices/'
MAIN = ['slices/main_materials_fixed.txt', 'slices/main.txt']
VN_FILE = ['slices/Uni/u_afn.txt']
AC_FILE = ['slices/Uni/u_idealloads.txt']

PARAMETERS = {
    'geometria':[SLICE+'Uni/u_geom_0_0_0.txt'],  # area, ratio, pe-direito, janelas
    'azimute':[SLICE+'rotation_000.txt',SLICE+'rotation_180.txt'],
    'sombreamento':[SLICE+'Uni/u_shade_050_geom_0_0_0.txt',SLICE+'Uni/u_shade_120_geom_0_0_0.txt'],
    'veneziana':[SLICE+'Uni/u_blind_off.txt',SLICE+'Uni/u_blind_on.txt'],
    'componente':[SLICE+'Uni/u_construction_ref.txt',SLICE+'Uni/u_construction_sfiso.txt',SLICE+'Uni/u_construction_tijmacico20.txt',SLICE+'Uni/u_construction_tv.txt'],  # paredes, piso e coertura
    'absortancia':[SLICE+'abs_60.txt',SLICE+'abs_20.txt',SLICE+'abs_80.txt'],  # paredes e cobertura
    'vidro':[SLICE+'vidro_simples.txt']#,  # simples/duplo e FS
    # 'open_fac':[]
}

# Dependents
col_names = list(PARAMETERS)
# samples_x_cluster = SIZE/NUM_CLUSTERS
name_length = '{:0'+str(len(str(SIZE)))+'.0f}'
# name_length_cluster = '{:0'+str(len(str(NUM_CLUSTERS)))+'.0f}'

def parameter_file(key, i):
    n_files = len(PARAMETERS[key])
    file_name = PARAMETERS[key][int(n_files*i)]

    return file_name

print('\nCREATING DIRECTORIES\n')

os.system('mkdir '+FOLDER)
# for i in range(NUM_CLUSTERS):
#     os.system('mkdir '+FOLDER+'/cluster'+name_length_cluster.format(i))
for epw in EPW_NAMES:
    os.system('mkdir '+FOLDER+'/'+epw)
    
# Generate sample
print('\nGENERATING SAMPLE\n')

sample = sample_gen.main(SIZE, col_names, SAMPLE_NAME, sobol=SOBOL, scnd_order = False)
# sample = pd.read_csv(SAMPLE_NAME+'.csv')
if SOBOL:
    sample = (sample+1)/2

# Set cases
print('\nGENERATING MODELS\n')

df = pd.DataFrame(columns=col_names+['case'])  # 'folder',
line = 0
for i in range(len(sample)):
    
    sample_line = list(sample.iloc[i])
    
    model_values = dict((param,parameter_file(param, sample.loc[i, param])) for param in col_names)
    
    case = name_length.format(line)
    
    output = (NAME_STDRD+'_{}'.format(case))
    df = df.append(pd.DataFrame([sample_line+[case]],columns=col_names+['case']))  # 'cluster'+name_length_cluster.format(cluster_n),  # 'folder',
    print(output)

    # AC
    # idf_bundler([model_values[param] for param in model_values.keys()]+MAIN+AC_FILE, output_name = FOLDER+'/'+output+'_ac.'+EXTENSION)
        
    # VN
    # idf_bundler([model_values[param] for param in model_values.keys()]+MAIN+VN_FILE, output_name = FOLDER+'/'+output+'_vn.'+EXTENSION)
        
    line += 1

df_base = pd.DataFrame()
for epw in EPW_NAMES:
    df['epw'] = epw
    df_base = df_base.append(df, ignore_index = True)

os.chdir(FOLDER)
print('\nRUNNING SIMULATIONS\n')
# list_epjson_names = runep_subprocess.gen_list_epjson_names(NUM_CLUSTERS, EXTENSION)
# runep_subprocess.main(NUM_CLUSTERS, EXTENSION, REMOVE_ALL_BUT, epw_names=EPW_NAMES)  # list_epjson_names,

print('\nPROCESSING OUTPUT\n')
output_processing.main(df_base, SUP_LIMITS, OUTPUT_PROCESSED,NUM_CLUSTERS,NAME_STDRD)

end_time = datetime.datetime.now()
total_time = (end_time - start_time)
print("Total processing time: " + str(total_time))
