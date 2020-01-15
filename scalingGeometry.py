
import json
import os
import numpy as np

# Window to Floor Ratio of the reference
REF_WINDOW_TO_FLOOR_RATIO = .17

# Functions

def polygon_area(p):
    # returns the area of a polygon, given the vertices.

    # p - A list of pairs of vectors, ex: [(x1,y1),(x2,y2),(x3,y3)...]
    return 0.5 * abs(sum(p[i][0]*p[(i+1)%len(p)][1] - p[(i+1)%len(p)][0]*p[i][1]
        for i in range(len(p))))

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

def ref_vertex(vertex, vertex_list, scale,ref_scale):
    # Checks which vertex it is, so it defines the new value,
    # in order to keep the reference opening area

    ref_scale_sqrt = ref_scale**(1/2)
    
    if max(vertex_list) == min(vertex_list):
        new_vertex = vertex*scale
    elif vertex == min(vertex_list):
        new_vertex = (scale*(max(vertex_list)+min(vertex_list))-(ref_scale_sqrt*(max(vertex_list)-min(vertex_list))))*.5
    elif vertex == max(vertex_list):
        new_vertex = (scale*(max(vertex_list)+min(vertex_list))+(ref_scale_sqrt*(max(vertex_list)-min(vertex_list))))*.5

    return(new_vertex)

def scaling(scalex=2, scaley=2,scalez=2, ref=False, window_scale=True, shading_scale=True, input_file='model.epJSON',output_name='scaled_model.epJSON'):

    # This function multiplies the vertices of the EnergyPlus model by a
    # determined value, and returns the scaled model (.idf and .epJSON)
    # scalex - Scale factor to be multiplied by the x vertices.
    # scaley - Scale factor to be multiplied by the y vertices.
    # scalez - Scale factor to be multiplied by the z vertices.
    # ref - Determines the size of windows based on the reference,
    ## and erases shading surfaces.
    # ratio_of_building_afn - New ratio of building value for AFN.
    # window_scale - Condition to change geometry of windows too.
    # shading_scale - Condition to change geometry of shading too.
    # input_file - The epJSON file to be edited.
    # output_name - The name of the output file to be created.
    
    print(output_name)
    
    # converts idf to epJSON, if needed
    if input_file[-3:] == 'idf':
        os.system('energyplus -x -c '+input_file)
        input_file = input_file[:-3]+'epJSON'
		
	# reading epJSON file
    file = open(input_file, "r")
    content = json.load(file)
    file.close()
    
    #### Changing epJSON fields ####
    
    
    for i in list(content['BuildingSurface:Detailed'].keys()):
        
        for j,k in enumerate(content['BuildingSurface:Detailed'][i]['vertices']):

	
    ## Zone
    for i in list(content["Zone"].keys()):
		content["Zone"][i]["x_origin"] = content["Zone"][i]["x_origin"]*scalex
		content["Zone"][i]["y_origin"] = content["Zone"][i]["y_origin"]*scaley
		content["Zone"][i]["z_origin"] = content["Zone"][i]["z_origin"]*scalez

    ## BuildingSurface:Detailed
    
    ##### RV - starts
		# fixes the variable 'ratio_of_building_afn'
    
    # will be used to define building ratio and shading
    x_min = 0
    x_max = 0
    y_min = 0
    y_max = 0
    for i in list(content["BuildingSurface:Detailed"].keys()):
		zone_name = content['BuildingSurface:Detailed'][i]['zone_name']
        x_zone = content['Zone'][zone_name]['x_origin']
        y_zone = content['Zone'][zone_name]['y_origin']
		for j,k in enumerate(content["BuildingSurface:Detailed"][i]["vertices"]):
			# scales the vertices of surfaces
			content["BuildingSurface:Detailed"][i]["vertices"][j]["vertex_x_coordinate"] = content["BuildingSurface:Detailed"][i]["vertices"][j]["vertex_x_coordinate"]*scalex
			content["BuildingSurface:Detailed"][i]["vertices"][j]["vertex_y_coordinate"] = content["BuildingSurface:Detailed"][i]["vertices"][j]["vertex_y_coordinate"]*scaley
			content["BuildingSurface:Detailed"][i]["vertices"][j]["vertex_z_coordinate"] = content["BuildingSurface:Detailed"][i]["vertices"][j]["vertex_z_coordinate"]*scalez

            if (x_zone + content['BuildingSurface:Detailed'][i]['vertices'][j]['vertex_x_coordinate']) < x_min:
                x_min = x_zone + content['BuildingSurface:Detailed'][i]['vertices'][j]['vertex_x_coordinate']
            if (x_zone + content['BuildingSurface:Detailed'][i]['vertices'][j]['vertex_x_coordinate']) > x_max:
                x_max = x_zone + content['BuildingSurface:Detailed'][i]['vertices'][j]['vertex_x_coordinate']
            if (y_zone + content['BuildingSurface:Detailed'][i]['vertices'][j]['vertex_y_coordinate']) < y_min:
                y_min = y_zone + content['BuildingSurface:Detailed'][i]['vertices'][j]['vertex_x_coordinate']
            if (y_zone + content['BuildingSurface:Detailed'][i]['vertices'][j]['vertex_y_coordinate']) > y_max:
                y_max = y_zone + content['BuildingSurface:Detailed'][i]['vertices'][j]['vertex_y_coordinate']

    ## AirflowNetwork:SimulationControl
    dif_x = (x_max - x_min)*scalex
    dif_y = (y_max - y_min)*scaley
    ratio_of_building_afn = min(dif_x, dif_y)/max(dif_x, dif_y)
	
	##### RV - ends
	
    if 'AirflowNetwork:SimulationControl' in list(content.keys()):
		for i in list(content['AirflowNetwork:SimulationControl'].keys()):
			content['AirflowNetwork:SimulationControl'][i]['ratio_of_building_width_along_short_axis_to_width_along_long_axis'] =  ratio_of_building_afn

    # Defines opening areas according to reference
    if ref:

        # erase shading devices
        if 'Shading:Building:Detailed' in list(content.keys()):
            del(content['Shading:Building:Detailed'])

        # list zones on a dict
        zones = {}
        for i in list(content["Zone"].keys()):
            zones[i] = {}
            zones[i]['surfaces'] = []
            zones[i]['fenestrations'] = {}
            
        for surface in content["BuildingSurface:Detailed"].keys():
            
            # adds the area of the zones
            if content["BuildingSurface:Detailed"][surface]['surface_type'] == 'Floor':

                # creates the input list for the polygon area function
                floor_vertices = []
                for j,k in enumerate(content["BuildingSurface:Detailed"][surface]["vertices"]):
                    floor_vertices.append((
                        content["BuildingSurface:Detailed"][surface]["vertices"][j]["vertex_x_coordinate"],
                        content["BuildingSurface:Detailed"][surface]["vertices"][j]["vertex_y_coordinate"]
                    ))

                zone_area = polygon_area(floor_vertices)
                zone = content["BuildingSurface:Detailed"][surface]["zone_name"]
                zones[zone]['area'] = zone_area

            # links surface name to zone name
            elif content["BuildingSurface:Detailed"][surface]['surface_type'] == 'Wall':
                zone = content["BuildingSurface:Detailed"][surface]["zone_name"]
                zones[zone]['surfaces'].append(surface)

        # links windows to zones and calculates opening areas
        for fenestration in list(content["FenestrationSurface:Detailed"].keys()):
            if content["FenestrationSurface:Detailed"][fenestration]['surface_type'] == 'Window':

                # take vertices which will be considered
                x_vertex = []
                y_vertex = []
                z_vertex = []
                for vertex in list(content["FenestrationSurface:Detailed"][fenestration].keys()):
                    if '_x_' in vertex:
                        x_vertex.append(content["FenestrationSurface:Detailed"][fenestration][vertex])
                    elif '_y_' in vertex:
                        y_vertex.append(content["FenestrationSurface:Detailed"][fenestration][vertex])
                    elif '_z_' in vertex:
                        z_vertex.append(content["FenestrationSurface:Detailed"][fenestration][vertex])
                
                # defines if which is constant (x or y)
                if max(x_vertex) == min(x_vertex):
                    w_list = y_vertex
                elif max(y_vertex) == min(y_vertex):
                    w_list = x_vertex
                
                # creates the input list for the polygon area function
                window_vertices = []
                for i in range(len(z_vertex)):
                    window_vertices.append((w_list[i],z_vertex[i]))

                window_area = polygon_area(window_vertices)

                for zone in list(zones.keys()):
                    for surface in zones[zone]['surfaces']:
                        if surface == content["FenestrationSurface:Detailed"][fenestration]['building_surface_name']:
                            zones[zone]['fenestrations'][fenestration] = window_area

        
    ## FenestrationSurface:Detailed
        # defines windows sizes and scale factor to create ref openings
        for zone in zones.keys():
            zones[zone]['ref_window_area'] = zones[zone]['area']*REF_WINDOW_TO_FLOOR_RATIO

            real_window_area = 0
            for fenestration in zones[zone]['fenestrations'].keys():
                real_window_area += zones[zone]['fenestrations'][fenestration]

            zones[zone]['real_window_area'] = real_window_area
            zones[zone]['ref_real_ratio'] = zones[zone]['ref_window_area']/zones[zone]['real_window_area']

        # changes values of windows' vertices
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

            for zone in zones.keys():
                for fenestration in zones[zone]['fenestrations'].keys():
                    if fenestration == i:
                        ref_scale = zones[zone]['ref_real_ratio']

            if content["FenestrationSurface:Detailed"][i]['surface_type'] == 'Window':

                content["FenestrationSurface:Detailed"][i]["vertex_1_x_coordinate"] = ref_vertex(content["FenestrationSurface:Detailed"][i]["vertex_1_x_coordinate"],x_vertex,scalex,ref_scale)
                content["FenestrationSurface:Detailed"][i]["vertex_2_x_coordinate"] = ref_vertex(content["FenestrationSurface:Detailed"][i]["vertex_2_x_coordinate"],x_vertex,scalex,ref_scale)
                content["FenestrationSurface:Detailed"][i]["vertex_3_x_coordinate"] = ref_vertex(content["FenestrationSurface:Detailed"][i]["vertex_3_x_coordinate"],x_vertex,scalex,ref_scale)
                content["FenestrationSurface:Detailed"][i]["vertex_4_x_coordinate"] = ref_vertex(content["FenestrationSurface:Detailed"][i]["vertex_4_x_coordinate"],x_vertex,scalex,ref_scale)
                    
                content["FenestrationSurface:Detailed"][i]["vertex_1_y_coordinate"] = ref_vertex(content["FenestrationSurface:Detailed"][i]["vertex_1_y_coordinate"],y_vertex,scaley,ref_scale)
                content["FenestrationSurface:Detailed"][i]["vertex_2_y_coordinate"] = ref_vertex(content["FenestrationSurface:Detailed"][i]["vertex_2_y_coordinate"],y_vertex,scaley,ref_scale)
                content["FenestrationSurface:Detailed"][i]["vertex_3_y_coordinate"] = ref_vertex(content["FenestrationSurface:Detailed"][i]["vertex_3_y_coordinate"],y_vertex,scaley,ref_scale)
                content["FenestrationSurface:Detailed"][i]["vertex_4_y_coordinate"] = ref_vertex(content["FenestrationSurface:Detailed"][i]["vertex_4_y_coordinate"],y_vertex,scaley,ref_scale)

                content["FenestrationSurface:Detailed"][i]["vertex_1_z_coordinate"] = ref_vertex(content["FenestrationSurface:Detailed"][i]["vertex_1_z_coordinate"],z_vertex,scalez,ref_scale)
                content["FenestrationSurface:Detailed"][i]["vertex_2_z_coordinate"] = ref_vertex(content["FenestrationSurface:Detailed"][i]["vertex_2_z_coordinate"],z_vertex,scalez,ref_scale)
                content["FenestrationSurface:Detailed"][i]["vertex_3_z_coordinate"] = ref_vertex(content["FenestrationSurface:Detailed"][i]["vertex_3_z_coordinate"],z_vertex,scalez,ref_scale)
                content["FenestrationSurface:Detailed"][i]["vertex_4_z_coordinate"] = ref_vertex(content["FenestrationSurface:Detailed"][i]["vertex_4_z_coordinate"],z_vertex,scalez,ref_scale)
            else:
                
                content["FenestrationSurface:Detailed"][i]["vertex_1_x_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_1_x_coordinate"],x_vertex,scalex)
                content["FenestrationSurface:Detailed"][i]["vertex_2_x_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_2_x_coordinate"],x_vertex,scalex)
                content["FenestrationSurface:Detailed"][i]["vertex_3_x_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_3_x_coordinate"],x_vertex,scalex)
                content["FenestrationSurface:Detailed"][i]["vertex_4_x_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_4_x_coordinate"],x_vertex,scalex)
                    
                content["FenestrationSurface:Detailed"][i]["vertex_1_y_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_1_y_coordinate"],y_vertex,scaley)
                content["FenestrationSurface:Detailed"][i]["vertex_2_y_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_2_y_coordinate"],y_vertex,scaley)
                content["FenestrationSurface:Detailed"][i]["vertex_3_y_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_3_y_coordinate"],y_vertex,scaley)
                content["FenestrationSurface:Detailed"][i]["vertex_4_y_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_4_y_coordinate"],y_vertex,scaley)

    # window area changes according to geometry scales
    elif window_scale:
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

    # window area does not change
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

            if content["FenestrationSurface:Detailed"][i]['surface_type'] == 'Window':
                
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
            
            else:                
                content["FenestrationSurface:Detailed"][i]["vertex_1_x_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_1_x_coordinate"],x_vertex,scalex)
                content["FenestrationSurface:Detailed"][i]["vertex_2_x_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_2_x_coordinate"],x_vertex,scalex)
                content["FenestrationSurface:Detailed"][i]["vertex_3_x_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_3_x_coordinate"],x_vertex,scalex)
                content["FenestrationSurface:Detailed"][i]["vertex_4_x_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_4_x_coordinate"],x_vertex,scalex)
                    
                content["FenestrationSurface:Detailed"][i]["vertex_1_y_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_1_y_coordinate"],y_vertex,scaley)
                content["FenestrationSurface:Detailed"][i]["vertex_2_y_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_2_y_coordinate"],y_vertex,scaley)
                content["FenestrationSurface:Detailed"][i]["vertex_3_y_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_3_y_coordinate"],y_vertex,scaley)
                content["FenestrationSurface:Detailed"][i]["vertex_4_y_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_4_y_coordinate"],y_vertex,scaley)

    ## Shading:Building:Detailed
    
    ##### RV - starts
		# fixes partially the shading scaling using 'Shading:Building:Detailed' objects
    
    if not ref:
        verts = np.empty([4])
        vert_max = 0
        vert_min = 0
        # erase shading devices
        if 'Shading:Building:Detailed' in list(content.keys()):
            if shading_scale:  # at the moment, code does not work for "shading_scale = False"
                for i in list(content['Shading:Building:Detailed'].keys()):
                    print i
                    for j,k in enumerate(content['Shading:Building:Detailed'][i]['vertices']):
                        content['Shading:Building:Detailed'][i]['vertices'][j]['vertex_z_coordinate'] = content["Shading:Building:Detailed"][i]["vertices"][j]["vertex_z_coordinate"]*scalez
                        print content['Shading:Building:Detailed'][i]['vertices'][j]
                        if ('_1' in i) or ('_3' in i):
                            verts[j] = content['Shading:Building:Detailed'][i]['vertices'][j]['vertex_y_coordinate']
                        if ('_2' in i) or ('_4' in i):
                            verts[j] = content['Shading:Building:Detailed'][i]['vertices'][j]['vertex_x_coordinate']
                        vert_max = max(verts)
                        vert_min = min(verts)
                    print vert_min, vert_max
                    for j,k in enumerate(content['Shading:Building:Detailed'][i]['vertices']):
                        if ('_1' in i) or ('_3' in i):
                            content['Shading:Building:Detailed'][i]['vertices'][j]['vertex_x_coordinate'] = content['Shading:Building:Detailed'][i]['vertices'][j]['vertex_x_coordinate']*scalex
                            if '_1' in i:
                                if content['Shading:Building:Detailed'][i]['vertices'][j]['vertex_y_coordinate'] == vert_max:
                                    content['Shading:Building:Detailed'][i]['vertices'][j]['vertex_y_coordinate'] = vert_max*scaley
                                else:
                                    content['Shading:Building:Detailed'][i]['vertices'][j]['vertex_y_coordinate'] = vert_max*scaley - (vert_max - vert_min)
                            else:
                                if content['Shading:Building:Detailed'][i]['vertices'][j]['vertex_y_coordinate'] == vert_min:
                                    content['Shading:Building:Detailed'][i]['vertices'][j]['vertex_y_coordinate'] = vert_min*scaley
                                else:
                                    content['Shading:Building:Detailed'][i]['vertices'][j]['vertex_y_coordinate'] = vert_min*scaley + (vert_max - vert_min)
                        else:
                            content['Shading:Building:Detailed'][i]['vertices'][j]['vertex_y_coordinate'] = content['Shading:Building:Detailed'][i]['vertices'][j]['vertex_y_coordinate']*scaley
                            if '_2' in i:
                                if content['Shading:Building:Detailed'][i]['vertices'][j]['vertex_x_coordinate'] == vert_min:
                                    content['Shading:Building:Detailed'][i]['vertices'][j]['vertex_x_coordinate'] = vert_min*scalex
                                else:
                                    content['Shading:Building:Detailed'][i]['vertices'][j]['vertex_x_coordinate'] = vert_min*scalex + (vert_max - vert_min)
                            else:
                                if content['Shading:Building:Detailed'][i]['vertices'][j]['vertex_x_coordinate'] == vert_max:
                                    content['Shading:Building:Detailed'][i]['vertices'][j]['vertex_x_coordinate'] = vert_max*scalex
                                else:
                                    content['Shading:Building:Detailed'][i]['vertices'][j]['vertex_x_coordinate'] = vert_max*scalex - (vert_max - vert_min)

	##### RV - ends

    # writing  epJSON file
    file = open(output_name, "w")
    content = json.dumps(content)
    file.write(content)
    file.close()

    os.system('energyplus -x -c '+output_name)
    
    ##### RV - starts
		# also removes the 'sqlite.err' file
    
    os.system('rm eplusout.* & rm sqlite.err')
    
    ##### RV - ends

######## Test function changing values on the following lines ########

# # Define the name of the input file here
# FILE_NAME = 'vn_Caso2.idf'

# scaling(scalex=2, scaley=2,scalez=2, ref=False, 
#     window_scale=False, shading_scale=False,
#     input_file= FILE_NAME, output_name='teste1b.epJSON')

# scaling(scalex=2, scaley=2,scalez=2, ref=False, 
#     window_scale=True, shading_scale=False,
#     input_file= FILE_NAME, output_name='teste2b.epJSON')

# scaling(scalex=2, scaley=2,scalez=2, ref=False, 
#     window_scale=False, shading_scale=True,
#     input_file= FILE_NAME, output_name='teste3b.epJSON')

# scaling(scalex=2, scaley=1,scalez=1, ref=True, 
#     window_scale=False, shading_scale=True,
#     input_file= FILE_NAME, output_name='teste4b.epJSON')

scaling(scalex = 2, scaley = 2, scalez = 1, ref = False, 
		window_scale = False, shading_scale = True,
		input_file = 'vn_caso2_rv.idf', output_name = 'vn_caso2_rv_new.epJSON')

'''
O que pode ser melhorado:
- Janelas:
    *conferir se W (ou H) nao passa da aresta da Wall
    *conferir se a janela nao se sobrepoem com a porta
    **definir se vai consertar autmaticamente, ou so avisar
- Shading:
    Encontrar uma forma de acompanhar a geometria, sem mudar o angulo de sombreamento
'''
