from abc import ABC, abstractmethod
from fr.dasshydro.dassflow2d_py.mesh.IncompleteMesh import IncompleteMesh

class MeshReader(ABC):
    @abstractmethod
    def read(self, file_path) -> IncompleteMesh:
        pass
