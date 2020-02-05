import datetime
import glob
import os
import pandas

BASE_FOLDER = ['multi1/','uni1/']

date = datetime.datetime.now().strftime("%d-%m-%y_%H-%M")
OUTPUT_FILE = 'resumo_erros_'+date+'.csv'

errors_dict = {
    'folder':[],
    'file':[],
    'epw':[],
    'WarningCompleted': [],
    'SevereCompleted': [],
    'WarningWarmup':[],
    'SevereWarmup': [],
    'WarningSizing':[],
    'SevereSizing': []
}

for folder in BASE_FOLDER:

    epws = glob.glob(folder+'BRA_*')
    
    for epw in epws:

        files = glob.glob(epw+'/*.err')

        for f in files:
            
            errors_dict["folder"].append(folder)
            errors_dict["epw"].append(epw)
            
            if f != ('sqlite.err'):
                file_name = f
                fatal = True
                print(f, end='\r')
                errors_dict["file"].append(f)
                f = open(f, 'r').readlines()
                
                for i in f:
                        
                    if "************* EnergyPlus Warmup Error Summary" in i:
                        errors_dict['WarningWarmup'].append(i[i.find(": ")+2:i.find("Warning;")-1]) 
                        errors_dict["SevereWarmup"].append(i[i.find("; ")+2:i.find("Severe")-1])
                    if "************* EnergyPlus Sizing Error Summary" in i:
                        errors_dict["WarningSizing"].append(i[i.find(": ")+2:i.find("Warning;")-1])
                        errors_dict["SevereSizing"].append(i[i.find("; ")+2:i.find("Severe")-1])
                    if "************* EnergyPlus Completed Successfully--" in i:
                        errors_dict["WarningCompleted"].append(i[i.find('-- ')+3:i.find(' Warning;')])
                        errors_dict["SevereCompleted"].append(i[i.find("; ")+2:i.find(" Severe")])
                        fatal = False
                    if "[EPS][thermal_resistance]" in i:
                        eps_error += 1
                        
                if fatal:
                    errors_dict["WarningCompleted"].append('FATAL')
                    errors_dict["SevereCompleted"].append('FATAL')

            
for obj in  errors_dict:
    print(obj, len(errors_dict[obj]))
    
errors_dict = pandas.DataFrame(errors_dict)
errors_dict.to_csv(OUTPUT_FILE, index=False)

