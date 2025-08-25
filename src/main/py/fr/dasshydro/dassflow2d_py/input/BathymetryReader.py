from typing import Callable
from fr.dasshydro.dassflow2d_py.mesh.Mesh import Vertex, Cell

class BathymetryReader:

    def __init__(self):
        raise NotImplementedError("Not yet implemented.")

    def readVertexBathymetry(self) -> Callable[[Vertex], float]:
        raise NotImplementedError("Not yet implemented.")

    def readCellBathymetry(self) -> Callable[[Cell], float]:
        raise NotImplementedError("Not yet implemented.")
