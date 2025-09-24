import unittest
import os
import yaml
from math import sqrt
from statistics import mean
from fr.dasshydro.dassflow2d_py.input.DassflowMeshReader import DassflowMeshReader
from fr.dasshydro.dassflow2d_py.mesh.MeshImpl import MeshImpl, BoundaryType, Boundary
# Unnecessary imports (here for type check)
from fr.dasshydro.dassflow2d_py.mesh.Mesh import RawVertex, RawCell

class TestMeshImpl(unittest.TestCase):
    def setUp(self):
        # Initialize path variables
        self.mesh_path = os.path.join('src', 'test', 'resources', 'mesh', 'mesh1.geo')
        self.oracle_path = os.path.join('src', 'test', 'resources', 'mesh', 'mesh1.orcl')
        # Intermediate values
        raw_info = DassflowMeshReader().read(self.mesh_path)
        raw_vertices, raw_cells, raw_inlets, raw_outlets = raw_info[:4]
        # Build mesh
        self.mesh = MeshImpl.createFromPartialInformation(raw_vertices, raw_cells, raw_inlets, raw_outlets, {})
        # Read oracle
        with open(self.oracle_path, 'r') as file:
            self.oracle_data = yaml.safe_load(file)
        # Set test variables
        self.raw_vertices = raw_vertices
        self.raw_cells = raw_cells
        self.raw_inlets = raw_inlets
        self.raw_outlets = raw_outlets

    def testCreateFromPartialInformation(self):
        self.assertEqual(self.mesh.getVertexNumber(), len(self.raw_vertices))
        self.assertEqual(self.mesh.getCellNumber(), len(self.raw_cells))
        self.assertEqual(self.mesh.getSurface(), self.oracle_data['header']['surface'])
        self.assertEqual(self.mesh.getEdgeNumber(), self.oracle_data['header']['edge_number'])

    def testVerticesCoordinates(self):
        raw_vertices_dict = {raw_vertex.id: raw_vertex for raw_vertex in self.raw_vertices}
        for vertex in self.mesh.getVertices():
            # check coordinates
            corresponding_raw_vertex = raw_vertices_dict[vertex.getID()]
            corresponding_coord = (corresponding_raw_vertex.x_coord, corresponding_raw_vertex.y_coord)
            self.assertEqual(vertex.getCoordinates(), corresponding_coord)
            # check boundary bool
            expected_boundary_value = self.oracle_data['vertices'][vertex.getID()]
            self.assertEqual(vertex.isBoundary(), expected_boundary_value)

    def testCellProperties(self):
        raw_cells_dict = {raw_cell.id: raw_cell for raw_cell in self.raw_cells}
        for cell in self.mesh.getCells():
            corresponding_raw_cell = raw_cells_dict[cell.getID()]
            # check vertices list
            raw_cells_vertices = list(set((
                corresponding_raw_cell.vertex1,
                corresponding_raw_cell.vertex2,
                corresponding_raw_cell.vertex3,
                corresponding_raw_cell.vertex4
            )))
            self.assertEqual(len(raw_cells_vertices), cell.getVerticesNumber())
            cells_vertices_id = [v.getID() for v in cell.getVertices()]
            self.assertIn(corresponding_raw_cell.vertex1, cells_vertices_id)
            self.assertIn(corresponding_raw_cell.vertex2, cells_vertices_id)
            self.assertIn(corresponding_raw_cell.vertex3, cells_vertices_id)
            self.assertIn(corresponding_raw_cell.vertex4, cells_vertices_id)
            # check neighbors list
            expected_neighbors = self.oracle_data['cells'][cell.getID()][3]
            cells_neighbors_id = [n.getID() for n in cell.getNeighbors()]
            expected_ghost_cell_number = 0
            for expected_neighbor in expected_neighbors:
                if expected_neighbor == None:
                    expected_ghost_cell_number += 1
                else:
                    self.assertIn(expected_neighbor, cells_neighbors_id)
            ghost_cell_number = len([ghost_cell for ghost_cell in cell.getNeighbors() if ghost_cell.isGhost()])
            self.assertEqual(expected_ghost_cell_number, ghost_cell_number)
            # check ghost
            self.assertFalse(cell.isGhost())
            # check geometric properties
            raw_vertices_dict = {raw_vertex.id: raw_vertex for raw_vertex in self.raw_vertices}
            raw_vertices_x = [raw_vertices_dict[raw_vertex_id].x_coord for raw_vertex_id in raw_cells_vertices]
            raw_vertices_y = [raw_vertices_dict[raw_vertex_id].y_coord for raw_vertex_id in raw_cells_vertices]
            expected_gravity_center = (
                mean(raw_vertices_x),
                mean(raw_vertices_y)
            )
            self.assertEqual(expected_gravity_center, cell.getGravityCenter())
            expected_surface = self.oracle_data['cells'][cell.getID()][0]
            self.assertEqual(expected_surface, cell.getSurface())
            expected_perimeter = self.oracle_data['cells'][cell.getID()][1]
            self.assertAlmostEqual(expected_perimeter, cell.getPerimeter())
            # check boundary
            expected_boundary_value = self.oracle_data['cells'][cell.getID()][2]
            self.assertEqual(expected_boundary_value, cell.isBoundary())

    def testEdgeProperties(self):
        # build expected boundaries dictionary
        expected_boundaries = {
            # split the key string into a tuple of IDs (int)
            tuple(sorted(map(int, key.split(", ")))):
            value
            for key, value in self.oracle_data['edges'].items()
        }

        for edge in self.mesh.getEdges():
            ### Geometric properties
            edge_vertex1, edge_vertex2 = edge.getVertices()
            ev1_x, ev1_y = edge_vertex1.getCoordinates()
            ev2_x, ev2_y = edge_vertex2.getCoordinates()
            self.assertAlmostEqual(edge.getCenter()[0], (ev1_x + ev2_x)/2)
            self.assertAlmostEqual(edge.getCenter()[1], (ev1_y + ev2_y)/2)
            self.assertAlmostEqual(edge.getLength(), sqrt((ev2_x - ev1_x)**2 + (ev2_y - ev1_y)**2))
            # normal vector
            vertices_vector = (ev2_x - ev1_x, ev2_y - ev1_y)
            normal_vector = edge.getNormalVector()
            dot_product = vertices_vector[0] * normal_vector[0] + vertices_vector[1] * normal_vector[1]
            self.assertEqual(dot_product, 0, msg="le vecteur normal doit être orthogonal à l'arrête")
            edge_center = edge.getCenter()
            avoided_cell_center = edge.getCells()[0].getGravityCenter()
            direction_vector = (edge_center[0] - avoided_cell_center[0], edge_center[1] - avoided_cell_center[1])
            dot_product = direction_vector[0] * normal_vector[0] + direction_vector[1] * normal_vector[1]
            self.assertGreater(dot_product, 0, msg="le vecteur normal doit avoir le bon sens (de gauche à droite)")
            self.assertAlmostEqual(sqrt(normal_vector[0]**2 + normal_vector[1]**2), 1, places=6, msg="le vecteur normal doit être unitaire")
            # flux direction vector
            cell1_center = edge.getCells()[0].getGravityCenter()
            cell2_center = edge.getCells()[1].getGravityCenter()
            expected_flux_vector = (cell2_center[0] - cell1_center[0], cell2_center[1] - cell1_center[1])
            self.assertAlmostEqual(edge.getFluxDirectionVector()[0], expected_flux_vector[0])
            self.assertAlmostEqual(edge.getFluxDirectionVector()[1], expected_flux_vector[1])
            # vector to cell
            edge_center = edge.getCenter()
            for cell in self.mesh.getCells():
                vector_to_cell = edge.getVectorToCellCenter(cell)
                cell_center = cell.getGravityCenter()
                displaced_edge_center = (edge_center[0] + vector_to_cell[0], edge_center[1] + vector_to_cell[1])
                self.assertAlmostEqual(displaced_edge_center[0], cell_center[0])
                self.assertAlmostEqual(displaced_edge_center[1], cell_center[1])
            ### Boundary specific properties
            cell1, cell2 = edge.getCells()
            self.assertNotEqual(cell1, cell2)
            self.assertFalse(cell1.isGhost() and cell2.isGhost())
            if cell1.isGhost() or cell2.isGhost():
                self.assertTrue(cell1.isBoundary() or cell2.isBoundary())
                self.assertTrue(edge.isBoundary())
            else:
                self.assertFalse(edge.isBoundary())
            ### check correct boundary
            edge_vertices_id = (edge_vertex1.getID(), edge_vertex2.getID())
            edge_key = tuple(sorted(edge_vertices_id))
            expected_boundary_value = expected_boundaries[edge_key]
            self.assertEqual(expected_boundary_value, edge.isBoundary())

    def testBoundary(self):
        boundary_oracles = self.oracle_data['boundaries']
        expected_boundaries_number = len(boundary_oracles)
        self.assertEqual(expected_boundaries_number, self.mesh.getBoundaryNumber())

        # build expected boundaries dictionary
        expected_boundaries = {
            # split the key string into a tuple of IDs (int)
            tuple(sorted(map(int, key.split(", ")))):
            # convert the string value to the corresponding BoundaryType
            BoundaryType(value)
            for key, value in boundary_oracles.items()
        }
        # build actual boundaries dictionary
        actual_boundaries = {}
        for boundary in self.mesh.getBoundaries():
            edge = boundary.getEdge()
            vertex1, vertex2 = edge.getVertices()
            vertex_id1 = vertex1.getID()
            vertex_id2 = vertex2.getID()
            # Use a sorted tuple to ensure (1, 2) and (2, 1) map to the same key
            key = tuple(sorted((vertex_id1, vertex_id2)))
            actual_boundaries[key] = boundary

        ### compare boundary dictionaries
        # check correct boundary targets
        expected_edges = expected_boundaries.keys()
        sorted_expected = [tuple(sorted(e)) for e in expected_edges]
        for expected_edge in sorted_expected: # unpack to compare sorted tuples
            self.assertIn(expected_edge, actual_boundaries.keys())
        # check correct boundary type
        for key in expected_boundaries:
            sorted_key = tuple(sorted(key))
            boundary = actual_boundaries[sorted_key]
            expected_type = expected_boundaries[key]
            self.assertEqual(boundary.getType(), expected_type)

if __name__ == '__main__':
    unittest.main()
