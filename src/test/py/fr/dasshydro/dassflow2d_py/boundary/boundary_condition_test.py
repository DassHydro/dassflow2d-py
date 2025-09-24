import unittest
import tempfile

from fr.dasshydro.dassflow2d_py.boundary.BoundaryCondition import BoundaryCondition, createBoundaryConditions
from fr.dasshydro.dassflow2d_py.input.DassflowMeshReader import DassflowMeshReader
from fr.dasshydro.dassflow2d_py.mesh.MeshImpl import MeshImpl, Boundary, BoundaryType, RawCell, RawVertex, RawInlet, RawOutlet
from fr.dasshydro.dassflow2d_py.input.Configuration import Configuration


class MockBoundary(Boundary):
    def __init__(self, boundary_type: BoundaryType, group_number: int):
        self.type = boundary_type
        self.group_number = group_number

    def getType(self) -> BoundaryType:
        return self.type

    def getEdge(self):
        return None


class MockBoundaryCondition(BoundaryCondition):
    def __init__(self, cfg, boundaries, *args):
        group_number = int(args[0])
        self.boundaries = boundaries
        self.group_number = group_number

    def getBoundaryType(self):
        return None

    def update(self, mesh, bathymetry, state, simulation_time):
        pass


# Test class
class TestBoundaryConditions(unittest.TestCase):

    def setUp(self):

        self.configuration = Configuration()
        self.bc_temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)

        self.configuration.updateValues({
            "boundary-condition-file": self.bc_temp_file.name
        })

    def test_createBoundaryConditions(self):
        # Setup
        wall1 = MockBoundary(BoundaryType.WALL, 0)
        wall2 = MockBoundary(BoundaryType.WALL, 0)
        inflow1 = MockBoundary(BoundaryType.INFLOW, 1)
        inflow2 = MockBoundary(BoundaryType.INFLOW, 1)
        inflow3 = MockBoundary(BoundaryType.INFLOW, 2)
        outflow1 = MockBoundary(BoundaryType.OUTFLOW, 3)
        outflow2 = MockBoundary(BoundaryType.OUTFLOW, 3)
        outflow3 = MockBoundary(BoundaryType.OUTFLOW, 4)
        boundaries = [wall1, wall2, inflow1, inflow2, inflow3, outflow1, outflow2, outflow3]
        boundaries_group = {boundary: boundary.group_number for boundary in boundaries}

        bc_file_content = """
            4 # number of boundary conditions
            1 discharg1 1
            2 discharg1 2
            3 ratcurve 1
            4 ratcurve 2
        """

        self.bc_temp_file.write(bc_file_content)
        self.bc_temp_file.close()

        boundary_condition_class_association = {
            "wall": MockBoundaryCondition,
            "discharg1": MockBoundaryCondition,
            "ratcurve": MockBoundaryCondition
        }

        # Call the function
        boundary_conditions = createBoundaryConditions(
            self.configuration,
            boundaries,
            boundaries_group,
            boundary_condition_class=boundary_condition_class_association
        )

        # Assertions
        self.assertEqual(len(boundary_conditions), 5)
        for bc in boundary_conditions:
            self.assertIsInstance(bc, MockBoundaryCondition)
        grouped_boundary_condition = {bc.group_number: bc.boundaries for bc in boundary_conditions}
        self.assertEqual([wall1, wall2], grouped_boundary_condition[0])
        self.assertEqual([inflow1, inflow2], grouped_boundary_condition[1])
        self.assertEqual([inflow3], grouped_boundary_condition[2])
        self.assertEqual([outflow1, outflow2], grouped_boundary_condition[3])
        self.assertEqual([outflow3], grouped_boundary_condition[4])

    def test_createBoundaryConditions_errors(self):
        # Setup
        boundaries = [
            MockBoundary(BoundaryType.WALL, 0)
        ]
        boundaries_group = {boundary: boundary.group_number for boundary in boundaries}

        # Unable to read error

        boundary_condition_class_association = {
            "wall": MockBoundaryCondition
        }

        with self.assertRaises(EOFError):
            createBoundaryConditions(
                self.configuration,
                boundaries,
                boundaries_group,
                boundary_condition_class=boundary_condition_class_association
            )

        # Unimplemented namespace error

        bc_file_content = "0"
        self.bc_temp_file.write(bc_file_content)
        self.bc_temp_file.close()

        empty_class_association = {}

        with self.assertRaises(NotImplementedError):
            createBoundaryConditions(
                self.configuration,
                boundaries,
                boundaries_group,
                boundary_condition_class=empty_class_association
            )


if __name__ == "__main__":
    unittest.main()
