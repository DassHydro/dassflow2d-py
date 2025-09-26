from typing import Callable
from dassflow2d_py.mesh.Mesh import Vertex, Cell

class BathymetryReader:
    """
    UNUSED reader for dedicated file for bathymetry, the idea of a bathymetry outside of the mesh
    has been thrown out.
    """

    def __init__(self):
        raise NotImplementedError("Not yet implemented.")

    def readVertexBathymetry(self) -> Callable[[Vertex], float]:
        raise NotImplementedError("Not yet implemented.")

    def readCellBathymetry(self) -> Callable[[Cell], float]:
        raise NotImplementedError("Not yet implemented.")
