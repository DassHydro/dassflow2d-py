from fr.dasshydro.dassflow2d_py.input.file_reading import *
from fr.dasshydro.dassflow2d_py.input.MeshReader import MeshReader
from fr.dasshydro.dassflow2d_py.mesh.Mesh import RawVertex, RawCell, RawInlet, RawOutlet


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
        vertex_bathymetry = {}
        cell_bathymetry = {}

        with open(file_path, 'r') as f:
            # Reads mesh header
            vertex_number, cell_number, _ = extract(f, (int, int, float))

            # Reads all vertices
            for _ in range(vertex_number):
                vertex_id, x_coord, y_coord, bathymetry = extract(f, (int, float, float, float))
                raw_vertex = RawVertex(vertex_id, x_coord, y_coord)
                raw_vertices.append(raw_vertex)
                vertex_bathymetry[vertex_id] = bathymetry

            # Reads all cells
            for _ in range(cell_number):
                cell_id, vertex1, vertex2, vertex3, vertex4, _, bathymetry = extract(f, (int, int, int, int, int, float, float))
                if vertex4 == 0:
                    # Handle triangular case
                    vertex4 = vertex1
                raw_cell = RawCell(cell_id, vertex1, vertex2, vertex3, vertex4)
                raw_cells.append(raw_cell)
                cell_bathymetry[cell_id] = bathymetry

            ### Boundaries
            # Reads inlet header
            _, inlet_number, inlets_groups_number = extract(f, (str, int, int))

            # Reads all inlets
            for _ in range(inlet_number):
                inlet_line = next_line(f).strip()
                parts = inlet_line.split()

                # Parse mandatory fields
                cell_id, edge_id = map(int, parts[:2])
                ghost_cell_bed_elevation = float(parts[3])

                # Parse optional group_number
                group_number = int(parts[4]) if len(parts) > 4 else 1 # USE 1 as default group number for inlets

                raw_inlet = RawInlet(cell_id, edge_id, ghost_cell_bed_elevation, group_number)

                inlet.append(raw_inlet)

            # Reads outlet header
            _, outlet_number, _ = extract(f, (str, int, int))

            # Reads all outlets
            for _ in range(outlet_number):
                outlet_line = next_line(f).strip()
                parts = outlet_line.split()

                # Parse mandatory fields
                cell_id, edge_id = map(int, parts[:2])
                ghost_cell_bed_elevation = float(parts[3])

                # Parse optional group_number
                group_number = int(parts[4]) if len(parts) > 4 else inlets_groups_number # USE number of inlets groups

                raw_outlet = RawOutlet(cell_id, edge_id, ghost_cell_bed_elevation, group_number)
                outlet.append(raw_outlet)

        # Gather all lists and return as tuple
        return raw_vertices, raw_cells, inlet, outlet, vertex_bathymetry, cell_bathymetry
