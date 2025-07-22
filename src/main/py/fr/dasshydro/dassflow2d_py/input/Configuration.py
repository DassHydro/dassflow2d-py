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
    
    def setMeshType(self, mesh_type: MeshType):
        raise NotImplementedError("Not yet implemented.")

    def setMeshShape(self, mesh_shape: MeshShape):
        raise NotImplementedError("Not yet implemented.")
    
    def setMeshFile(self, mesh_file: str):
        raise NotImplementedError("Not yet implemented.")

    def setTemporalScheme(self, temporal_scheme: TemporalScheme):
        raise NotImplementedError("Not yet implemented.")

    def setSpatialScheme(self, spatial_scheme: SpatialScheme):
        raise NotImplementedError("Not yet implemented.")
    
    def setInitialStateFile(self, initial_state_file: str):
        raise NotImplementedError("Not yet implemented.")


def load_from_file(file_path: str) -> Configuration:
    raise NotImplementedError("Not yet implemented.")
