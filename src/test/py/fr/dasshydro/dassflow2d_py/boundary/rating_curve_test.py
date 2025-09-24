import unittest
import os

from fr.dasshydro.dassflow2d_py.input.Configuration import Configuration
from fr.dasshydro.dassflow2d_py.boundary.RatingCurve import RatingCurve
from fr.dasshydro.dassflow2d_py.mesh.MeshImpl import Boundary, BoundaryType, Edge, Cell
from fr.dasshydro.dassflow2d_py.d2dtime.TimeStepState import TimeStepState, Node

class MockCell(Cell):
    def getID(self):
        pass
    def getSurface(self):
        pass
    def getPerimeter(self):
        pass
    def getVertices(self):
        pass
    def getVerticesNumber(self):
        pass
    def getEdges(self):
        pass
    def getNeighbors(self):
        pass
    def getGravityCenter(self):
        pass
    def isBoundary(self):
        pass
    def isGhost(self):
        return True

class MockEdge(Edge):
    def __init__(self, length: float, cell: Cell, ghost_cell: Cell):
        self.length = length
        self.cell = cell
        self.ghost_cell = ghost_cell
    def getID(self):
        pass
    def getVertices(self):
        pass
    def getCenter(self):
        pass
    def getLength(self):
        return self.length
    def getCells(self):
        return (self.cell, self.ghost_cell)
    def getNormalVector(self):
        return (1, 0)
    def getFluxDirectionVector(self):
        pass
    def getVectorToCellCenter(self, cell):
        pass
    def isBoundary(self):
        return True
    def getGhostCell(self):
        return self.ghost_cell

class MockBoundary(Boundary):
    def __init__(self, edge: Edge):
        self.edge = edge

    def getEdge(self):
        return self.edge

    def getType(self):
        return BoundaryType.OUTFLOW

class TestRatingCurve(unittest.TestCase):
    def setUp(self):
        # Setup configuration
        self.config = Configuration()
        rating_curve_filepath = os.path.join('src', 'test', 'resources', 'boundary', 'rating_curves.txt')
        self.config.updateValues({
            "rating-curve-file": rating_curve_filepath
        })

        # Setup cells and edges
        self.small_cell = MockCell()
        self.medium_cell = MockCell()
        self.large_cell = MockCell()
        self.small_ghost_cell = MockCell()
        self.medium_ghost_cell = MockCell()
        self.large_ghost_cell = MockCell()

        self.small_edge = MockEdge(1.283, self.small_cell, self.small_ghost_cell)
        self.medium_edge = MockEdge(12.83, self.medium_cell, self.medium_ghost_cell)
        self.large_edge = MockEdge(128.3, self.large_cell, self.large_ghost_cell)

        self.small_boundary = MockBoundary(self.small_edge)
        self.medium_boundary = MockBoundary(self.medium_edge)
        self.large_boundary = MockBoundary(self.large_edge)

        boundaries = [self.small_boundary, self.medium_boundary, self.large_boundary]

        # Setup RatingCurve instance
        self.rating_curve = RatingCurve(self.config, boundaries, 1, 'ratcurve', 2)

        # Setup nodes and state
        self.small_node = Node(1.0, 0.5, 0.8)
        self.medium_node = Node(10.0, 5.0, 8.0)
        self.large_node = Node(100.0, 50.0, 80.0)

        self.state = TimeStepState({
            self.small_cell: self.small_node,
            self.medium_cell: self.medium_node,
            self.large_cell: self.large_node,
            self.small_ghost_cell: self.small_node,
            self.medium_ghost_cell: self.medium_node,
            self.large_ghost_cell: self.large_node
        })

    def test_read_rating_curve(self):
        """Test reading the rating curve from a file."""
        rating_curve = self.rating_curve._read_dynamic_data(self.config.getRatingCurvesFile(), 2)
        expected_rating_curve = {
            0.0000000E+00: 0.5772765E-01,
            0.3600000E+04: 0.5772765E-01,
            0.7200000E+04: 0.5772765E-01,
            0.1080000E+05: 0.5772765E-01,
            0.1440000E+05: 0.5772765E-01,
            0.1800000E+05: 0.1555663E+00,
            0.2160000E+05: 0.3591730E+00,
            0.2520000E+05: 0.7370547E+00,
            0.2880000E+05: 0.1378366E+01,
            0.3240000E+05: 0.2390183E+01,
            0.3600000E+05: 0.2999316E+01,
            0.3960000E+05: 0.3381740E+01,
            0.4320000E+05: 0.3505978E+01,
            0.4680000E+05: 0.3372389E+01,
            0.5040000E+05: 0.3003062E+01,
            0.5400000E+05: 0.2434232E+01,
            0.5760000E+05: 0.1710678E+01,
            0.6120000E+05: 0.8819232E+02,
            0.6480000E+05: 0.6558166E-04,
            0.6840000E+05: 0.6558166E-04,
            0.7200000E+05: 0.6558166E-04,
            0.7560000E+05: 0.6558166E-04
        }
        self.assertEqual(expected_rating_curve, rating_curve)

    def test_interpolate_q_out(self):
        """Test interpolation of q_out."""

        # Test interpolation at t=18000.0 (should be 0.1555663)
        q_out = self.rating_curve.interpolate_dynamic_value(18000.0)
        self.assertAlmostEqual(q_out, 0.1555663)

        # Test interpolation at t=36000.0 (should be 2.999316)
        q_out = self.rating_curve.interpolate_dynamic_value(36000.0)
        self.assertAlmostEqual(q_out, 2.999316)

        # Test interpolation at t=50000.0 (between 46800.0 and 50400.0)
        q_out = self.rating_curve.interpolate_dynamic_value(50000.0)
        expected_q = 3.372389 - (3.372389 - 3.003062) * (50000.0 - 46800.0) / (50400.0 - 46800.0)
        self.assertAlmostEqual(q_out, expected_q, places=6)

    def test_update_distributes_q_out(self):
        """Test distribution of q_out across boundaries."""
        # Get q_out
        q_out = self.rating_curve.interpolate_dynamic_value(5.0)

        # Get actual water depths from nodes
        h_small = self.small_node.h
        h_medium = self.medium_node.h
        h_large = self.large_node.h

        # Get edge lengths
        length_small = self.small_edge.getLength()
        length_medium = self.medium_edge.getLength()
        length_large = self.large_edge.getLength()

        # Calculate sum_pow_h using actual water depths and edge lengths
        sum_pow_h = (
            (h_small ** (5/3)) * length_small +
            (h_medium ** (5/3)) * length_medium +
            (h_large ** (5/3)) * length_large
        )

        # Call update
        self.rating_curve.update({}, self.state, 5.0)

        # Calculate expected outflows using actual water depths
        expected_outflow_small = q_out * (h_small ** (2/3)) / sum_pow_h
        expected_outflow_medium = q_out * (h_medium ** (2/3)) / sum_pow_h
        expected_outflow_large = q_out * (h_large ** (2/3)) / sum_pow_h

        # Check that the outflow is distributed correctly
        self.assertAlmostEqual(self.small_node.u, expected_outflow_small, places=6)
        self.assertAlmostEqual(self.medium_node.u, expected_outflow_medium, places=6)
        self.assertAlmostEqual(self.large_node.u, expected_outflow_large, places=6)

if __name__ == "__main__":
    unittest.main()
