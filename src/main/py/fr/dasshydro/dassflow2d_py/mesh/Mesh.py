from enum import Enum

class MeshShape(Enum):
    TRIANGULAR = "triangular"
    QUADRILATERAL = "quadrilateral"
    HYBRID = "hybrid"

class MeshType(Enum):
    BASIC = "basic"
    DASSFLOW = "dassflow"

class Mesh:

    def __init__(self):
        raise NotImplementedError("Not yet implemented.")
