from fr.dasshydro.dassflow2d_py.mesh.Mesh import *

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

import math

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

    def  getEdges(self) -> list[Edge]:
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

    def __init__(self, cell: Cell):
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


def _get_normal_vector(a: tuple[float, float], b: tuple[float, float], p: tuple[float, float]):
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
    # normalize
    magnitude = math.sqrt(normal_vector[0]**2 + normal_vector[1]**2)
    if magnitude == 0:
        return (0, 0)  # Avoid division by zero
    normal_vector = (normal_vector[0] / magnitude, normal_vector[1] / magnitude)
    return normal_vector


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
        self.normalVector = _get_normal_vector(vertices[0].getCoordinates(), vertices[1].getCoordinates(), cells[0].getGravityCenter())

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

    def setType(self, boundaryType: BoundaryType):
        self.type = boundaryType


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
        rawVertices: list[RawVertex],
        rawCells: list[RawCell],
        inlets: list[RawInlet],
        outlets: list[RawOutlet]
        ) -> Mesh:
        # Step 1: Create a dictionary to map vertex IDs to vertex objects
        vertices_dict = {
            v.id: VertexImpl(v.id, (v.x_coord, v.y_coord), False)
            for v in rawVertices
        }

        # Step 2: Create cells
        cells: list[Cell] = []
        for raw_cell in rawCells:
            # Get the vertices for this cell using their IDs
            cell_vertices = set()
            cell_vertices.add(vertices_dict[raw_cell.vertex1])
            cell_vertices.add(vertices_dict[raw_cell.vertex2])
            cell_vertices.add(vertices_dict[raw_cell.vertex3])
            cell_vertices.add(vertices_dict[raw_cell.vertex4])
            # Create the cell
            cell = CellImpl(
                id=raw_cell.id,
                vertices=list(cell_vertices),
                edges=[],  # Will be populated later
                neighbors=[],  # Will be populated later
                isBoundary=False,
                isGhost=False,
            )
            cells.append(cell)

        # Step 3: Compute connectivity and create edges
        edges: list[Edge] = []
        edge_id = 1
        edge_map: dict[tuple[int, int], EdgeImpl] = {}  # To avoid duplicate edges

        for cell in cells:
            # get all possible vertices combinations among cell's vertices
            possible_edges = []
            for i in range(cell.getVerticesNumber()):
                for j in range(i+1, cell.getVerticesNumber()):
                    vertex1 = cell.getVertices()[i]
                    vertex2 = cell.getVertices()[j]
                    possible_edges.append((vertex1.getID(), vertex2.getID()))
            # create edges
            for possible_edge in possible_edges:
                edge_key = tuple(sorted(possible_edge))
                if edge_key not in edge_map:
                    # create incomplete edge object
                    edge = EdgeImpl(
                        id=edge_id,
                        vertices=(vertices_dict[possible_edge[0]], vertices_dict[possible_edge[1]]),
                        # second cell will be set later if possible, either another cell or ghost cell
                        cells=(cell, cell),
                        # boundary by default, this will be set to False later if there is another cell connected to it
                        isBoundary=True
                    )
                    edges.append(edge)
                    edge_id += 1
                    edge_map[edge_key] = edge
                else:
                    # update edge's cells
                    edge = edge_map[edge_key]
                    edge.setCells((edge.getCells()[0], cell)) # change second cell for current cell
                    edge.boundary = False

        # Step 4: Create boundaries
        boundaries: list[Boundary] = []
        for edge in edges:
            if edge.isBoundary():
                boundary = BoundaryImpl(edge, BoundaryType.WALL)  # Default type
                boundaries.append(boundary)
                # create ghost cell
                real_cell = edge.getCells()[0]
                real_cell.setBoundary(True)
                ghost_cell = GhostCell(real_cell)
                edge.setCells((edge.getCells()[0], ghost_cell))
        
        # Step 5: Update boundary vertices
        for boundary in boundaries:
            target_edge = boundary.getEdge()
            edge_vertices = target_edge.getVertices()
            for vertex in edge_vertices:
                vertex.setBoundary(True)


        # Step 5: Update cell edges
        for edge in edges:
            edge_cells = edge.getCells()
            for cell in edge_cells:
                if not cell.isGhost():
                    cell.getEdges().append(edge)

        # Step 6: Process INLET and OUTLET
        cells_dict = {cell.getID(): cell for cell in cells}
        boundary_edge_dict = {boundary.getEdge(): boundary for boundary in boundaries}
        # INLET
        for raw_inlet in inlets:
            target_cell = cells_dict[raw_inlet.cell]
            edge_index = raw_inlet.edge-1
            target_edge = target_cell.getEdges()[edge_index]
            target_boundary = boundary_edge_dict.get(target_edge)
            if target_boundary is None:
                print("Warning: target edge of an inflow is not a boundary edge")
            else:
                target_boundary.setType(BoundaryType.INFLOW)
        # OUTLET
        for raw_outlet in outlets:
            target_cell = cells_dict[raw_outlet.cell]
            edge_index = raw_outlet.edge-1
            target_edge = target_cell.getEdges()[edge_index]
            target_boundary = boundary_edge_dict.get(target_edge)
            if target_boundary is None:
                print("Warning: target edge of an outflow is not a boundary edge")
            else:
                target_boundary.setType(BoundaryType.OUTFLOW)
        
        # Step 7: Add neighbors
        for cell in cells:
            for cell_edge in cell.getEdges():
                edge_cell1, edge_cell2 = cell_edge.getCells()
                other_cell = edge_cell1 if edge_cell2 == cell else edge_cell2
                cell.getNeighbors().append(other_cell)

        mesh = MeshImpl(vertices=list(vertices_dict.values()), edges=edges, cells=cells, boundaries=boundaries)
        return mesh

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

if __name__ == "__main__":
    import os
    with open(os.path.join('testmesh.geo'), "r") as f:
        from fr.dasshydro.dassflow2d_py.input.DassflowMeshReader import DassflowMeshReader
        mesh_reader = DassflowMeshReader()
        raw_vertices, raw_cells, raw_inlets, raw_outlets = mesh_reader.read(os.path.join('testmesh.geo'))
        mesh = MeshImpl.createFromPartialInformation(raw_vertices, raw_cells, raw_inlets, raw_outlets)