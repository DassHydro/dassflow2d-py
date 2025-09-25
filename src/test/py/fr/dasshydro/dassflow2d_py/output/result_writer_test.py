import unittest
import os
from tempfile import TemporaryDirectory
import h5py #type: ignore
import vtk #type: ignore

from fr.dasshydro.dassflow2d_py.output.ResultWriter import ResultWriter, OutputMode
from fr.dasshydro.dassflow2d_py.d2dtime.TimeStepState import TimeStepState, Node
from fr.dasshydro.dassflow2d_py.input.DassflowMeshReader import DassflowMeshReader
from fr.dasshydro.dassflow2d_py.mesh.MeshImpl import MeshImpl

class TestResultWriter(unittest.TestCase):

    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        mesh_filepath = os.path.join('src', 'test', 'resources', 'mesh', 'mesh1.geo')
        raw_info = DassflowMeshReader().read(mesh_filepath)
        raw_mesh_info = raw_info[:4]
        self.mesh = MeshImpl.createFromPartialInformation(*(*raw_mesh_info, {}))
        self.result_writer = ResultWriter(self.mesh, self.temp_dir.name, 1.0)

    def tearDown(self):
        # Clean up the temporary directory
        self.temp_dir.cleanup()

    def testValidParameters(self):
        # Test for invalid path
        with self.assertRaises(ValueError, msg="Constructor should raise ValueError for invalid paths"):
            ResultWriter(self.mesh, None, 1.0)

        # Test for file path
        with self.assertRaises(ValueError, msg="Constructor should raise ValueError for paths that point to files"):
            ResultWriter(self.mesh, os.path.join('src', 'test', 'resources', 'output', 'file'), 1.0)

        # Test for negative delta_to_write
        with self.assertRaises(ValueError, msg="Constructor should raise ValueError for negative delta_to_write (-1.0)"):
            ResultWriter(self.mesh, os.path.join('src', 'test', 'resources', 'output'), -1.0)

        # Test for null mesh value
        with self.assertRaises(ValueError, msg="Constructor should raise ValueError is mesh is null"):
            ResultWriter(None, os.path.join('src', 'test', 'resources', 'output'), 1.0)

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
        state = TimeStepState({cell: Node(1.0, 1.0, 1.0) for cell in self.mesh.getCells()})
        self.result_writer.save(state, 0.0)
        expected_path1 = os.path.join(self.temp_dir.name, "result_0.000000e+00.raw")
        self.assertTrue(os.path.exists(expected_path1))

        # write with current simulation time represented with a negative in scientific notation
        self.result_writer.save(state, 0.000234)
        expected_path2 = os.path.join(self.temp_dir.name, "result_2.340000e-04.raw")
        self.assertTrue(os.path.exists(expected_path2))

        # write with a great current simulation time
        self.result_writer.save(state, 124.3255)
        expected_path3 = os.path.join(self.temp_dir.name, "result_1.243255e+02.raw")
        self.assertTrue(os.path.exists(expected_path3))

        # write with a current simulation time that will overflow filename
        self.result_writer.save(state, 1.23456789)
        expected_path4 = os.path.join(self.temp_dir.name, "result_1.234568e+00.raw")
        self.assertTrue(os.path.exists(expected_path4))

    def testCorrectFileContent(self):
        # simulate that it's always time to write
        self.result_writer.last_quotient = -1

        # test file content
        H_BASE_VALUE = 0.3222
        U_BASE_VALUE = 94.3311
        V_BASE_VALUE = 5.432134
        h_value = H_BASE_VALUE
        u_value = U_BASE_VALUE
        v_value = V_BASE_VALUE
        node_dict = {}
        for cell in self.mesh.getCells():
            node_dict[cell] = Node(h_value, u_value, v_value)
            h_value += 1.0
            u_value += 1.0
            v_value += 1.0
        state = TimeStepState(node_dict)

        # write the state
        self.result_writer.save(state, 0.0)

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

    def testVTKOutput(self):
        """Test that VTK output is generated correctly and contains expected data."""
        self.result_writer.last_quotient = -1
        H_BASE_VALUE = 0.3222
        U_BASE_VALUE = 94.3311
        V_BASE_VALUE = 5.432134
        h_value = H_BASE_VALUE
        u_value = U_BASE_VALUE
        v_value = V_BASE_VALUE
        node_dict = {}
        for cell in self.mesh.getCells():
            node_dict[cell] = Node(h_value, u_value, v_value)
            h_value += 1.0
            u_value += 1.0
            v_value += 1.0
        state = TimeStepState(node_dict)
        # Write the state
        self.result_writer.save(state, 0.0)
        # Convert to VTK
        self.result_writer.writeAll(OutputMode.VTK)
        # Check the file exists
        expected_path = os.path.join(self.temp_dir.name, "result_0.000000e+00.vtk")
        self.assertTrue(os.path.exists(expected_path))

        # Try to read the file with vtkUnstructuredGridReader
        reader = vtk.vtkUnstructuredGridReader()
        reader.SetFileName(expected_path)
        reader.Update()  # This will raise an exception if the file is invalid
        output = reader.GetOutput()
        self.assertIsNotNone(output, "Failed to read VTK file")
        self.assertGreater(output.GetNumberOfPoints(), 0, "No points in VTK file")
        self.assertGreater(output.GetNumberOfCells(), 0, "No cells in VTK file")

    def testTecplotOutput(self):
        """Test that Tecplot output is generated correctly and contains expected data."""
        self.result_writer.last_quotient = -1
        H_BASE_VALUE = 0.3222
        U_BASE_VALUE = 94.3311
        V_BASE_VALUE = 5.432134
        h_value = H_BASE_VALUE
        u_value = U_BASE_VALUE
        v_value = V_BASE_VALUE
        node_dict = {}
        for cell in self.mesh.getCells():
            node_dict[cell] = Node(h_value, u_value, v_value)
            h_value += 1.0
            u_value += 1.0
            v_value += 1.0
        state = TimeStepState(node_dict)
        # Write the state
        self.result_writer.save(state, 0.0)
        # Convert to Tecplot
        self.result_writer.writeAll(OutputMode.TECPLOT)
        # Check the file exists
        expected_path = os.path.join(self.temp_dir.name, "result_0.000000e+00.plt")
        self.assertTrue(os.path.exists(expected_path))

        # Read and check the Tecplot file content
        with open(expected_path, "r") as f:
            lines = f.readlines()

        # Check header
        self.assertTrue(lines[0].startswith('TITLE = "DassFlow Result File in Time"'))
        self.assertTrue('VARIABLES = "x","y","bathy","h","zs","Manning","u","v"' in lines[1])

        # Check ZONE line
        zone_line = lines[2].strip()
        self.assertTrue(zone_line.startswith('ZONE T = "0.000000e+00"'))
        self.assertTrue("DATAPACKING = BLOCK" in zone_line)
        self.assertTrue("ZONETYPE = FEQUADRILATERAL" in zone_line)

        # Check VARLOCATION
        var_location_line = lines[3].strip()
        self.assertTrue('VARLOCATION = ([3-8]=CELLCENTERED)' in var_location_line)

        # Check some values (optional, but recommended)
        # Note: Tecplot files are more complex, so this is a simplified check
        h_values_start = 4 + self.mesh.getVertexNumber()
        for i, line in enumerate(lines[h_values_start:h_values_start + 3]):
            parts = line.strip().split()
            print(parts)
            if len(parts) >= 3:
                h_val = float(parts[0])
                expected_h = H_BASE_VALUE + i * 1.0
                self.assertAlmostEqual(h_val, expected_h, places=6, msg=f"h value mismatch in Tecplot file")

    def testGnuplotOutput(self):
        """Test that Gnuplot output is generated correctly and contains expected data."""
        self.result_writer.last_quotient = -1
        H_BASE_VALUE = 0.3222
        U_BASE_VALUE = 94.3311
        V_BASE_VALUE = 5.432134
        h_value = H_BASE_VALUE
        u_value = U_BASE_VALUE
        v_value = V_BASE_VALUE
        node_dict = {}
        for cell in self.mesh.getCells():
            node_dict[cell] = Node(h_value, u_value, v_value)
            h_value += 1.0
            u_value += 1.0
            v_value += 1.0
        state = TimeStepState(node_dict)
        # Write the state
        self.result_writer.save(state, 0.0)
        # Convert to Gnuplot
        self.result_writer.writeAll(OutputMode.GNUPLOT)
        # Check the file exists
        expected_path = os.path.join(self.temp_dir.name, "result_0.000000e+00.dat")
        self.assertTrue(os.path.exists(expected_path))

        # Read and check the Gnuplot file content
        with open(expected_path, "r") as f:
            lines = f.readlines()

        # Check header
        self.assertTrue(lines[0].startswith(" # Gnuplot DataFile Version"))
        self.assertTrue('i x y bathy h zs Manning u v' in lines[1])

        # Check some values (optional, but recommended)
        for i, line in enumerate(lines[2:5]):
            parts = line.strip().split()
            print(parts)
            if len(parts) >= 9:
                h_val = float(parts[6])
                u_val = float(parts[9])
                v_val = float(parts[10])
                expected_h = H_BASE_VALUE + i * 1.0
                expected_u = U_BASE_VALUE + i * 1.0
                expected_v = V_BASE_VALUE + i * 1.0
                self.assertAlmostEqual(h_val, expected_h, places=6, msg=f"h value mismatch in Gnuplot file")
                self.assertAlmostEqual(u_val, expected_u, places=6, msg=f"u value mismatch in Gnuplot file")
                self.assertAlmostEqual(v_val, expected_v, places=6, msg=f"v value mismatch in Gnuplot file")

    def testHDF5Output(self):
        """Test that HDF5 output is generated correctly and contains expected data for all time steps."""
        self.result_writer.last_quotient = -1
        H_BASE_VALUE = 0.3222
        U_BASE_VALUE = 94.3311
        V_BASE_VALUE = 5.432134
        h_value = H_BASE_VALUE
        u_value = U_BASE_VALUE
        v_value = V_BASE_VALUE
        node_dict = {}
        for cell in self.mesh.getCells():
            node_dict[cell] = Node(h_value, u_value, v_value)
            h_value += 1.0
            u_value += 1.0
            v_value += 1.0
        state = TimeStepState(node_dict)
        # Write the state
        self.result_writer.save(state, 0.0)
        # Convert to HDF5
        self.result_writer.writeAll(OutputMode.HDF5)
        # Check the file exists (now named results.hdf5)
        expected_path = os.path.join(self.temp_dir.name, "results.hdf5")
        self.assertTrue(os.path.exists(expected_path))
        # Read the HDF5 file and check its content
        with h5py.File(expected_path, "r") as hdf:
            # Check that a group for time 0.0 exists
            self.assertIn("time_0.000000e+00", hdf)
            time_group = hdf["time_0.000000e+00"]
            self.assertIn("ids", time_group)
            self.assertIn("h", time_group)
            self.assertIn("u", time_group)
            self.assertIn("v", time_group)
            ids = time_group["ids"][:]
            hs = time_group["h"][:]
            us = time_group["u"][:]
            vs = time_group["v"][:]
            # Check that the values match the expected pattern
            for i, id in enumerate(ids):
                expected_h = H_BASE_VALUE + i * 1.0
                expected_u = U_BASE_VALUE + i * 1.0
                expected_v = V_BASE_VALUE + i * 1.0
                self.assertAlmostEqual(hs[i], expected_h, places=6, msg=f"h value mismatch for cell {id}")
                self.assertAlmostEqual(us[i], expected_u, places=6, msg=f"u value mismatch for cell {id}")
                self.assertAlmostEqual(vs[i], expected_v, places=6, msg=f"v value mismatch for cell {id}")
