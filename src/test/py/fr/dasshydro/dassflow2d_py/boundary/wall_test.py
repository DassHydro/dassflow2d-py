import unittest
from unittest.mock import MagicMock

from dassflow2d_py.boundary.Wall import Wall
from dassflow2d_py.mesh.Mesh import Boundary, BoundaryType, Cell
from dassflow2d_py.d2dtime.TimeStepState import TimeStepState, Node

class TestWall(unittest.TestCase):
    def setUp(self):
        # Mock configuration
        self.config = MagicMock()

        # Mock cells
        self.left_cell = MagicMock(spec=Cell)
        self.ghost_cell = MagicMock(spec=Cell)

        # Mock edge
        self.edge = MagicMock()
        self.edge.getCells.return_value = [self.left_cell, self.ghost_cell]
        self.edge.getGhostCell.return_value = self.ghost_cell

        # Mock boundary
        self.boundary = MagicMock(spec=Boundary)
        self.boundary.getEdge.return_value = self.edge
        self.boundary.getType.return_value = BoundaryType.WALL

        self.boundaries = [self.boundary]

        # Mock bathymetry
        self.bathymetry = {self.left_cell: 1.0, self.ghost_cell: 2.0}

        # Mock nodes
        self.left_node = MagicMock(spec=Node)
        self.left_node.h = 3.0
        self.left_node.u = 4.0
        self.left_node.v = 5.0

        self.ghost_node = MagicMock(spec=Node)

        # Mock state
        self.state = MagicMock(spec=TimeStepState)
        self.state.getNode.side_effect = lambda cell: self.left_node if cell == self.left_cell else self.ghost_node

        # Create Wall instance
        self.wall = Wall(self.config, self.boundaries)

    def test_update(self):
        # Call update
        self.wall.update(self.bathymetry, self.state, 0.0)

        # Check that ghost cell values are updated correctly
        self.assertAlmostEqual(self.ghost_node.h, 3.0 + 1.0 - 2.0)  # hR = hL + zL - zR
        self.assertAlmostEqual(self.ghost_node.u, -4.0)  # uR = -uL
        self.assertAlmostEqual(self.ghost_node.v, 5.0)  # vR = vL

if __name__ == "__main__":
    unittest.main()
