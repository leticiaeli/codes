from glob import glob
import os
from idf_bundler import idf_bundler
from scalingGeometry import scaling

m_geom = glob('slices/Multi/m_g_geom*')
u_geom = glob('slices/Uni/u_g_geom*')

for geom in m_geom:
    
    idf_bundler(['slices/rotation_000.txt','slices/Multi/m_construction_ref.txt','slices/Multi/m_afn.txt','slices/main_materials_fixed.txt', 'slices/main.txt',geom,'slices/Multi/m_fenes_17'+geom.split('/')[-1][3:]],geom.split('.')[0]+'COMJANELA.idf')
for geom in u_geom:
    
    idf_bundler(['slices/rotation_000.txt','slices/Uni/u_construction_ref.txt','slices/Uni/u_afn.txt','slices/main_materials_fixed.txt', 'slices/main.txt',geom,'slices/Uni/u_fenes_17'+geom.split('/')[-1][3:]],geom.split('.')[0]+'COMJANELA.idf')

geom_janela = glob('slices/Uni/*COMJANELA*') + glob('slices/Multi/*COMJANELA*')
for geom in geom_janela:
    os.system('energyplus -c '+geom)

geom_janela = glob('*COMJANELA*')

wwrs = [.1,.3,.5]

for geom in geom_janela:
    for wwr in wwrs:
        scaling(scales={'scalex':1, 'scaley':1,'scalez':1}, ref=(False,.17), wwr = (True,wwr), window_scale=False,
        shading_scale=False, input_file=geom,output_name=geom.split('.')[0]+'_wwr'+str(int(100*wwr)))
