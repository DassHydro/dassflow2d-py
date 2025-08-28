from typing import Callable
from io import TextIOWrapper
from fr.dasshydro.dassflow2d_py.input.MeshReader import MeshReader
from fr.dasshydro.dassflow2d_py.mesh.Mesh import RawVertex, RawCell, RawInlet, RawOutlet

def _read_next(file: TextIOWrapper, ignore_predicate: Callable[[str], bool]) -> str:
    """Reads the next line in the file that don't match the ignore predicate

    Args:
        file (TextIOWrapper): file to read from
        ignore_predicate (Callable[[str], bool]): predicate on strings that indicate if the line should be ignored
    Returns:
        str: next line that don't match predicate
    """
    line = file.readline()
    while ignore_predicate(line):
        line = file.readline()
    return line

def _next_line(file: TextIOWrapper) -> str:
    """Gets the next line of text in file ignoring whitespaces and comments

    Args:
        file (TextIOWrapper): file to read line from

    Returns:
        str: the next line in file that is not only whitespaces nor a comment
    """
    def ignore_line(line: str):
        # Strip whitespace from the string
        stripped_line = line.strip()
        # Check if the string is empty or a comment
        return not stripped_line or stripped_line.startswith('#')
    return _read_next(file, ignore_line)

def extract(file: TextIOWrapper, type_tuple: tuple) -> tuple:
    """Extract a number of variables from the next relevant line of a file

    Args:
        file (TextIOWrapper): file to extract relevant line from
        type_tuple (tuple): types of all extracted variables

    Returns:
        tuple: all extracted variables in a tuple
    """
    parts = _next_line(file).strip().split()
    return tuple(typ(part) for typ, part in zip(type_tuple, parts))



class DassflowMeshReader(MeshReader):
    """This class implements the reading of a mesh, on a dassflow mesh type
    """

    def __init__(self):
        pass

    def read(self, file_path: str):
        raw_vertices = []
        raw_cells = []
        inlet = []
        outlet = []

        with open(file_path, 'r') as f:
            # Reads mesh header
            vertex_number, cell_number, _ = extract(f, (int, int, float))

            # Reads all vertices
            for _ in range(vertex_number):
                vertex_id, x_coord, y_coord = extract(f, (int, float, float))
                raw_vertex = RawVertex(vertex_id, x_coord, y_coord)
                raw_vertices.append(raw_vertex)

            # Reads all cells
            for _ in range(cell_number):
                cell_id, vertex1, vertex2, vertex3, vertex4 = extract(f, (int, int, int, int, int))
                if vertex4 == 0:
                    # Handle triangular case
                    vertex4 = vertex1
                raw_cell = RawCell(cell_id, vertex1, vertex2, vertex3, vertex4)
                raw_cells.append(raw_cell)

            ### Boundaries
            # Reads inlet header
            _, inlet_number, _ = extract(f, (str, int, int))

            # Reads all inlets
            for _ in range(inlet_number):
                cell_id, edge_id, boundary_type, ghost_cell_bed_elevation = extract(f, (int, int, int, float))
                raw_inlet = RawInlet(cell_id, edge_id, boundary_type, ghost_cell_bed_elevation)
                inlet.append(raw_inlet)
            
            # Reads outlet header
            _, outlet_number, _ = extract(f, (str, int, int))

            #Reads all outlets
            for _ in range(outlet_number):
                cell_id, edge_id, boundary_type, ghost_cell_bed_elevation = extract(f, (int, int, int, float))
                raw_outlet = RawOutlet(cell_id, edge_id, boundary_type, ghost_cell_bed_elevation)
                outlet.append(raw_outlet)

        # Gather all lists and return as tuple
        return raw_vertices, raw_cells, inlet, outlet
