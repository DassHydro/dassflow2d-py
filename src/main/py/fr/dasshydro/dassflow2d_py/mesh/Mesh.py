from enum import Enum

class MeshShape(Enum):
    TRIANGULAR = "triangular"
    QUADRILATERAL = "quadrilateral"
    HYBRID = "hybrid"


class MeshType(Enum):
    BASIC = "basic"
    DASSFLOW = "dassflow"


from abc import ABC, abstractmethod
from typing import Iterable

class Vertex(ABC):

    @abstractmethod
    def getID(self) -> int:
        """
        Get the id of the vertex

        Returns:
            int: id of the vertex
        """
        pass

    @abstractmethod
    def getCoordinates(self) -> tuple[float, float]:
        """
        Get the coordinates of the vertex.

        Returns:
            tuple[float, float]: coordinates of the vertex
        """
        pass

    @abstractmethod
    def isBoundary(self) -> bool:
        """
        Check if the vertex is on the boundary.

        Returns:
            bool: True if the vertex is on the boundary, False otherwise
        """
        pass


class Cell(ABC):

    @abstractmethod
    def getID(self) -> int:
        """
        Get the id of the cell

        Returns:
            int: id of the cell
        """
        pass

    @abstractmethod
    def getSurface(self) -> float:
        """
        Get the surface area of the cell

        Returns:
            float: surface area of the cell
        """
        pass

    @abstractmethod
    def getPerimeter(self) -> float:
        """
        Get the perimeter of the cell

        Returns:
            float: perimeter of the cell
        """
        pass

    @abstractmethod
    def getVertices(self) -> Iterable[Vertex]:
        """
        Get the list of the cell's vertices

        Returns:
            Iterable[Vertex]: list of vertices of the cell
        """
        pass

    @abstractmethod
    def getVerticesNumber(self) -> int:
        """
        Get the number of vertices that this cell have.
        It allows to know cell geometry (triangle, quadrilateral ...)

        Returns:
            int: number of vertices in the cell
        """
        pass

    @abstractmethod
    def  getEdges(self) -> Iterable['Edge']:
        """
        Get the list of the cell's edges

        Returns:
            Iterable[Edge]: list of edges of the cell
        """
        pass

    @abstractmethod
    def getNeighbors(self) -> Iterable['Cell']:
        """
        Get all neighboring cells

        Returns:
            Iterable[Cell]: list of neighboring cells
        """
        pass

    @abstractmethod
    def getGravityCenter(self) -> tuple[float, float]:
        """
        Get the cell's gravity center coordinates

        Returns:
            tuple[float,float]: centre of gravity of the cell
        """
        pass

    @abstractmethod
    def isBoundary(self) -> bool:
        """
        Tells if the cell is at mesh boundary

        Returns:
            bool: True if the cell is on the boundary, False otherwise
        """
        pass

    @abstractmethod
    def isGhost(self) -> bool:
        """
        Tells if the cell represent a ghost cell

        Returns:
            bool: True if the cell is a ghost cell, False otherwise
        """
        pass


class Edge(ABC):

    @abstractmethod
    def getID(self) -> int:
        """
        Get the id of the edge

        Returns:
            int: id of the edge
        """
        pass

    @abstractmethod
    def getVertices(self) -> tuple[Vertex, Vertex]:
        """
        Get the two vertices associated with the edge.

        Returns:
            tuple[Vertex,Vertex]: tuple of the two vertices of the edge
        """
        pass

    @abstractmethod
    def getCenter(self) -> tuple[float, float]:
        """
        Get the coordinates of the center of the edge.

        Returns:
            tuple[float,float]: coordinates of the center of the edge
        """
        pass

    @abstractmethod
    def getLength(self) -> float:
        """
        Get the length of the edge.

        Returns:
            float: length of the edge
        """
        pass

    @abstractmethod
    def getCells(self) -> tuple[Cell, Cell]:
        """
        Get the two cells associated with the edge.

        Returns:
            tuple[Cell,Cell]: tuple of the two cells associated with the edge
        """
        pass

    @abstractmethod
    def getNormalVector(self) -> tuple[float, float]:
        """
        Get the normal vector of the edge.

        Returns:
            tuple[float,float]: coordinates of the normal vector to the edge  (from cell 1 to cell 2).
        """
        pass

    @abstractmethod
    def getFluxDirectionVector(self) -> tuple[float, float]:
        """
        Get the vector connecting the centroids of the two cells adjacent to the edge.
        This vector goes from left cell center to right cell center

        Returns:
            tuple[float,float]: coordinates of vector connecting the centroids of the
            two cells adjacent to the edge (from cell 1 to cell 2).
        """
        pass

    @abstractmethod
    def getVectorToCellCenter(self, cell: Cell) -> tuple[float, float]:
        """
        Get the vector from the edge to the centroid of a specified cell.

        Args:
            cell (Cell): Cell to which the vector is directed.

        Returns:
            tuple[float,float]: coordinates of the vector from the edge to the centroid of the specified cell.
        """
        pass

    @abstractmethod
    def isBoundary(self) -> bool:
        """
        Check if the edge is on the boundary.

        Returns:
            bool: wether or not the edge is at the mesh boundary
        """
        pass

    def getGhostCell(self) -> Cell:
        """
        Shortcut function to get the ghost assuming the edge is a boundary edge

        Returns:
            Cell: the ghost cell if the edge is boundary, the second cell otherwise
        """
        return self.getCells()[1]


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

        Returns:
            Edge: target edge of the boundary object
        """
        pass

    @abstractmethod
    def getType(self) -> BoundaryType:
        """
        Get the associated type of that boundary

        Returns:
            BoundaryType: simple boundary type
        """
        pass


from typing import NamedTuple

class RawVertex(NamedTuple):
    """Represents a vertex with an id and 2D coordinates."""
    id: int
    x_coord: float
    y_coord: float


class RawCell(NamedTuple):
    """Represents a cell with an id and it's connected vertices"""
    id: int
    vertex1: int
    vertex2: int
    vertex3: int
    vertex4: int


class RawInlet(NamedTuple):
    """Represents an inlet boundary"""
    cell: int # target cell
    edge: int # target edge
    boundary_type: int # deprecated boundary type number
    ghost_cell_bed_elevation: float # bathymetry value of the ghost cell
    group_number: int # group number to which the inlet belongs

class RawOutlet(NamedTuple):
    """Represents an outlet boundary"""
    cell: int # target cell
    edge: int # target edge
    boundary_type: int # deprecated boundary type number
    ghost_cell_bed_elevation: float # bathymetry value of the ghost cell
    group_number: int # group number to which the outlet belongs


class Mesh(ABC):
    """
    Represent a geometric mesh, defining the simulation space
    """

    @staticmethod
    @abstractmethod
    def createFromPartialInformation(
        rawVertices: Iterable[RawVertex],
        rawCells: Iterable[RawCell],
        inlet: Iterable[RawInlet],
        outlet: Iterable[RawOutlet],
        out_boundary_origin: dict[Boundary, RawInlet|RawOutlet]
    ) -> 'Mesh':
        """
        Create a mesh from raw information.

        Args:
            rawVertices (Iterable[RawVertex]): All vertices of the mesh in raw format.
            rawCells (Iterable[RawCell]): All cells of the mesh in raw format.
            inlet (Iterable[RawInlet]): All inlet boundaries of the mesh in raw format.
            outlet (Iterable[RawOutlet]): All outlet boundaries of the mesh in raw format.
            out_boundaries association (dict[Boundary, RawInlet|RawOutlet]): Empty dictionary that will be populated
                with boundaries associations.

        Returns:
            Mesh: Complete mesh with all parameters included in it.
        """
        pass

    @abstractmethod
    def getSurface(self) -> float:
        """
        Get the total surface area of the mesh.

        Returns:
            float: total mesh surface
        """
        pass

    @abstractmethod
    def getVertexNumber(self) -> int:
        """
        Get the number of vertices in the mesh.

        Returns:
            int: number if vertices in the mesh
        """
        pass

    @abstractmethod
    def getVertices(self) -> Iterable[Vertex]:
        """
        Get the list of all vertices in the mesh.

        Returns:
            Iterable[Vertex]: all vertices in the mesh
        """
        pass

    @abstractmethod
    def getEdgeNumber(self) -> int:
        """
        Get the number of edges in the mesh.

        Returns:
            int: number of edges in the mesh
        """
        pass

    @abstractmethod
    def getEdges(self) -> Iterable[Edge]:
        """
        Get the list of edges in the mesh.

        Returns:
            Iterable[Edge]: all edges in the mesh
        """
        pass

    @abstractmethod
    def getCellNumber(self) -> int:
        """
        Get the number of cells in the mesh.

        Returns:
            int: number of cells in the mesh
        """
        pass

    @abstractmethod
    def getCells(self) -> Iterable[Cell]:
        """
        Get the list of cells in the mesh.

        Returns:
            Iterable[Cell]: all cells in the mesh
        """
        pass

    @abstractmethod
    def getBoundaryNumber(self) -> int:
        """
        Get the number of boundaries associated with edges in the mesh.

        Returns:
            int: number of boundaries in the mesh
        """
        pass

    @abstractmethod
    def getBoundaries(self) -> Iterable[Boundary]:
        """
        Get the list of boundaries associated with edges in the mesh.

        Returns:
            Iterable[Boundary]: all boundaries of the mesh
        """
        pass
