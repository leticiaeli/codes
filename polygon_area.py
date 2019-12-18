def area(p):
     return 0.5 * abs(sum(p[i][0]*p[(i+1)%len(p)][1] - p[(i+1)%len(p)][0]*p[i][1]
        for i in range(len(p))))


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
