import unittest
import os
import tempfile
from fr.dasshydro.dassflow2d_py.input.DassflowMeshReader import DassflowMeshReader
from fr.dasshydro.dassflow2d_py.mesh.Mesh import RawVertex, RawCell, RawInlet, RawOutlet

class TestDassflowMeshReader(unittest.TestCase):
    def setUp(self):
        # Create a temporary mesh file for testing
        self.test_mesh_content = """
            # mesh generated for testing DassflowMeshReader
            6 4 1.0
            #Vertex||| id vertex, x coord, y coord, bathymetry
            1 0.0 0.0 0.0
            2 1.0 0.0 0.0
            3 2.0 0.0 0.0
            4 0.0 1.0 0.0
            5 1.0 1.0 0.0
            6 2.0 1.0 0.0
            #cells||| id cell, id_vertex1, id_vertex2, id_vertex3, id_vertex4, patch_manning, bathymetry
            1 1 2 5 1 1 0.
            2 2 3 6 2 1 0.
            3 1 4 5 1 1 0.
            4 2 5 6 2 1 0.
            # boundaries
            INLET 1 1
            3 1 1 1 1
            OUTLET 1 1
            2 1 1 1 1
        """

        # Create a temporary file
        self.temp_file = tempfile.NamedTemporaryFile(mode='w+', delete=False)
        self.temp_file.write(self.test_mesh_content)
        self.temp_file.close()

        # Initialize the reader
        self.reader = DassflowMeshReader()

    def tearDown(self):
        # Clean up the temporary file
        os.unlink(self.temp_file.name)

    def test_read_mesh_file(self):
        """Test reading a mesh file and verifying its contents"""
        raw_info = self.reader.read(self.temp_file.name)
        raw_vertices, raw_cells, inlet, outlet = raw_info[:4]

        # Test vertices
        self.assertEqual(len(raw_vertices), 6)
        self.assertEqual(raw_vertices[0], RawVertex(1, 0.0, 0.0))
        self.assertEqual(raw_vertices[1], RawVertex(2, 1.0, 0.0))
        self.assertEqual(raw_vertices[5], RawVertex(6, 2.0, 1.0))

        # Test cells
        self.assertEqual(len(raw_cells), 4)
        self.assertEqual(raw_cells[0], RawCell(1, 1, 2, 5, 1))
        self.assertEqual(raw_cells[1], RawCell(2, 2, 3, 6, 2))
        self.assertEqual(raw_cells[3], RawCell(4, 2, 5, 6, 2))

        # Test boundaries
        self.assertEqual(len(inlet), 1)
        self.assertEqual(inlet[0], RawInlet(3, 1, 1, 1.0))

        self.assertEqual(len(outlet), 1)
        self.assertEqual(outlet[0], RawOutlet(2, 1, 1, 1.0))

    def test_vertex_coordinates(self):
        """Test that vertex coordinates are correctly read"""
        raw_info = self.reader.read(self.temp_file.name)
        raw_vertices = raw_info[0]

        # Check coordinates of specific vertices
        self.assertAlmostEqual(raw_vertices[0][1], 0.0)  # x-coord of vertex 1
        self.assertAlmostEqual(raw_vertices[0][2], 0.0)  # y-coord of vertex 1
        self.assertAlmostEqual(raw_vertices[2][1], 2.0)  # x-coord of vertex 3
        self.assertAlmostEqual(raw_vertices[2][2], 0.0)  # y-coord of vertex 3
        self.assertAlmostEqual(raw_vertices[5][1], 2.0)  # x-coord of vertex 6
        self.assertAlmostEqual(raw_vertices[5][2], 1.0)  # y-coord of vertex 6

    def test_cell_connectivity(self):
        """Test that cell connectivity is correctly read"""
        raw_info = self.reader.read(self.temp_file.name)
        raw_cells = raw_info[1]

        # Check connectivity of specific cells
        self.assertEqual(raw_cells[0], (1, 1, 2, 5, 1))  # Cell 1
        self.assertEqual(raw_cells[1], (2, 2, 3, 6, 2))  # Cell 2
        self.assertEqual(raw_cells[3], (4, 2, 5, 6, 2))  # Cell 5

    def test_triangular_cells(self):
        """Test handling of triangular cells (where node4 = node1)"""
        # Create a test file with a triangular cell
        triangular_mesh_content = """
            # mesh with triangular cell
            4 2 1.0
            #Nodes||| id node, x coord, y coord, bathymetry
            1 0.0 0.0 0.0
            2 1.0 0.0 0.0
            3 0.0 1.0 0.0
            4 1.0 1.0 0.0
            #cells||| id cell, id_node1, id_node2, id_node3, id_node4, patch_manning, bathymetry
            1 1 2 4 0 1 0.
            2 1 4 3 0 1 0.
            # boundaries
            INLET 0 0
            OUTLET 0 0
        """

        # Create a temporary file
        temp_file = tempfile.NamedTemporaryFile(mode='w+', delete=False)
        temp_file.write(triangular_mesh_content)
        temp_file.close()

        try:
            raw_info = self.reader.read(temp_file.name)
            raw_cells = raw_info[1]

            # Check that triangular cells are handled correctly (node4 = node1)
            self.assertEqual(raw_cells[0], (1, 1, 2, 4, 1))  # Should be (1, 2, 4, 1)
            self.assertEqual(raw_cells[1], (2, 1, 4, 3, 1))  # Should be (1, 4, 3, 1)
        finally:
            # Clean up
            os.unlink(temp_file.name)

if __name__ == '__main__':
    unittest.main()
