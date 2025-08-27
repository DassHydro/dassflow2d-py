from enum import Enum

class MeshShape(Enum):
    TRIANGULAR = "triangular"
    QUADRILATERAL = "quadrilateral"
    HYBRID = "hybrid"


class MeshType(Enum):
    BASIC = "basic"
    DASSFLOW = "dassflow"


from abc import ABC, abstractmethod

class Vertex(ABC):

    @abstractmethod
    def getID(self) -> int:
        """
        Get the id of the vertex

        :return: id of the vertex
        :rtype: int
        """
        pass

    @abstractmethod
    def getCoordinates(self) -> tuple[float, float]:
        """
        Get the coordinates of the vertex.

        :return: coordinates of the vertex
        :rtype: tuple[float, float]
        """
        pass

    @abstractmethod
    def isBoundary(self) -> bool:
        """
        Check if the vertex is on the boundary.

        :return: True if the vertex is on the boundary, False otherwise
        :rtype: bool
        """
        pass


class Cell(ABC):

    @abstractmethod
    def getID(self) -> int:
        """
        Get the id of the cell

        :return: id of the cell
        :rtype: int
        """
        pass

    @abstractmethod
    def getSurface(self) -> float:
        """
        Get the surface area of the cell

        :return: surface area of the cell
        :rtype: float
        """
        pass

    @abstractmethod
    def getPerimeter(self) -> float:
        """
        Get the perimeter of the cell

        :return: perimeter of the cell
        :rtype: float
        """
        pass

    @abstractmethod
    def getVertices(self) -> list[Vertex]:
        """
        Get the list of the cell's vertices

        :return: list of vertices of the cell
        :rtype: list[Vertices]
        """
        pass

    @abstractmethod
    def getVerticesNumber(self) -> int:
        """
        Get the number of vertices that this cell have.
        It allows to know cell geometry (triangle, quadrilateral ...)

        :return: number of vertices in the cell
        :rtype: int
        """
        pass

    @abstractmethod
    def  getEdges(self) -> list['Edge']:
        """
        Get the list of the cell's edges

        :return: list of edges of the cell
        :rtype: list[Edge]
        """
        pass

    @abstractmethod
    def getNeighbors(self) -> list['Cell']:
        """
        Get all neighboring cells

        :return: list of neighboring cells
        :rtype: list[Cell]
        """
        pass

    @abstractmethod
    def getGravityCenter(self) -> tuple[float, float]:
        """
        Get the cell's gravity center coordinates

        :return: centre of gravity of the cell
        :rtype: tuple[float, float]
        """
        pass

    @abstractmethod
    def isBoundary(self) -> bool:
        """
        Tells if the cell is at mesh boundary

        :return: True if the cell is on the boundary, False otherwise
        :rtype: bool
        """
        pass

    @abstractmethod
    def isGhost(self) -> bool:
        """
        Tells if the cell represent a ghost cell

        :return: True if the cell is a ghost cell, False otherwise
        :rtype: bool
        """
        pass


class Edge(ABC):

    @abstractmethod
    def getID(self) -> int:
        """
        Get the id of the edge

        :return: id of the edge
        :rtype: int
        """
        pass

    @abstractmethod
    def getVertices(self) -> list[Vertex]:
        """
        Get the list of vertices associated with the edge.

        :return: list of vertices of the edge
        :rtype: list[Vertex]
        """
        pass

    @abstractmethod
    def getCenter(self) -> tuple[float, float]:
        """
        Get the coordinates of the center of the edge.

        :return: coordinates of the center of the edge
        :rtype: tuple[float, float]
        """
        pass

    @abstractmethod
    def getLength(self) -> float:
        """Get the length of the edge.

        :return: length of the edge
        :rtype: float
        """
        pass

    @abstractmethod
    def getCells(self) -> list[Cell]:
        """
        Get the list of cells associated with the edge.

        :return: list of cells associated with the edge
        :rtype: list[Cell]
        """
        pass

    @abstractmethod
    def getNormalVector(self) -> tuple[float, float]:
        """
        Get the normal vector of the edge.

        :return: coordinates of the normal vector to the edge  (from cell 1 to cell 2).
        :rtype: tuple[float, float]
        """
        pass

    @abstractmethod
    def getFluxDirectionVector(self) -> tuple[float, float]:
        """
        Get the vector connecting the centroids of the two cells adjacent to the edge.
        This vector goes from left cell center to right cell center

        :return:  coordinates of vector connecting the centroids of the two cells adjacent to the edge (from cell 1 to cell 2).
        :rtype: tuple[float, float]
        """
        pass

    @abstractmethod
    def getVectorToCellCenter(self, cell: Cell) -> tuple[float, float]:
        """
        Get the vector from the edge to the centroid of a specified cell.

        :param cell: Cell to which the vector is directed.
        :return: coordinates of the vector from the edge to the centroid of the specified cell.
        :rtype: tuple[float, float]
        """
        pass

    @abstractmethod
    def isBoundary(self) -> bool:
        """
        Check if the edge is on the boundary.

        :return: Edge at this boundary
        :rtype: Edge
        """
        pass


class BoundaryType(Enum):
    INFLOW = "inflow"
    OUTFLOW = "outflow"
    WALL = "wall"


class Boundary(ABC):
    """
    Concept of a boundary, it includes the boundary edge and a type.
    From this class you can get all needed information about boundaries
    """

    @abstractmethod
    def getEdge(self) -> Edge:
        """
        Get the edge positioned at this boundary of the mesh

        :return: True if the edge is on the boundary, False otherwise
        :rtype: bool
        """
        pass

    @abstractmethod
    def getType(self) -> BoundaryType:
        """
        Get the associated type of that boundary

        :return: Type of boundary
        :rtype: BoundaryType
        """
        pass


from typing import NamedTuple

class RawVertex(NamedTuple):
    """Represents a vertex with an id and 2D coordinates."""
    id: int
    x_coord: float
    y_coord: float


class RawCell(NamedTuple):
    """Represents a cell with an id and it's connected nodes"""
    id: int
    node1: int
    node2: int
    node3: int
    node4: int


class Mesh(ABC):
    """
    Represent a geometric mesh, defining the simulation space
    """

    @staticmethod
    @abstractmethod
    def createFromPartialInformation(
        rawVertices: list[RawVertex], rawCells: list[RawCell],
        inlet = list[int], outlet = list[int]
    ) -> 'Mesh':
        """
        Create a mesh from raw informations

        :return: Associated completed mesh
        :rtype: Mesh
        """
        pass

    @abstractmethod
    def getSurface(self) -> float:
        """
        Get the total surface area of the mesh.

        :return: Total surface area.
        :rtype: float
        """
        pass

    @abstractmethod
    def getVertexNumber(self) -> int:
        """
        Get the number of vertices in the mesh.

        :return: Number of vertices
        :rtype: int
        """
        pass

    @abstractmethod
    def getVertices(self) -> list[Vertex]:
        """
        Get the list of all vertices in the mesh.

        :return: List of vertices
        :rtype: list[Node]
        """
        pass

    @abstractmethod
    def getEdgeNumber(self) -> int:
        """
        Get the number of edges in the mesh.

        :return: Number of edges.
        :rtype: int
        """
        pass

    @abstractmethod
    def getEdges(self) -> list[Edge]:
        """
        Get the list of edges in the mesh.

        :return: List of edges.
        :rtype: list[Edge]
        """
        pass

    @abstractmethod
    def getCellNumber(self) -> int:
        """
        Get the number of cells in the mesh.

        :return: Number of cells.
        :rtype: int
        """
        pass

    @abstractmethod
    def getCells(self) -> list[Cell]:
        """
        Get the list of cells in the mesh.

        :return: List of cells.
        :rtype: list[Cell]
        """
        pass

    @abstractmethod
    def getBoundaryNumber(self) -> int:
        """
        Get the number of boundaries associated with edges in the mesh.

        :return: Number of boundary.
        :rtype: int
        """
        pass

    @abstractmethod
    def getBoundaries(self) -> list[Boundary]:
        """
        Get the list of boundaries associated with edges in the mesh.

        :return: List of boundaries
        :rtype: list[Boundary]
        """
        pass
