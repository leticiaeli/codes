def idf_bundler(input_files, output_name):
    # Bundles files with different idf objects to create one idf model.
    # input_files - List of files with idf objects.
    # output_name - The name of the resulted idf model.
    
    print(output_name)
    
    for i in range(len(input_files)):
        input_files[i] = open(input_files[i], 'rb')
    
    with open(output_name, 'wb') as model:
        
        for i in range(len(input_files)):
            for line in input_files[i]:
                
                model.write(line)