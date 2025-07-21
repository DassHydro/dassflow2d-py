from mesh.Mesh import MeshType, MeshShape

class Configuration:

    def __init__(self):
        raise NotImplementedError("Not yet implemented.")
    
    def getMeshType(self) -> MeshType:
        raise NotImplementedError("Not yet implemented.")
    
    def getMeshShape(self) -> MeshShape:
        raise NotImplementedError("Not yet implemented.")

def load_from_file(file_path: str) -> Configuration:
    raise NotImplementedError("Not yet implemented.")