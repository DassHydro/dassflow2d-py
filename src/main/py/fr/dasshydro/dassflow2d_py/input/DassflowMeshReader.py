from fr.dasshydro.dassflow2d_py.input.MeshReader import MeshReader

def _read_next(file, ignore_predicate):
    line = file.readline()
    while ignore_predicate(line):
        line = file.readline()
    return line

def _read_until_info(file) -> str:
    def ignore_line(line: str):
        # Strip whitespace from the string
        stripped_line = line.strip()
        # Check if the string is empty or a comment
        return not stripped_line or stripped_line.startswith('#')
    return _read_next(file, ignore_line)


class DassflowMeshReader(MeshReader):

    def __init__(self):
        pass

    def read(self, file_path):
        raw_vertices = []
        raw_cells = []
        inlet = []
        outlet = []

        with open(file_path, 'r') as f:
            header_line = _read_until_info(f)
            parts = header_line.split()
            vertex_number, cell_number, _ = int(parts[0]), int(parts[1]), float(parts[2])
            # Read vertices
            for _ in range(vertex_number):
                vertex_line = _read_until_info(f).strip()
                parts = vertex_line.split()
                vertex_id = int(parts[0])
                x_coord = float(parts[1])
                y_coord = float(parts[2])
                raw_vertices.append((vertex_id, x_coord, y_coord))

            # Read cells
            for _ in range(cell_number):
                cell_line = _read_until_info(f).strip()
                parts = cell_line.split()
                cell_id = int(parts[0])
                node1 = int(parts[1])
                node2 = int(parts[2])
                node3 = int(parts[3])
                node4 = int(parts[4]) if len(parts) > 4 and parts[4] != '0' else node1  # Handle triangular cells
                raw_cells.append((cell_id, node1, node2, node3, node4))

            # Read boundaries
            inlet_header_line = _read_until_info(f).strip()
            inlet_count = int(inlet_header_line.split()[1])
            for _ in range(inlet_count):
                inlet_line = _read_until_info(f).strip()
                parts = inlet_line.split()
                cell_id = int(parts[0])
                _ = int(parts[1])
                _ = int(parts[2])
                _ = int(parts[3])
                _ = int(parts[4])
                inlet.append(cell_id)
            
            outlet_header_line = _read_until_info(f).strip()
            outlet_count = int(outlet_header_line.split()[1])
            for _ in range(outlet_count):
                line = _read_until_info(f).strip()
                parts = line.split()
                cell_id = int(parts[0])
                _ = int(parts[1])
                _ = int(parts[2])
                _ = int(parts[3])
                _ = int(parts[4])
                outlet.append(cell_id)

        return raw_vertices, raw_cells, inlet, outlet
