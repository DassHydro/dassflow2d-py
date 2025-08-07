from abc import ABC, abstractmethod
from fr.dasshydro.dassflow2d_py.mesh.Mesh import Mesh

class MeshReader(ABC):
    @abstractmethod
    def read(self, file_path: str) -> Mesh:
        pass
