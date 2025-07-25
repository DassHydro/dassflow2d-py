from abc import ABC, abstractmethod
from mesh.IncompleteMesh import IncompleteMesh

class MeshReader(ABC):
    @abstractmethod
    def read(self, file_path) -> IncompleteMesh:
        pass
