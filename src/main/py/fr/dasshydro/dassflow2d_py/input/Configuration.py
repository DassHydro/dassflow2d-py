from mesh.Mesh import MeshType, MeshShape
from resolution.ResolutionMethod import TemporalScheme, SpatialScheme

class Configuration:

    def __init__(self):
        raise NotImplementedError("Not yet implemented.")

    def getMeshType(self) -> MeshType:
        raise NotImplementedError("Not yet implemented.")

    def getMeshShape(self) -> MeshShape:
        raise NotImplementedError("Not yet implemented.")
    
    def getMeshFile(self) -> str:
        raise NotImplementedError("Not yet implemented.")

    def getTemporalScheme(self) -> TemporalScheme:
        raise NotImplementedError("Not yet implemented.")

    def getSpatialScheme(self) -> SpatialScheme:
        raise NotImplementedError("Not yet implemented.")
    
    def getInitialStateFile(self) -> str:
        raise NotImplementedError("Not yet implemented.")
    
    def updateValues(values: dict[str, str]):
        raise NotImplementedError("Not yet implemented.")


def load_from_file(file_path: str) -> Configuration:
    raise NotImplementedError("Not yet implemented.")
