
import datetime
import json
import os
import pandas as pd

import dict_update
import sample_gen
import idf_creator_floor as whole_gen
import singlezone_diss
import runep_subprocess
import output_processing
import other_crack_fac

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
EPW_NAME = [
    'BRA_GO_Itumbiara.867740_INMET.epw','BRA_MG_Uberlandia.867760_INMET.epw','BRA_PR_Curitiba.838420_INMET.epw',
    'BRA_RJ_Duque.de.Caxias-Xerem.868770_INMET.epw','BRA_RS_Santa.Maria.839360_INMET.epw','BRA_SC_Florianopolis.838970_INMET.epw',
    'BRA_MA_Sao.Luis.817150_INMET.epw','BRA_TO_Palmas.866070_INMET.epw'
]
SUP_LIMITS = 'sup_limits.csv'
OUTPUT_PROCESSED = 'means_'+FOLDER
SOBOL = False  # True  # 

PARAMETERS = {
    'geometria':[],  # area, ratio, pe-direito, janelas
    'azimute':[],
    'sombreamento':[],
    'veneziana':[],
    'componente':[],  # paredes, piso e coertura
    'absortancia':[],  # paredes e cobertura
    'vidro':[],  # simples/duplo e FS
    'open_fac':[]
}

# Dependents
col_names = list(PARAMETERS)
samples_x_cluster = SIZE/NUM_CLUSTERS
name_length = '{:0'+str(len(str(SIZE)))+'.0f}'
name_length_cluster = '{:0'+str(len(str(NUM_CLUSTERS)))+'.0f}'

def parameter_file(key, i):
    n_files = len(PARAMETERS[key])
    file_name = PARAMETERS[key][int(n_files*i)]

    return file_name

print('\nCREATING DIRECTORIES\n')

os.system('mkdir '+FOLDER)
for i in range(NUM_CLUSTERS):
    os.system('mkdir '+FOLDER+'/cluster'+name_length_cluster.format(i))
    
# Generate sample
print('\nGENERATING SAMPLE\n')

sample = sample_gen.main(SIZE, col_names, SAMPLE_NAME, sobol=SOBOL)
# sample = pd.read_csv(SAMPLE_NAME+'.csv')
if SOBOL:
    sample = (sample+1)/2

# Set cases
print('\nGENERATING MODELS\n')

df = pd.DataFrame(columns=col_names+['folder','file'])
line = 0
for i in range(len(sample)):
    
    sample_line = list(sample.iloc[i])
    
    model_values = dict((param,parameter_file(param, sample.loc[i, param])) for param in col_names)
    
    cluster_n = int(line//samples_x_cluster)
    
    case = name_length.format(line)
    
    output = (FOLDER+'/'+NAME_STDRD+'_{}'.format(case)+'.'+EXTENSION)
    df = df.append(pd.DataFrame([sample_line+['cluster'+name_length_cluster.format(cluster_n),NAME_STDRD+'_{}'.format(case)+'.'+EXTENSION]],columns=col_names+['folder','file']))
    print(output)

    idf_bundler.main([model_values[param] for param in model_values.keys()], output = output)
        
    line += 1

os.chdir(FOLDER)
print('\nRUNNING SIMULATIONS\n')
list_epjson_names = runep_subprocess.gen_list_epjson_names(NUM_CLUSTERS, EXTENSION)
runep_subprocess.main(list_epjson_names, NUM_CLUSTERS, EXTENSION, REMOVE_ALL_BUT, epw_name=EPW_NAME)

print('\nPROCESSING OUTPUT\n')
output_processing.main(df, MONTH_MEANS, OUTPUT_PROCESSED)

end_time = datetime.datetime.now()
total_time = (end_time - start_time)
print("Total processing time: " + str(total_time))
