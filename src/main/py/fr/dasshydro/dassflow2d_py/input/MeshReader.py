from abc import ABC, abstractmethod
from fr.dasshydro.dassflow2d_py.mesh.Mesh import RawCell, RawVertex

class MeshReader(ABC):
    @abstractmethod
    def read(self, file_path: str) -> tuple[list[RawVertex], list[RawCell], list[int], list[int]]:
        pass
