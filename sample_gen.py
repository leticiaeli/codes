import pandas as pd
from pyDOE import lhs
from SALib.sample import saltelli

def n_calc(d, n_cases, scnd_order = False):
    # N calculator
    
    if scnd_order:
        n_size = n_cases/(2*d + 2)
    else:
        n_size = n_cases/(d + 2)

    print('N = ',n_size)

    return int(n_size)

def main(size, col_names, output_name, sobol=False, scnd_order=True):
    
    if sobol:

        BOUNDS = [-1, 1]
    
        problem = {
            'num_vars': len(col_names),
            'names': col_names,
            'bounds': [BOUNDS for x in range(len(col_names))]
        }
        
        n_size = n_calc(problem['num_vars'], size, scnd_order=scnd_order)        
        sample_matrix = saltelli.sample(problem, n_size, calc_second_order=scnd_order)
    
    else:

        sample_matrix = lhs(len(col_names),size)
    
    df = pd.DataFrame(sample_matrix, columns=col_names)
    df.to_csv(output_name+".csv", index=False)
    
    return df
