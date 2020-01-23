from scalingGeometry import scaling

## UNI
# files = ['ac_Ref_ZB1a6.idf','ac_Ref_ZB7e8.idf','vn_Ref_ZB1a6.idf','vn_Ref_ZB7e8.idf']
# z_scales = [1,2]
# xy_scales = [(1,1), (1.2,1), (1.6,1),(2.5,1),(1,1.25),(1,2)]
# area_fac = [1,1.1,1.2,1.35,1.5]

## MULTI
files = ['M001_Caso1_vn.idf','M001_Caso1_ac.idf']
z_scales = [1]
xy_scales = [(1,1), (1.2,1), (1.5,1),(2,1),(1,1.5),(1,2)]
area_fac = [1,1.25,1.5]

i=0

# files_list = open('files_list.csv','w')
files_list = open('files_list_multi.csv','w')
files_list.write('case,z,x,y,area_fac,file\n')

for z in z_scales:
    for xy in xy_scales:
        for a in area_fac:
            a_sqrt = a**(1/2)
            for file in files:

                scaling(scales={'scalex':xy[0]*a_sqrt, 'scaley':xy[1]*a_sqrt,'scalez':z}, ref=True, refscale=.17, window_scale=False,
                shading_scale=False, input_file=file,output_name=file.split('.')[0]+'_'+'{:03.0f}'.format(i))

                files_list.write('{:03.0f}'.format(i)+','+str(z)+','+str(xy[0])+','+str(xy[1])+','+str(a)+','+file+'\n')

            i += 1

files_list.close()
