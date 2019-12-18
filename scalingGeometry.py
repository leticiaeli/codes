import json

def constant_vertex(vertex, vertex_list, scale):
    # Checks which vertex it is, so it defines the new value,
    # in order to keep the same opening area
    
    if max(vertex_list) == min(vertex_list):
        new_vertex = vertex*scale
    elif vertex == min(vertex_list):
        new_vertex = (scale*(max(vertex_list)+min(vertex_list))-(max(vertex_list)-min(vertex_list)))*.5
    elif vertex == max(vertex_list):
        new_vertex = (scale*(max(vertex_list)+min(vertex_list))+(max(vertex_list)-min(vertex_list)))*.5

    return(new_vertex)

def scaling(scalex=1.55, scaley=1.55,scalez=1.55,
    ratio_of_building_afn=0.85, window_scale=True, shading_scale=False,
    input_file='model.epJSON',output_name='scaled_model.epJSON'):
    # This function multiplies the vertices of the epJSON model by a
    # determined value.
    
    # scalex - Scale factor to be multiplied by the x vertices.
    # scaley - Scale factor to be multiplied by the y vertices.
    # scalez - Scale factor to be multiplied by the z vertices.
    # ratio_of_building_afn - New ratio of building value for AFN.
    # window_scale - Condition to change geometry of windows too.
    # shading_scale - Condition to change geometry of shading too.
    # input_file - The epJSON file to be edited.
    # output_name - The name of the output file to be created.
    
    print(output_name)
    
    # reading epJSON file
    file = open(input_file, "r")
    content = json.load(file)
    file.close()

    # changing epJSON fields
    ## AirflowNetwork:SimulationControl
    for i in list(content["AirflowNetwork:SimulationControl"].keys()):
        content["AirflowNetwork:SimulationControl"][i]["ratio_of_building_width_along_short_axis_to_width_along_long_axis"] =  ratio_of_building_afn

    ## BuildingSurface:Detailed
    for i in list(content["BuildingSurface:Detailed"].keys()):
        for j,k in enumerate(content["BuildingSurface:Detailed"][i]["vertices"]):
            content["BuildingSurface:Detailed"][i]["vertices"][j]["vertex_x_coordinate"] = content["BuildingSurface:Detailed"][i]["vertices"][j]["vertex_x_coordinate"]*scalex
            content["BuildingSurface:Detailed"][i]["vertices"][j]["vertex_y_coordinate"] = content["BuildingSurface:Detailed"][i]["vertices"][j]["vertex_y_coordinate"]*scaley
            content["BuildingSurface:Detailed"][i]["vertices"][j]["vertex_z_coordinate"] = content["BuildingSurface:Detailed"][i]["vertices"][j]["vertex_z_coordinate"]*scalez

    ## FenestrationSurface:Detailed
    if window_scale:
        for i in list(content["FenestrationSurface:Detailed"].keys()):
            
            content["FenestrationSurface:Detailed"][i]["vertex_1_x_coordinate"] = content["FenestrationSurface:Detailed"][i]["vertex_1_x_coordinate"]*scalex
            content["FenestrationSurface:Detailed"][i]["vertex_2_x_coordinate"] = content["FenestrationSurface:Detailed"][i]["vertex_2_x_coordinate"]*scalex
            content["FenestrationSurface:Detailed"][i]["vertex_3_x_coordinate"] = content["FenestrationSurface:Detailed"][i]["vertex_3_x_coordinate"]*scalex
            content["FenestrationSurface:Detailed"][i]["vertex_4_x_coordinate"] = content["FenestrationSurface:Detailed"][i]["vertex_4_x_coordinate"]*scalex
                
            content["FenestrationSurface:Detailed"][i]["vertex_1_y_coordinate"] = content["FenestrationSurface:Detailed"][i]["vertex_1_y_coordinate"]*scaley
            content["FenestrationSurface:Detailed"][i]["vertex_2_y_coordinate"] = content["FenestrationSurface:Detailed"][i]["vertex_2_y_coordinate"]*scaley
            content["FenestrationSurface:Detailed"][i]["vertex_3_y_coordinate"] = content["FenestrationSurface:Detailed"][i]["vertex_3_y_coordinate"]*scaley
            content["FenestrationSurface:Detailed"][i]["vertex_4_y_coordinate"] = content["FenestrationSurface:Detailed"][i]["vertex_4_y_coordinate"]*scaley

            content["FenestrationSurface:Detailed"][i]["vertex_1_z_coordinate"] = content["FenestrationSurface:Detailed"][i]["vertex_1_z_coordinate"]*scalez
            content["FenestrationSurface:Detailed"][i]["vertex_2_z_coordinate"] = content["FenestrationSurface:Detailed"][i]["vertex_2_z_coordinate"]*scalez
            content["FenestrationSurface:Detailed"][i]["vertex_3_z_coordinate"] = content["FenestrationSurface:Detailed"][i]["vertex_3_z_coordinate"]*scalez
            content["FenestrationSurface:Detailed"][i]["vertex_4_z_coordinate"] = content["FenestrationSurface:Detailed"][i]["vertex_4_z_coordinate"]*scalez

    else:
        for i in list(content["FenestrationSurface:Detailed"].keys()):

            x_vertex = []
            y_vertex = []
            z_vertex = []

            for vertex in list(content["FenestrationSurface:Detailed"][i].keys()):

                if '_x_' in vertex:
                    x_vertex.append(content["FenestrationSurface:Detailed"][i][vertex])
                elif '_y_' in vertex:
                    y_vertex.append(content["FenestrationSurface:Detailed"][i][vertex])
                elif '_z_' in vertex:
                    z_vertex.append(content["FenestrationSurface:Detailed"][i][vertex])
            
            content["FenestrationSurface:Detailed"][i]["vertex_1_x_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_1_x_coordinate"],x_vertex,scalex)
            content["FenestrationSurface:Detailed"][i]["vertex_2_x_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_2_x_coordinate"],x_vertex,scalex)
            content["FenestrationSurface:Detailed"][i]["vertex_3_x_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_3_x_coordinate"],x_vertex,scalex)
            content["FenestrationSurface:Detailed"][i]["vertex_4_x_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_4_x_coordinate"],x_vertex,scalex)
                
            content["FenestrationSurface:Detailed"][i]["vertex_1_y_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_1_y_coordinate"],y_vertex,scaley)
            content["FenestrationSurface:Detailed"][i]["vertex_2_y_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_2_y_coordinate"],y_vertex,scaley)
            content["FenestrationSurface:Detailed"][i]["vertex_3_y_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_3_y_coordinate"],y_vertex,scaley)
            content["FenestrationSurface:Detailed"][i]["vertex_4_y_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_4_y_coordinate"],y_vertex,scaley)

            content["FenestrationSurface:Detailed"][i]["vertex_1_z_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_1_z_coordinate"],z_vertex,scalez)
            content["FenestrationSurface:Detailed"][i]["vertex_2_z_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_2_z_coordinate"],z_vertex,scalez)
            content["FenestrationSurface:Detailed"][i]["vertex_3_z_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_3_z_coordinate"],z_vertex,scalez)
            content["FenestrationSurface:Detailed"][i]["vertex_4_z_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_4_z_coordinate"],z_vertex,scalez)


    ## Shading:Building:Detailed
    if shading_scale:
        for i in list(content["Shading:Building:Detailed"].keys()):
            for j,k in enumerate(content["Shading:Building:Detailed"][i]["vertices"]):
                content["Shading:Building:Detailed"][i]["vertices"][j]["vertex_x_coordinate"] = content["Shading:Building:Detailed"][i]["vertices"][j]["vertex_x_coordinate"]*scalex
                content["Shading:Building:Detailed"][i]["vertices"][j]["vertex_y_coordinate"] = content["Shading:Building:Detailed"][i]["vertices"][j]["vertex_y_coordinate"]*scaley
                content["Shading:Building:Detailed"][i]["vertices"][j]["vertex_z_coordinate"] = content["Shading:Building:Detailed"][i]["vertices"][j]["vertex_z_coordinate"]*scalez

    ## Zone
    ## Shading:Building:Detailed
    for i in list(content["Zone"].keys()):
        content["Zone"][i]["x_origin"] = content["Zone"][i]["x_origin"]*scalex
        content["Zone"][i]["y_origin"] = content["Zone"][i]["y_origin"]*scaley
        content["Zone"][i]["z_origin"] = content["Zone"][i]["z_origin"]*scalez

    # writing  epJSON file
    file = open(output_name, "w")
    content = json.dumps(content)
    file.write(content)
    file.close()

## Test function changing values on the following lines: ---------------

# Define the name of the input file here
FILE_NAME = 'singlezone_gen/hive_12-04_floor0_roof0.epJSON'

# Define the input parameters here
scaling(scalex=2, scaley=.5,scalez=1, ratio_of_building_afn=0.85, 
    window_scale=False, shading_scale=False,
    input_file= FILE_NAME, output_name='scaling_test.epJSON')

'''

- abre o idf
- converte pra json
- enumera as zonas
    procurando no objeto "Zone"
- calcula as areas das zonas
    procurando em "BuildingSurface:Detailed", "surface_type": "Floor", e lendo os vertices
- enumera as surfaces de cada zona
    procurando em "BuildingSurface:Detailed", e adicionando a lista das surfaces, pelo "zone_name" (só walls)
- enumera as janelas de cada zona, a partir das surfaces
    para cada zona, lendo "building_surface_name" e "surface_type": "Window" do "FenestrationSurface:Detailed"
- calcula as áreas das janelas
    lendo os vertices das janelas (conferir se varia no x ou y)
- corrige as áreas das janelas
    multiplicando W (ou H) pelo fator "area ref/area real"
    *conferir se W (ou H) não passa da aresta da Wall
    *conferir se a janela não se sobrepoem com a porta
    **definir se vai consertar autmaticamente, ou só avisar
- salva o json
- converte pra idf

'''