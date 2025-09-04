import unittest
import os
from tempfile import TemporaryDirectory
from fr.dasshydro.dassflow2d_py.output.ResultWriter import ResultWriter
from fr.dasshydro.dassflow2d_py.d2dtime.TimeStepState import TimeStepState, Node
from fr.dasshydro.dassflow2d_py.input.DassflowMeshReader import DassflowMeshReader
from fr.dasshydro.dassflow2d_py.mesh.Mesh import Cell
from fr.dasshydro.dassflow2d_py.mesh.MeshImpl import MeshImpl

class TestResultWriter(unittest.TestCase):

    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.result_writer = ResultWriter(self.temp_dir.name, 1.0)

    def tearDown(self):
        # Clean up the temporary directory
        self.temp_dir.cleanup()

    def testValidParameters(self):
        # Test for invalid path
        with self.assertRaises(ValueError, msg="Constructor should raise ValueError for invalid paths"):
            ResultWriter("invalid//path../", 1.0)

        # Test for file path
        with self.assertRaises(ValueError, msg="Constructor should raise ValueError for paths that point to files"):
            ResultWriter(os.path.join('src', 'test', 'resources', 'output', 'file'), 1.0)

        # Test for negative delta_to_write
        with self.assertRaises(ValueError, msg="Constructor should raise ValueError for negative delta_to_write (-1.0)"):
            ResultWriter("valid/path/", -1.0)

    def testRightTiming(self):
        self.assertFalse(self.result_writer.isTimeToWrite(0.0))
        self.assertFalse(self.result_writer.isTimeToWrite(0.3))
        self.assertFalse(self.result_writer.isTimeToWrite(0.6))
        self.assertFalse(self.result_writer.isTimeToWrite(0.9))
        self.assertTrue(self.result_writer.isTimeToWrite(1.2))
        self.assertFalse(self.result_writer.isTimeToWrite(1.5))
        self.assertFalse(self.result_writer.isTimeToWrite(1.9))

    def testSkipTiming(self):
        self.assertTrue(self.result_writer.isTimeToWrite(2.0))
        self.assertTrue(self.result_writer.isTimeToWrite(4.5))
        self.assertTrue(self.result_writer.isTimeToWrite(6.0))

    def testCorrectFilenames(self):
        """Test that write creates files with sequential names."""
        # simulate that it's always time to write
        self.result_writer.last_quotient = -1

        # write zero as current simulation time
        state = TimeStepState({})
        self.result_writer.write(state, 0.0)
        expected_path1 = os.path.join(self.temp_dir.name, "result_0.000000e+00.raw")
        self.assertTrue(os.path.exists(expected_path1))

        # write with current simulation time represented with a negative in scientific notation
        self.result_writer.write(state, 0.000234)
        expected_path2 = os.path.join(self.temp_dir.name, "result_2.340000e-04.raw")
        self.assertTrue(os.path.exists(expected_path2))

        # write with a great current simulation time
        self.result_writer.write(state, 124.3255)
        expected_path3 = os.path.join(self.temp_dir.name, "result_1.243255e+02.raw")
        self.assertTrue(os.path.exists(expected_path3))

        # write with a current simulation time that will overflow filename
        self.result_writer.write(state, 1.23456789)
        expected_path4 = os.path.join(self.temp_dir.name, "result_1.234568e+00.raw")
        self.assertTrue(os.path.exists(expected_path4))

    def testCorrectFileContent(self):
        # simulate that it's always time to write
        self.result_writer.last_quotient = -1

        # TODO: test file content
        mesh_filepath = os.path.join('src', 'test', 'resources', 'mesh', 'mesh1.geo')
        rv, rc, ri, ro = DassflowMeshReader().read(mesh_filepath)
        mesh = MeshImpl.createFromPartialInformation(rv, rc, ri, ro)
        H_BASE_VALUE = 0.3222
        U_BASE_VALUE = 94.3311
        V_BASE_VALUE = 5.432134
        h_value = H_BASE_VALUE
        u_value = U_BASE_VALUE
        v_value = V_BASE_VALUE
        node_dict = {}
        for cell in mesh.getCells():
            node_dict[cell] = Node(h_value, u_value, v_value)
            h_value += 1.0
            u_value += 1.0
            v_value += 1.0
        state = TimeStepState(node_dict)

        # write the state
        self.result_writer.write(state, 0.0)

        # check the file exists
        expected_path = os.path.join(self.temp_dir.name, "result_0.000000e+00.raw")
        self.assertTrue(os.path.exists(expected_path))

        # read the file and check its content
        with open(expected_path, "r") as file:
            lines = file.readlines()
        
        ### check information coherence, we should get the values we put in node_dict
        # parse lines into a list of (id, h, u, v)
        parsed_values = []
        for line in lines:
            parts = line.strip().split()
            id = int(parts[0])
            h = float(parts[1])
            u = float(parts[2])
            v = float(parts[3])
            parsed_values.append((id, h, u, v))

        # sort by cell ID
        parsed_values.sort(key=lambda x: x[0])

        # check that the values match the expected pattern
        for i, (id, h, u, v) in enumerate(parsed_values):
            expected_h = H_BASE_VALUE + i * 1.0
            expected_u = U_BASE_VALUE + i * 1.0
            expected_v = V_BASE_VALUE + i * 1.0

            self.assertAlmostEqual(h, expected_h, places=6, msg=f"h value mismatch for cell {id}")
            self.assertAlmostEqual(u, expected_u, places=6, msg=f"u value mismatch for cell {id}")
            self.assertAlmostEqual(v, expected_v, places=6, msg=f"v value mismatch for cell {id}")
