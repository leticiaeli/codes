
import json
import os

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

# def ref_vertex(window, surface, scalex, scaley, scalez,ref_scale):
    # Checks which vertex it is, so it defines the new value,
    # in order to keep the reference opening area
    
    # ref_scale_sqrt = ref_scale**(1/2)
    
    # if max(vertex_list) == min(vertex_list):
        # new_vertex = vertex*scale
    # elif vertex == min(vertex_list):
        # new_vertex = (scale*(max(vertex_list)+min(vertex_list))-(ref_scale_sqrt*(max(vertex_list)-min(vertex_list))))*.5
    # elif vertex == max(vertex_list):
        # new_vertex = (scale*(max(vertex_list)+min(vertex_list))+(ref_scale_sqrt*(max(vertex_list)-min(vertex_list))))*.5

    # return(new_vertex)

def scaling(scales={'scalex':2, 'scaley':2,'scalez':2}, ref=False, window_scale=True,
    shading_scale=True, input_file='model.epJSON',output_name='scaled_model.epJSON'):
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
            
    ## Zone
    for i in list(content["Zone"].keys()):
        content["Zone"][i]["x_origin"] = content["Zone"][i]["x_origin"]*scales['scalex']
        content["Zone"][i]["y_origin"] = content["Zone"][i]["y_origin"]*scales['scaley']
        content["Zone"][i]["z_origin"] = content["Zone"][i]["z_origin"]*scales['scalez']

    ## BuildingSurface:Detailed

    # dictionary to define how windows change size
    walls_vertices = {}

    # will be used to define building ratio
    x_max = 0
    y_max = 0

    for i in list(content["BuildingSurface:Detailed"].keys()):
        
        wall_x_list = []
        wall_y_list = []
        wall_z_list = []

        for j,k in enumerate(content["BuildingSurface:Detailed"][i]["vertices"]):

            # scales the vertices of surfaces
            content["BuildingSurface:Detailed"][i]["vertices"][j]["vertex_x_coordinate"] = content["BuildingSurface:Detailed"][i]["vertices"][j]["vertex_x_coordinate"]*scales['scalex']
            content["BuildingSurface:Detailed"][i]["vertices"][j]["vertex_y_coordinate"] = content["BuildingSurface:Detailed"][i]["vertices"][j]["vertex_y_coordinate"]*scales['scaley']
            content["BuildingSurface:Detailed"][i]["vertices"][j]["vertex_z_coordinate"] = content["BuildingSurface:Detailed"][i]["vertices"][j]["vertex_z_coordinate"]*scales['scalez']

            wall_x_list.append(content["BuildingSurface:Detailed"][i]["vertices"][j]["vertex_x_coordinate"])
            wall_y_list.append(content["BuildingSurface:Detailed"][i]["vertices"][j]["vertex_y_coordinate"])
            wall_z_list.append(content["BuildingSurface:Detailed"][i]["vertices"][j]["vertex_z_coordinate"])
            
        walls_vertices[i] = {}
        walls_vertices[i]['wall_x_min'] = min(wall_x_list)
        walls_vertices[i]['wall_y_min'] = min(wall_y_list)
        walls_vertices[i]['wall_z_min'] = min(wall_z_list)
        walls_vertices[i]['wall_x_max'] = max(wall_x_list)
        walls_vertices[i]['wall_y_max'] = max(wall_y_list)
        walls_vertices[i]['wall_z_max'] = max(wall_z_list)

        # will be used to define building ratio
        if walls_vertices[i]['wall_x_max'] > x_max:
            x_max = walls_vertices[i]['wall_x_max']
        if walls_vertices[i]['wall_y_max'] > y_max:
            y_max = walls_vertices[i]['wall_y_max']

    ## AirflowNetwork:SimulationControl
    ratio_of_building_afn = min(x_max,y_max)/max(x_max,y_max)

    if "AirflowNetwork:SimulationControl" in list(content.keys()):
        for i in list(content["AirflowNetwork:SimulationControl"].keys()):
            content["AirflowNetwork:SimulationControl"][i]["ratio_of_building_width_along_short_axis_to_width_along_long_axis"] =  ratio_of_building_afn

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
                
            # ref_vertex(content["FenestrationSurface:Detailed"][i], walls_vertices[content["FenestrationSurface:Detailed"][i]['building_surface_name']])
            
            vertex_dict ={
            'x_vertex': [],
            'y_vertex': [],
            'z_vertex': []
            }

            for vertex in list(content["FenestrationSurface:Detailed"][i].keys()):

                if '_x_' in vertex:
                    vertex_dict['x_vertex'].append(content["FenestrationSurface:Detailed"][i][vertex])
                elif '_y_' in vertex:
                    vertex_dict['y_vertex'].append(content["FenestrationSurface:Detailed"][i][vertex])
                elif '_z_' in vertex:
                    vertex_dict['z_vertex'].append(content["FenestrationSurface:Detailed"][i][vertex])

            if content["FenestrationSurface:Detailed"][i]['surface_type'] == 'Window':

                for zone in zones.keys():
                    for fenestration in zones[zone]['fenestrations'].keys():
                        if fenestration == i:
                            ref_scale = zones[zone]['ref_real_ratio']
                
                wall = content["FenestrationSurface:Detailed"][i]['building_surface_name']
                
                same_z = True  # to verify if z vertices will change
                
                for letter in ['x','y']:
                    
                    if min(vertex_dict[letter+'_vertex']) == max(vertex_dict[letter+'_vertex']):
                        for number in range(1,5):
                            content["FenestrationSurface:Detailed"][i]["vertex_"+str(number)+"_"+letter+"_coordinate"] = content["FenestrationSurface:Detailed"][i]["vertex_"+str(number)+"_"+letter+"_coordinate"]*scales['scale'+letter]
                    
                    elif ref_scale*(max(vertex_dict[letter+'_vertex'])-min(vertex_dict[letter+'_vertex'])) < walls_vertices[wall]['wall_'+letter+'_max']-walls_vertices[wall]['wall_'+letter+'_min']:
                        for number in range(1,5):
                        
                            if content["FenestrationSurface:Detailed"][i]["vertex_"+str(number)+"_"+letter+"_coordinate"] == min(vertex_dict[letter+'_vertex']):
                                content["FenestrationSurface:Detailed"][i]["vertex_"+str(number)+"_"+letter+"_coordinate"] = ((walls_vertices[wall]['wall_'+letter+'_max']+walls_vertices[wall]['wall_'+letter+'_min'])-ref_scale*(max(vertex_dict[letter+'_vertex'])-min(vertex_dict[letter+'_vertex'])))*.5
                            else:
                                content["FenestrationSurface:Detailed"][i]["vertex_"+str(number)+"_"+letter+"_coordinate"] = ((walls_vertices[wall]['wall_'+letter+'_max']+walls_vertices[wall]['wall_'+letter+'_min'])+ref_scale*(max(vertex_dict[letter+'_vertex'])-min(vertex_dict[letter+'_vertex'])))*.5
                    else:
                        for number in range(1,5):
                        
                            if content["FenestrationSurface:Detailed"][i]["vertex_"+str(number)+"_"+letter+"_coordinate"] == min(vertex_dict[letter+'_vertex']):
                                content["FenestrationSurface:Detailed"][i]["vertex_"+str(number)+"_"+letter+"_coordinate"] = walls_vertices[wall]['wall_'+letter+'_min']+(walls_vertices[wall]['wall_'+letter+'_max']-walls_vertices[wall]['wall_'+letter+'_min'])*.01
                            else:
                                content["FenestrationSurface:Detailed"][i]["vertex_"+str(number)+"_"+letter+"_coordinate"] = walls_vertices[wall]['wall_'+letter+'_min']+(walls_vertices[wall]['wall_'+letter+'_max']-walls_vertices[wall]['wall_'+letter+'_min'])*.99
                                
                        z_refscale = (ref_scale*(max(vertex_dict[letter+'_vertex'])-min(vertex_dict[letter+'_vertex'])))/((walls_vertices[wall]['wall_'+letter+'_max']+walls_vertices[wall]['wall_'+letter+'_min'])*.98)
                        same_z = False
                        
                if same_z:
                    z_refscale = (ref_scale*(max(vertex_dict[letter+'_vertex'])-min(vertex_dict[letter+'_vertex'])))/((walls_vertices[wall]['wall_'+letter+'_max']+walls_vertices[wall]['wall_'+letter+'_min'])*.98)
                    if  min(vertex_dict['z_vertex'])+(z_refscale*(max(vertex_dict['z_vertex'])-min(vertex_dict['z_vertex']))) < walls_vertices[wall]['wall_z_max']:
                        
                        for number in range(1,5):
                            
                            if content["FenestrationSurface:Detailed"][i]["vertex_"+str(number)+"_z_coordinate"] == max(vertex_dict['z_vertex']):
                                content["FenestrationSurface:Detailed"][i]["vertex_"+str(number)+"_z_coordinate"] = min(vertex_dict['z_vertex'])+(z_refscale*(max(vertex_dict['z_vertex'])-min(vertex_dict['z_vertex'])))
                    else:
                        delta_z = min(vertex_dict['z_vertex'])+(z_refscale*(max(vertex_dict['z_vertex'])-min(vertex_dict['z_vertex'])))-walls_vertices[wall]['wall_z_max']*(.99)
                        for number in range(1,5):
                            
                            if content["FenestrationSurface:Detailed"][i]["vertex_"+str(number)+"_z_coordinate"] == max(vertex_dict['z_vertex']):
                                content["FenestrationSurface:Detailed"][i]["vertex_"+str(number)+"_z_coordinate"] = walls_vertices[wall]['wall_z_max']*99
                            else:
                                content["FenestrationSurface:Detailed"][i]["vertex_"+str(number)+"_z_coordinate"] = content["FenestrationSurface:Detailed"][i]["vertex_"+str(number)+"_z_coordinate"]-delta_z
                    
                # content["FenestrationSurface:Detailed"][i]["vertex_1_x_coordinate"] = ref_vertex(content["FenestrationSurface:Detailed"][i]["vertex_1_x_coordinate"],x_vertex,scalex,ref_scale)
                # content["FenestrationSurface:Detailed"][i]["vertex_2_x_coordinate"] = ref_vertex(content["FenestrationSurface:Detailed"][i]["vertex_2_x_coordinate"],x_vertex,scalex,ref_scale)
                # content["FenestrationSurface:Detailed"][i]["vertex_3_x_coordinate"] = ref_vertex(content["FenestrationSurface:Detailed"][i]["vertex_3_x_coordinate"],x_vertex,scalex,ref_scale)
                # content["FenestrationSurface:Detailed"][i]["vertex_4_x_coordinate"] = ref_vertex(content["FenestrationSurface:Detailed"][i]["vertex_4_x_coordinate"],x_vertex,scalex,ref_scale)
                    
                # content["FenestrationSurface:Detailed"][i]["vertex_1_y_coordinate"] = ref_vertex(content["FenestrationSurface:Detailed"][i]["vertex_1_y_coordinate"],y_vertex,scaley,ref_scale)
                # content["FenestrationSurface:Detailed"][i]["vertex_2_y_coordinate"] = ref_vertex(content["FenestrationSurface:Detailed"][i]["vertex_2_y_coordinate"],y_vertex,scaley,ref_scale)
                # content["FenestrationSurface:Detailed"][i]["vertex_3_y_coordinate"] = ref_vertex(content["FenestrationSurface:Detailed"][i]["vertex_3_y_coordinate"],y_vertex,scaley,ref_scale)
                # content["FenestrationSurface:Detailed"][i]["vertex_4_y_coordinate"] = ref_vertex(content["FenestrationSurface:Detailed"][i]["vertex_4_y_coordinate"],y_vertex,scaley,ref_scale)

                # content["FenestrationSurface:Detailed"][i]["vertex_1_z_coordinate"] = ref_vertex(content["FenestrationSurface:Detailed"][i]["vertex_1_z_coordinate"],z_vertex,scalez,ref_scale)
                # content["FenestrationSurface:Detailed"][i]["vertex_2_z_coordinate"] = ref_vertex(content["FenestrationSurface:Detailed"][i]["vertex_2_z_coordinate"],z_vertex,scalez,ref_scale)
                # content["FenestrationSurface:Detailed"][i]["vertex_3_z_coordinate"] = ref_vertex(content["FenestrationSurface:Detailed"][i]["vertex_3_z_coordinate"],z_vertex,scalez,ref_scale)
                # content["FenestrationSurface:Detailed"][i]["vertex_4_z_coordinate"] = ref_vertex(content["FenestrationSurface:Detailed"][i]["vertex_4_z_coordinate"],z_vertex,scalez,ref_scale)
            else:
                
                content["FenestrationSurface:Detailed"][i]["vertex_1_x_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_1_x_coordinate"],vertex_dict['x_vertex'],scales['scalex'])
                content["FenestrationSurface:Detailed"][i]["vertex_2_x_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_2_x_coordinate"],vertex_dict['x_vertex'],scales['scalex'])
                content["FenestrationSurface:Detailed"][i]["vertex_3_x_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_3_x_coordinate"],vertex_dict['x_vertex'],scales['scalex'])
                content["FenestrationSurface:Detailed"][i]["vertex_4_x_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_4_x_coordinate"],vertex_dict['x_vertex'],scales['scalex'])
                    
                content["FenestrationSurface:Detailed"][i]["vertex_1_y_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_1_y_coordinate"],vertex_dict['y_vertex'],scales['scaley'])
                content["FenestrationSurface:Detailed"][i]["vertex_2_y_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_2_y_coordinate"],vertex_dict['y_vertex'],scales['scaley'])
                content["FenestrationSurface:Detailed"][i]["vertex_3_y_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_3_y_coordinate"],vertex_dict['y_vertex'],scales['scaley'])
                content["FenestrationSurface:Detailed"][i]["vertex_4_y_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_4_y_coordinate"],vertex_dict['y_vertex'],scales['scaley'])

    # window area changes according to geometry scales
    elif window_scale:
        for i in list(content["FenestrationSurface:Detailed"].keys()):

            if content["FenestrationSurface:Detailed"][i]['surface_type'] == 'Window':
            
                content["FenestrationSurface:Detailed"][i]["vertex_1_x_coordinate"] = content["FenestrationSurface:Detailed"][i]["vertex_1_x_coordinate"]*scales['scalex']
                content["FenestrationSurface:Detailed"][i]["vertex_2_x_coordinate"] = content["FenestrationSurface:Detailed"][i]["vertex_2_x_coordinate"]*scales['scalex']
                content["FenestrationSurface:Detailed"][i]["vertex_3_x_coordinate"] = content["FenestrationSurface:Detailed"][i]["vertex_3_x_coordinate"]*scales['scalex']
                content["FenestrationSurface:Detailed"][i]["vertex_4_x_coordinate"] = content["FenestrationSurface:Detailed"][i]["vertex_4_x_coordinate"]*scales['scalex']
                    
                content["FenestrationSurface:Detailed"][i]["vertex_1_y_coordinate"] = content["FenestrationSurface:Detailed"][i]["vertex_1_y_coordinate"]*scales['scaley']
                content["FenestrationSurface:Detailed"][i]["vertex_2_y_coordinate"] = content["FenestrationSurface:Detailed"][i]["vertex_2_y_coordinate"]*scales['scaley']
                content["FenestrationSurface:Detailed"][i]["vertex_3_y_coordinate"] = content["FenestrationSurface:Detailed"][i]["vertex_3_y_coordinate"]*scales['scaley']
                content["FenestrationSurface:Detailed"][i]["vertex_4_y_coordinate"] = content["FenestrationSurface:Detailed"][i]["vertex_4_y_coordinate"]*scales['scaley']

                content["FenestrationSurface:Detailed"][i]["vertex_1_z_coordinate"] = content["FenestrationSurface:Detailed"][i]["vertex_1_z_coordinate"]*scales['scalez']
                content["FenestrationSurface:Detailed"][i]["vertex_2_z_coordinate"] = content["FenestrationSurface:Detailed"][i]["vertex_2_z_coordinate"]*scales['scalez']
                content["FenestrationSurface:Detailed"][i]["vertex_3_z_coordinate"] = content["FenestrationSurface:Detailed"][i]["vertex_3_z_coordinate"]*scales['scalez']
                content["FenestrationSurface:Detailed"][i]["vertex_4_z_coordinate"] = content["FenestrationSurface:Detailed"][i]["vertex_4_z_coordinate"]*scales['scalez']
            else:
                
                content["FenestrationSurface:Detailed"][i]["vertex_1_x_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_1_x_coordinate"],x_vertex,scales['scalex'])
                content["FenestrationSurface:Detailed"][i]["vertex_2_x_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_2_x_coordinate"],x_vertex,scales['scalex'])
                content["FenestrationSurface:Detailed"][i]["vertex_3_x_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_3_x_coordinate"],x_vertex,scales['scalex'])
                content["FenestrationSurface:Detailed"][i]["vertex_4_x_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_4_x_coordinate"],x_vertex,scales['scalex'])
                    
                content["FenestrationSurface:Detailed"][i]["vertex_1_y_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_1_y_coordinate"],y_vertex,scales['scaley'])
                content["FenestrationSurface:Detailed"][i]["vertex_2_y_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_2_y_coordinate"],y_vertex,scales['scaley'])
                content["FenestrationSurface:Detailed"][i]["vertex_3_y_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_3_y_coordinate"],y_vertex,scales['scaley'])
                content["FenestrationSurface:Detailed"][i]["vertex_4_y_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_4_y_coordinate"],y_vertex,scales['scaley'])

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
                
                content["FenestrationSurface:Detailed"][i]["vertex_1_x_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_1_x_coordinate"],x_vertex,scales['scalex'])
                content["FenestrationSurface:Detailed"][i]["vertex_2_x_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_2_x_coordinate"],x_vertex,scales['scalex'])
                content["FenestrationSurface:Detailed"][i]["vertex_3_x_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_3_x_coordinate"],x_vertex,scales['scalex'])
                content["FenestrationSurface:Detailed"][i]["vertex_4_x_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_4_x_coordinate"],x_vertex,scales['scalex'])
                    
                content["FenestrationSurface:Detailed"][i]["vertex_1_y_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_1_y_coordinate"],y_vertex,scales['scaley'])
                content["FenestrationSurface:Detailed"][i]["vertex_2_y_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_2_y_coordinate"],y_vertex,scales['scaley'])
                content["FenestrationSurface:Detailed"][i]["vertex_3_y_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_3_y_coordinate"],y_vertex,scales['scaley'])
                content["FenestrationSurface:Detailed"][i]["vertex_4_y_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_4_y_coordinate"],y_vertex,scales['scaley'])

                content["FenestrationSurface:Detailed"][i]["vertex_1_z_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_1_z_coordinate"],z_vertex,scales['scalez'])
                content["FenestrationSurface:Detailed"][i]["vertex_2_z_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_2_z_coordinate"],z_vertex,scales['scalez'])
                content["FenestrationSurface:Detailed"][i]["vertex_3_z_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_3_z_coordinate"],z_vertex,scales['scalez'])
                content["FenestrationSurface:Detailed"][i]["vertex_4_z_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_4_z_coordinate"],z_vertex,scales['scalez'])
            
            else:                
                content["FenestrationSurface:Detailed"][i]["vertex_1_x_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_1_x_coordinate"],x_vertex,scales['scalex'])
                content["FenestrationSurface:Detailed"][i]["vertex_2_x_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_2_x_coordinate"],x_vertex,scales['scalex'])
                content["FenestrationSurface:Detailed"][i]["vertex_3_x_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_3_x_coordinate"],x_vertex,scales['scalex'])
                content["FenestrationSurface:Detailed"][i]["vertex_4_x_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_4_x_coordinate"],x_vertex,scales['scalex'])
                    
                content["FenestrationSurface:Detailed"][i]["vertex_1_y_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_1_y_coordinate"],y_vertex,scales['scaley'])
                content["FenestrationSurface:Detailed"][i]["vertex_2_y_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_2_y_coordinate"],y_vertex,scales['scaley'])
                content["FenestrationSurface:Detailed"][i]["vertex_3_y_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_3_y_coordinate"],y_vertex,scales['scaley'])
                content["FenestrationSurface:Detailed"][i]["vertex_4_y_coordinate"] = constant_vertex(content["FenestrationSurface:Detailed"][i]["vertex_4_y_coordinate"],y_vertex,scales['scaley'])

    ## Shading:Building:Detailed
    if not ref:
        # erase shading devices
        if 'Shading:Building:Detailed' in list(content.keys()):
            if shading_scale:  # at the moment, code does not work for "shading_scale = False"
                for i in list(content["Shading:Building:Detailed"].keys()):
                    for j,k in enumerate(content["Shading:Building:Detailed"][i]["vertices"]):
                        content["Shading:Building:Detailed"][i]["vertices"][j]["vertex_x_coordinate"] = content["Shading:Building:Detailed"][i]["vertices"][j]["vertex_x_coordinate"]*scales['scalex']
                        content["Shading:Building:Detailed"][i]["vertices"][j]["vertex_y_coordinate"] = content["Shading:Building:Detailed"][i]["vertices"][j]["vertex_y_coordinate"]*scales['scaley']
                        content["Shading:Building:Detailed"][i]["vertices"][j]["vertex_z_coordinate"] = content["Shading:Building:Detailed"][i]["vertices"][j]["vertex_z_coordinate"]*scales['scalez']

    # writing  epJSON file
    file = open(output_name, "w")
    content = json.dumps(content)
    file.write(content)
    file.close()

    os.system('energyplus -x -c '+output_name)
    os.system('rm eplusout.*')

######## Test function changing values on the following lines ########

# Define the name of the input file here
FILE_NAME = 'vn_Caso2.idf'
scales={'scalex':2, 'scaley':2,'scalez':2}

scaling(scales, ref=True, 
    window_scale=False, shading_scale=False,
    input_file= FILE_NAME, output_name='teste_newref.epJSON')

# scaling(scalex=2, scaley=2,scalez=2, ref=False, 
    # window_scale=True, shading_scale=False,
    # input_file= FILE_NAME, output_name='teste2b.epJSON')

# scaling(scalex=2, scaley=2,scalez=2, ref=False, 
    # window_scale=False, shading_scale=True,
    # input_file= FILE_NAME, output_name='teste3b.epJSON')

# scaling(scalex=2, scaley=1,scalez=1, ref=True, 
    # window_scale=False, shading_scale=True,
    # input_file= FILE_NAME, output_name='teste4b.epJSON')



'''
O que pode ser melhorado:
- Janelas:
    *conferir se W (ou H) não passa da aresta da Wall
    *conferir se a janela não se sobrepoem com a porta
    **definir se vai consertar autmaticamente, ou só avisar
- Shading:
    Encontrar uma forma de acompanhar a geometria, sem mudar o ângulo de sombreamento
'''
