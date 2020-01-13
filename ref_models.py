from scalingGeometry import scaling

FILE_NAME = 'vn_Caso2.idf'

z_scales = [1,2]
x_scales = [1+i*.25 for i in range(5)]
y_scales = [1+i*.25 for i in range(5)]

for z in z_scales:
    for x in x_scales:
        for y in y_scales:

            scaling(scalex=x, scaley=y,scalez=z, ref=True, 
                window_scale=False, shading_scale=False,
                input_file= FILE_NAME, output_name='ref_'+str(x_scales.index(x))+'_'+str(y_scales.index(y))+'_'+str(z_scales.index(z))+'.epJSON')