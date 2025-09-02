# mesh generated for testing DassflowMeshReader
6 4 1.0
#Vertex||| id vertex, x coord, y coord, bathymetry
1 0.0 0.0 0.0
2 1.0 0.0 0.0
3 2.0 0.0 0.0
4 0.0 1.0 0.0
5 1.0 1.0 0.0
6 2.0 1.0 0.0
#cells||| id cell, id_vertex1, id_vertex2, id_vertex3, id_vertex4, patch_manning, bathymetry
1 1 2 5 1 1 0.
2 2 3 6 2 1 0.
3 1 4 5 1 1 0.
4 2 5 6 2 1 0.
# boundaries
INLET 1 1
3 1 1 1 1
OUTLET 1 1
2 1 1 1 1
