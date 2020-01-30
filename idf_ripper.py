
def idf_ripper(input_file_name, slices, left='main'):
    # Creates new idf files only with the objects defined on a dictioinary.
    # 
    # INPUTS:
    # input_file_name = Name of the idf model to be ripped.
    # slices = Dictionary with new files to be generated, and the objects included
    # in each generated file

    outputs = {
        left: open(input_file_name.split('.')[0]+'_'+left+'.idf', 'w')
    }
    writeon = left

    input_file = open(input_file_name, 'r')

    for slc in slices.keys():
        outputs[slc] = open(input_file_name.split('.')[0]+'_'+slc+'.idf', 'w')

    for line in input_file:
        for slc in slices.keys():
            for obj in slices[slc]:
                
                if line.startswith(obj):
                    writeon = slc

        outputs[writeon].write(line)
                
        if ';' in line:
            writeon = left

'''
#### EXAMPLE ####

input_file_name = 'teste.idf'

slices = {
    'afn': ['AirflowNetwork:MultiZone:Surface,','AirflowNetwork:SimulationControl,'],
    'building': ['BuildingSurface:Detailed,']
}

idf_ripper(input_file_name, slices)
'''
