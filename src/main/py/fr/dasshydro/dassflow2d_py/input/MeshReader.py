from abc import ABC, abstractmethod
from mesh.UncompleteMesh import UncompleteMesh

class MeshReader(ABC):
    @abstractmethod
    def read(self, file_path) -> UncompleteMesh:
        pass
