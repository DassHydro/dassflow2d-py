from fr.dasshydro.dassflow2d_py.mesh.Mesh import *
import math
from typing import cast, Iterable


# --- Global Helper Functions ---

def _gauss_area_formula(vertices: list[tuple[float, float]]):
    """
    Also known as the shoelace formula, this function calculate
    the area of a 2D polygon given its vertices.

    Args:
        vertices: List of tuples [(x1, y1), (x2, y2), ..., (xn, yn)]

    Returns:
        Area of the polygon as a float.
    """
    n = len(vertices)
    area = 0.0
    for i in range(n):
        x_i, y_i = vertices[i]
        x_j, y_j = vertices[(i + 1) % n]
        area += (x_i * y_j) - (x_j * y_i)
    return abs(area) / 2.0

def _polygon_perimeter(vertices):
    """
    Calculate the perimeter of a 2D polygon given its vertices.

    Args:
        vertices: List of tuples [(x1, y1), (x2, y2), ..., (xn, yn)]

    Returns:
        Perimeter of the polygon as a float.
    """
    n = len(vertices)
    perimeter = 0.0
    for i in range(n):
        x_i, y_i = vertices[i]
        x_j, y_j = vertices[(i + 1) % n]
        perimeter += math.sqrt((x_j - x_i)**2 + (y_j - y_i)**2)
    return perimeter

def _polygon_center(vertices):
    """
    Calculate the center of a 2D polygon given its vertices.

    Args:
        vertices: List of tuples [(x1, y1), (x2, y2), ..., (xn, yn)]

    Returns:
        Center of the polygon as a tuple of floats.
    """
    return (
        sum(x for x, _ in vertices) / len(vertices),
        sum(y for _, y in vertices) / len(vertices)
    )


class VertexImpl(Vertex):

    def __init__(self, id: int, coordinates: tuple[float, float], isBoundary: bool):
        self.id = id
        self.coordinates = coordinates
        self.boundary = isBoundary

    def getID(self) -> int:
        return self.id

    def getCoordinates(self) -> tuple[float, float]:
        return self.coordinates

    def isBoundary(self) -> bool:
        return self.boundary

    def setBoundary(self, isBoundary: bool):
        self.boundary = isBoundary


class CellImpl(Cell):

    def __init__(self, id: int, vertices: list[Vertex], edges: list[Edge], neighbors: list[Cell],
                 isBoundary: bool, isGhost: bool):
        self.id = id
        self.vertices = vertices
        self.edges = edges
        self.neighbors = neighbors
        self.boundary = isBoundary
        self.ghost = isGhost

        self.verticesNumber = len(vertices)
        
        # map from a list of vertices to a list of there coordinates
        list_of_coordinates = [vertex.getCoordinates() for vertex in vertices]
        self.center = _polygon_center(list_of_coordinates)
        self.surface = _gauss_area_formula(list_of_coordinates)
        self.perimeter = _polygon_perimeter(list_of_coordinates)

    def getID(self) -> int:
        return self.id

    def getSurface(self) -> float:
        return self.surface

    def getPerimeter(self) -> float:
        return self.perimeter

    def getVertices(self) -> list[Vertex]:
        return self.vertices

    def getVerticesNumber(self) -> int:
        return self.verticesNumber

    def getEdges(self) -> list[Edge]:
        return self.edges

    def getNeighbors(self) -> list[Cell]:
        return self.neighbors

    def getGravityCenter(self) -> tuple[float, float]:
        return self.center

    def isBoundary(self) -> bool:
        return self.boundary

    def setBoundary(self, isBoundary: bool):
        self.boundary = isBoundary

    def isGhost(self) -> bool:
        return self.ghost


class GhostCell(Cell):

    def __init__(self, cell: CellImpl):
        self.cell = cell

    def getID(self) -> int:
        return -1

    def getSurface(self) -> float:
        return self.cell.getID()

    def getPerimeter(self) -> float:
        return self.cell.getPerimeter()

    def getVertices(self) -> list[Vertex]:
        return self.cell.getVertices()

    def getVerticesNumber(self) -> int:
        return self.cell.getVerticesNumber()

    def  getEdges(self) -> list[Edge]:
        return self.cell.getEdges()

    def getNeighbors(self) -> list[Cell]:
        return self.cell.getNeighbors()

    def getGravityCenter(self) -> tuple[float, float]:
        return self.cell.getGravityCenter()

    def isBoundary(self) -> bool:
        return self.cell.isBoundary()

    def isGhost(self) -> bool:
        return True


class EdgeImpl(Edge):

    def __init__(self, id: int, vertices: tuple[Vertex, Vertex], cells: tuple[Cell, Cell], isBoundary: bool):
        self.id = id
        self.vertices = vertices
        self.setCells(cells)
        self.boundary = isBoundary

        tuple_of_coordinates = (vertices[0].getCoordinates(), vertices[1].getCoordinates())
        self.center = _polygon_center(tuple_of_coordinates)
        x_0, y_0 = tuple_of_coordinates[0]
        x_1, y_1 = tuple_of_coordinates[1]
        self.length = math.sqrt((x_1 - x_0)**2 + (y_1 - y_0)**2)
        self.normalVector = self._create_normal_vector(vertices[0].getCoordinates(), vertices[1].getCoordinates(), cells[0].getGravityCenter())
    
    # --- Private Methods ---

    def _create_normal_vector(
        self,
        a: tuple[float, float],
        b: tuple[float, float],
        p: tuple[float, float]
    ) -> tuple[float, float]:
        """
        Creates a 2D vector representing the normal vector of the current edge.
        The edge normal vector is defined as the normal vector that faces away from the first cell in 'Edge#getCells()'

        Args:
            a (tuple[float, float]): one vertex of the edge
            b (tuple[float, float]): other vertex of the edge
            p (tuple[float, float]): a point in the cell to avoid

        Raises:
            ValueError: if p is colinear with a and b

        Returns:
            tuple[float, float]: the normal vector of the edge
        """
        cross = (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])
        if cross == 0:
            raise ValueError("p cannot be collinear with segment AB")
        isLeft = cross > 0
        normal_vector = (b[0] - a[0], b[1] - a[1])
        if isLeft:
            # turn AB vector to the right
            normal_vector = (normal_vector[1], -normal_vector[0])
        else:
            # so it's right
            # turn AB vector to the left
            normal_vector = (-normal_vector[1], normal_vector[0])
        # normalizing step
        magnitude = math.sqrt(normal_vector[0]**2 + normal_vector[1]**2)
        if magnitude == 0:
            return (0, 0)  # Avoid division by zero
        normal_vector = (normal_vector[0] / magnitude, normal_vector[1] / magnitude)
        return normal_vector

    # --- End of Private ---

    def getID(self) -> int:
        return self.id

    def getVertices(self) -> tuple[Vertex, Vertex]:
        return self.vertices

    def getCenter(self) -> tuple[float, float]:
        return self.center

    def getLength(self) -> float:
        return self.length

    def getCells(self) -> tuple[Cell, Cell]:
        return self.cells

    def setCells(self, cells: tuple[Cell, Cell]):
        self.cells = cells
        self.fluxDirectionVector = (
            cells[1].getGravityCenter()[0] - cells[0].getGravityCenter()[0],
            cells[1].getGravityCenter()[1] - cells[0].getGravityCenter()[1]
        )

    def getNormalVector(self) -> tuple[float, float]:
        return self.normalVector

    def getFluxDirectionVector(self) -> tuple[float, float]:
        assert self.cells[0] != self.cells[1]
        return self.fluxDirectionVector

    def getVectorToCellCenter(self, cell: Cell) -> tuple[float, float]:
        return (cell.getGravityCenter()[0] - self.center[0], cell.getGravityCenter()[1] - self.center[1])

    def isBoundary(self) -> bool:
        return self.boundary

    def setBoundary(self, isBoundary):
        self.boundary = isBoundary


class BoundaryImpl(Boundary):
    """
    Concept of a boundary, it includes the boundary edge and a type.
    From this class you can get all needed information about boundaries
    """

    def __init__(self, edge: Edge, type: BoundaryType):
        self.edge = edge
        self.type = type

    def getEdge(self) -> Edge:
        return self.edge

    def getType(self) -> BoundaryType:
        return self.type

    def setType(self, boundaryType):
        self.type = boundaryType


# --- Mesh Helper Functions ---

def _create_partial_vertices_dict(rawVertices: Iterable[RawVertex]) -> dict[int, Vertex]:
    """
    Creates a dictionary mapping vertex IDs to partial Vertex objects.
    Created Vertices are partial as they lack coherence on the 'isBoundary' method

    Args:
        rawVertices: List of raw vertex data.

    Returns:
        A dictionary mapping vertex IDs to Vertex objects.
    """
    return {
        v.id: VertexImpl(v.id, (v.x_coord, v.y_coord), False)
        for v in rawVertices
    }


def _create_partial_cells(rawCells: Iterable[RawCell], vertices_dict: dict[int, Vertex]) -> list[Cell]:
    """
    Creates a list of partial Cell objects from raw cell data.
    Created Cells are partial as they lack coherence on 'getEdges', 'getNeighbors', and 'isBoundary' methods

    Args:
        rawCells: List of raw cell data.
        vertices_dict: Dictionary mapping vertex IDs to Vertex objects.

    Returns:
        A list of Cell objects.
    """
    cells: list[Cell] = []

    for raw_cell in rawCells:
        
        # build cell's vertices list
        cell_vertices: list[Vertex] = [
            vertices_dict[raw_cell.vertex1],
            vertices_dict[raw_cell.vertex2],
            vertices_dict[raw_cell.vertex3],
        ]
        # _ don't add fourth element if it comply with at least one method of nullification
        # i.e. that means that the fourth vertex don't represent a vertex but the end of the vertices list
        # in the case of a triangular cell
        if raw_cell.vertex4 != 0 and (raw_cell.vertex1 != raw_cell.vertex4):
            cell_vertices.append(vertices_dict[raw_cell.vertex4])

        cell = CellImpl(
            id=raw_cell.id,
            vertices=cell_vertices,
            edges=[],                 # non-coherent (populated later)
            neighbors=[],             # non-coherent (populated later)
            isBoundary=False,         # non-coherent (corrected later)
            isGhost=False,
        )
        cells.append(cell)

    return cells


def _create_partial_edges(cells: list[Cell], vertices_dict: dict[int, Vertex]) -> list[Edge]:
    """
    Creates a list of partial Edge objects from cell and vertex informations.
    Created Edges are partial as they lack coherence on the 'getCells' method

    Args:
        cells: List of Cell objects.
        vertices_dict: Dictionary mapping vertex IDs to Vertex objects.

    Returns:
        A list of Edge objects.
    """
    edges: list[Edge] = []
    # counter to assign different IDs to each edge
    edge_id = 1
    # keeps track of what tuple of int*int already exists as an partial Edge object (avoid edge duplication)
    edge_map = {}

    for cell in cells:

        # build array of possible tuple of vertex IDs that can lead to an edge
        possible_edges = []
        for i in range(cell.getVerticesNumber()):
            for j in range(i + 1, cell.getVerticesNumber()):
                cell = cast(CellImpl, cell)
                vertex1 = cell.getVertices()[i]
                vertex2 = cell.getVertices()[j]
                possible_edges.append((vertex1.getID(), vertex2.getID()))

        for possible_edge in possible_edges:

            edge_key = tuple(sorted(possible_edge))
            
            # verify if this tuple of vertex IDs already led to the creation of a partial Edge object
            if edge_key not in edge_map:

                # if not, create it
                edge = EdgeImpl(
                    id=edge_id,
                    vertices=(vertices_dict[possible_edge[0]], vertices_dict[possible_edge[1]]),
                    cells=(cell, cell),
                    isBoundary=True,
                )
                edges.append(edge)
                edge_id += 1
                # and update the dictionary to not create it again
                edge_map[edge_key] = edge

            else:

                # if not, that means that this edge is the connection between two cells
                edge = edge_map[edge_key]
                edge.setCells((edge.getCells()[0], cell))
                edge.setBoundary(False)

    return edges


def _create_boundaries(edges: list[Edge]) -> list[Boundary]:
    """
    Creates boundaries for boundary edges and resolve coherence around target edge

    Args:
        edges: List of Edge objects.

    Returns:
        A list of Boundary objects.
    """
    boundaries: list[Boundary] = []

    for edge in edges:

        if edge.isBoundary():

            edge = cast(EdgeImpl, edge)
            # Create boundary object
            boundary = BoundaryImpl(edge, BoundaryType.WALL)
            boundaries.append(boundary)
            # Make boundary surround objects coherent
            # _ boundary flags
            real_cell = edge.getCells()[0]
            real_cell = cast(CellImpl, real_cell)
            real_cell.setBoundary(True)

            for edge_vertex in edge.getVertices():

                edge_vertex = cast(VertexImpl, edge_vertex)
                edge_vertex.setBoundary(True)

            # _ ghost cell
            ghost_cell = GhostCell(real_cell)
            edge.setCells((edge.getCells()[0], ghost_cell))

    return boundaries


def _add_cell_edges(edges: list[Edge]):
    """
    Adds the edges of each cell.

    Args:
        edges: List of Edge objects.
    """

    for edge in edges:

        for cell in edge.getCells():

            if not cell.isGhost():

                cell = cast(CellImpl, cell)
                cell.getEdges().append(edge)


def _add_neighbors_to_cells(cells: list[Cell]):
    """
    Adds neighboring cells to each cell.

    Args:
        cells: List of Cell objects.
    """

    for cell in cells:
        # for each cells, explore their neighbors using edges

        cell = cast(CellImpl, cell)

        for cell_edge in cell.getEdges():

            edge_cell1, edge_cell2 = cell_edge.getCells()
            assert edge_cell1 != edge_cell2 # assume that edges are coherent on 'getCells' method
            other_cell = edge_cell1 if edge_cell2 == cell else edge_cell2
            cell.getNeighbors().append(other_cell)


def _process_inlets_and_outlets(
    cells: list[Cell],
    boundaries: list[Boundary],
    inlets: Iterable[RawInlet],
    outlets: Iterable[RawOutlet]
):
    """
    Processes inlets and outlets, setting correct boundary type to corresponding Boundary object.
    This function uses a naive approach to resolve target edge from inlet/outlet raw informations.
    This approach don't guarantee landing on the good edge and make tests unreliable on this information.
    This issue should be investigated, Issue N°: #10

    Args:
        cells: List of Cell objects.
        boundaries: List of Boundary objects.
        inlets: List of RawInlet objects.
        outlets: List of RawOutlet objects.
    """
    # allows to search for a Cell object using it's ID
    cells_dict = {cell.getID(): cell for cell in cells}
    # allow to search for a Boundary object using it's target edge
    boundary_edge_dict: dict[Edge, Boundary] = {boundary.getEdge(): boundary for boundary in boundaries}

    # function to process generic raw inlet/outlet
    def process_boundary_update(boundary_list, type_to_set: BoundaryType):

        for raw_boundary in boundary_list:

            target_cell = cells_dict[raw_boundary.cell]
            # casting to use 'getEdges' method as returning a list (indexable) instead of an Iterable
            target_cell = cast(CellImpl, target_cell) 
            edge_index = raw_boundary.edge - 1 # because mesh.geo is 1-based, not 0-based
            target_edge = target_cell.getEdges()[edge_index]
            # this can fail as resolving target edge using index in Cell#getEdges() is a naive approach
            target_boundary = boundary_edge_dict.get(target_edge)
            
            if target_boundary is None:

                # this print should be replaced with a proper logging method
                print(f"Warning: Target edge of inlet {raw_boundary.cell} is not a boundary edge.")

            else:

                # casting to use 'setType' method
                target_boundary = cast(BoundaryImpl, target_boundary)
                target_boundary.setType(type_to_set)

    # process inlets
    process_boundary_update(inlets, BoundaryType.INFLOW)
    # process outlets
    process_boundary_update(outlets, BoundaryType.OUTFLOW)


class MeshImpl(Mesh):
    """
    Represent a geometric mesh, defining the simulation space
    """

    def __init__(self, vertices: list[Vertex], edges: list[Edge], cells: list[Cell], boundaries: list[Boundary]):
        self.verticesNumber = len(vertices)
        self.vertices = vertices
        self.edgesNumber = len(edges)
        self.edges = edges
        self.cellsNumber = len(cells)
        self.cells = cells
        self.boundariesNumber = len(boundaries)
        self.boundaries = boundaries
        self.surface = sum(map(lambda c: c.getSurface(), cells))

    @staticmethod
    def createFromPartialInformation(
        rawVertices: Iterable[RawVertex],
        rawCells: Iterable[RawCell],
        inlets: Iterable[RawInlet],
        outlets: Iterable[RawOutlet]
    ) -> Mesh:
        """
        Creates a Mesh object from raw vertex, cell, inlet, and outlet data.

        Args:
            rawVertices: List of raw vertex data.
            rawCells: List of raw cell data.
            inlets: List of raw inlet data.
            outlets: List of raw outlet data.

        Returns:
            A fully constructed Mesh object.
        """
        vertices_dict = _create_partial_vertices_dict(rawVertices)
        cells = _create_partial_cells(rawCells, vertices_dict)
        edges = _create_partial_edges(cells, vertices_dict)
        boundaries = _create_boundaries(edges)
        _add_cell_edges(edges)
        _add_neighbors_to_cells(cells)
        _process_inlets_and_outlets(cells, boundaries, inlets, outlets)

        return MeshImpl(
            vertices=list(vertices_dict.values()),
            edges=edges,
            cells=cells,
            boundaries=boundaries,
        )

    def getSurface(self) -> float:
        return self.surface

    def getVertexNumber(self) -> int:
        return self.verticesNumber

    def getVertices(self) -> list[Vertex]:
        return self.vertices

    def getEdgeNumber(self) -> int:
        return self.edgesNumber

    def getEdges(self) -> list[Edge]:
        return self.edges

    def getCellNumber(self) -> int:
        return self.cellsNumber

    def getCells(self) -> list[Cell]:
        return self.cells

    def getBoundaryNumber(self) -> int:
        return self.boundariesNumber

    def getBoundaries(self) -> list[Boundary]:
        return self.boundaries
