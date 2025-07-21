from enum import Enum

class MeshShape(Enum):
    TRIANGULAR = 1
    QUADRILATERAL = 2
    HYBRID = 3

class MeshType(Enum):
    BASIC = 0
    DASSFLOW = 1

class Mesh:

    def __init__(self):
        raise NotImplementedError("Not yet implemented.")