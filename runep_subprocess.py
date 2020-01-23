import glob
import subprocess
import os
import time

def gen_folders_clusters(num_clusters):

    ### creates folders
    name_length_cluster = '{:0'+str(len(str(num_clusters)))+'.0f}'
    for cluster in range(num_clusters):

        folder_name = 'cluster'+name_length_cluster.format(cluster)

        if os.path.isdir(folder_name):
            pass

        else:
            os.mkdir(folder_name)
            
def gen_list_epjson_names(num_clusters, extension='epJSON'):
    
    ### creates the list of files
    list_epjson_names = []
    name_length_cluster = '{:0'+str(len(str(num_clusters)))+'.0f}'
    
    for cluster in range(num_clusters):
        folder_name = 'cluster'+name_length_cluster.format(cluster)
        os.chdir(folder_name)
        # list_epjson_names = list_epjson_names + glob.glob(folder_name+'/*.'+extension)
        list_epjson_names.append(sorted(glob.glob('*.'+extension)))   # list_epjson_names.append(glob.glob(folder_name+'/*.'+extension)) 
        os.chdir('..')
    return list_epjson_names

### execucao dos clusters
def simulate(epjson_name, cluster, extension='epJSON', version_EnergyPlus='energyplus-8.9.0', epw_name='~/equipe-r/arquivos_climaticos/SP.epw',num_clusters=10):

    name_length_cluster = '{:0'+str(len(str(num_clusters)))+'.0f}'
    folder_name = 'cluster'+name_length_cluster.format(cluster)
    
    stringcluster = version_EnergyPlus + ' -w ' + epw_name + ' -p ' + epjson_name.split('.'+extension)[0] + ' -r ' + epjson_name
    # print(stringcluster)

    os.chdir(folder_name)
    processing = subprocess.Popen(stringcluster, stdout = open(os.devnull, 'w'), stderr = subprocess.STDOUT, shell=True)
    os.chdir('..')

    return [processing, cluster, epjson_name]

### remove os arquivos desnecessarios
def remove_rest(epjson_name, cluster,remove_all_but,num_clusters=10):
        
    name_length_cluster = '{:0'+str(len(str(num_clusters)))+'.0f}'
    folder_name = 'cluster'+name_length_cluster.format(cluster)
    os.chdir(folder_name)
    internal_list = glob.glob(epjson_name.split('.')[0]+"*")
    
    for file_name in internal_list:
        if file_name.split('.')[-1] not in remove_all_but:
            os.remove(file_name)
            
    os.chdir('..')


def main(list_epjson_names, num_clusters,extension = 'epJSON',remove_all_but = ['.epJSON', '.csv'], epw_name='~/equipe-r/arquivos_climaticos/SP.epw'):

    list_epjson_names = gen_list_epjson_names(num_clusters)

    check_execute = [0 for i in range(num_clusters)]
    check_available_clusters = num_clusters
    
    list_execute = []
    
    # for _ in range(len(list_epjson_names[0])):
    while sum([len(i) for i in list_epjson_names]) > 0:
        
        if 0 < check_available_clusters <= num_clusters:

            cluster_n = check_execute.index(0)
            if len(list_epjson_names[cluster_n]) == 0:
                check_execute[cluster_n] = 1 
                check_available_clusters -= 1
            else:
                epjson_name = list_epjson_names[cluster_n].pop(0)

                processing = simulate(epjson_name, cluster_n, epw_name=epw_name,num_clusters=num_clusters)
                list_execute.append(processing)

                check_available_clusters -= 1
                check_execute[cluster_n] = 1  # [check_execute.index(0)] = 1

                print(f'MODEL: {epjson_name} \t EPW: {epw_name} \t CLUSTER: {cluster_n}')

        if check_available_clusters == 0:
            
            for i, simulation in enumerate(list_execute):
                if simulation[0].poll() == 0:
                    check_available_clusters += 1
                    check_execute[simulation[1]] = 0
                    remove_rest(list_execute[i][2],list_execute[i][1],remove_all_but,num_clusters)
                    del list_execute[i]

        if sum([len(i) for i in list_epjson_names]) <= num_clusters:
            
            for i in range(len(list_execute)):
                list_execute[i][0].wait()
                remove_rest(list_execute[i][2],list_execute[i][1],remove_all_but,num_clusters)
        
        time.sleep(.1)
        # print(sum([len(i) for i in list_epjson_names]))
