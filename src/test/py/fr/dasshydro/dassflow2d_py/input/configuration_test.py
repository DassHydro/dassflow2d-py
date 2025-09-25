import unittest
import os

from fr.dasshydro.dassflow2d_py.input.Configuration import Configuration
from fr.dasshydro.dassflow2d_py.resolution.ResolutionMethod import TemporalScheme, SpatialScheme
from fr.dasshydro.dassflow2d_py.output.ResultWriter import OutputMode

class TestConfiguration(unittest.TestCase):

    def setUp(self):
        self.config = Configuration('default')

    def testNamespacesValidity(self):
        # Set of configuration tested
        temporal_scheme = TemporalScheme.EULER
        spatial_scheme = SpatialScheme.MUSCL
        mesh_file = 'channel.geo'
        bc_file = 'boundary_condition.txt'
        initial_state_file = 'dof_init.txt'
        bathymetry_file = 'bathymetry.txt'
        hydrographs_file = 'hydrographs.txt'
        rating_curves_file = 'rat_curves.txt'
        manning_file = 'manning.txt'
        result_path = 'output/'
        output_mode = OutputMode.HDF5
        simulation_time = 42000
        delta_to_write = 100
        is_delta_adaptive = True
        default_delta = 0.0001

        # Apply these parameters
        self.config.updateValues({
            'temporal-scheme': temporal_scheme.value,
            'spatial-scheme': spatial_scheme.value,
            'mesh-file': mesh_file,
            'boundary-condition-file': bc_file,
            'initial-state-file': initial_state_file,
            'bathymetry-file': bathymetry_file,
            'hydrographs-file': hydrographs_file,
            'rating-curve-file': rating_curves_file,
            'manning-file': manning_file,
            'result-path': result_path,
            'output-mode': output_mode.value,
            'simulation-time': str(simulation_time),
            'delta-to-write': str(delta_to_write),
            'is-delta-adaptive': str(is_delta_adaptive),
            'default-delta': str(default_delta)
        }, None)

        # Test if all have correctly been updated
        self.assertEqual(self.config.getTemporalScheme(), temporal_scheme, "Temporal scheme is not stored correctly")
        self.assertEqual(self.config.getSpatialScheme(), spatial_scheme, "Spatial scheme is not stored correctly")
        self.assertEqual(self.config.getMeshFilePath(), mesh_file, "mesh file is not stored correctly")
        self.assertEqual(self.config.getInitialStateFilePath(), initial_state_file, "initial state file is not stored correctly")
        self.assertEqual(self.config.getBathymetryFilePath(), bathymetry_file, "bathymetry file is not stored correctly")
        self.assertEqual(self.config.getManningFilePath(), manning_file, "manning file is not stored correctly")
        self.assertEqual(self.config.getResultFolderPath(), result_path, "result path is not stored correctly")
        self.assertEqual(self.config.getSimulationTime(), simulation_time, "simulation time is not stored correctly")
        self.assertEqual(self.config.getDeltaToWrite(), delta_to_write, "delta to write is not stored correctly")
        self.assertEqual(self.config.isDeltaAdaptive(), is_delta_adaptive, "whether or not the delta is adaptive is not stored correctly")
        self.assertEqual(self.config.getDefaultDelta(), default_delta, "default delta is not stored correctly")

    def testUpdateValues(self):
        # Initial state
        current_value = float(self.config.DEFAULT['default-delta'])
        self.assertEqual(self.config.getDefaultDelta(), current_value)
        previous_value = current_value

        # First update
        current_value = 0.0001
        if current_value == previous_value:
            current_value += 0.1 # Ensure previous and current values are not the same
        self.config.updateValues({'default-delta': current_value}, None)
        self.assertEqual(self.config.getDefaultDelta(), current_value)
        previous_value = current_value

        # Second update
        current_value = 0.0578
        # current and previous are already distinct here
        self.config.updateValues({'default-delta': current_value}, None)
        self.assertEqual(self.config.getDefaultDelta(), current_value)

    def testLoadFromFile(self):
        test_config_path = os.path.join('src', 'test', 'resources', 'input', 'test_config.yml')
        self.config.update_from_file(test_config_path, None)

        # expected values from the YAML file
        expected_temporal_scheme = TemporalScheme.EULER
        expected_spatial_scheme = SpatialScheme.MUSCL
        expected_mesh_file = 'mesh_from_file.geo'
        expected_initial_state_file = 'dof_init_from_file.txt'
        expected_bathymetry_file = 'bathymetry_from_file.txt'
        expected_manning_file = 'manning_from_file.txt'
        expected_result_path = 'output_from_file/'
        expected_simulation_time = 86400
        expected_delta_to_write = 500
        expected_is_delta_adaptive = False
        expected_default_delta = 0.001

        # assert that the loaded configuration matches the expected values
        self.assertEqual(self.config.getTemporalScheme(), expected_temporal_scheme, "Temporal scheme from file is not loaded correctly")
        self.assertEqual(self.config.getSpatialScheme(), expected_spatial_scheme, "Spatial scheme from file is not loaded correctly")
        self.assertEqual(self.config.getMeshFilePath(), expected_mesh_file, "Mesh file from file is not loaded correctly")
        self.assertEqual(self.config.getInitialStateFilePath(), expected_initial_state_file, "Initial state file from file is not loaded correctly")
        self.assertEqual(self.config.getBathymetryFilePath(), expected_bathymetry_file, "Bathymetry file from file is not loaded correctly")
        self.assertEqual(self.config.getManningFilePath(), expected_manning_file, "Manning file from file is not loaded correctly")
        self.assertEqual(self.config.getResultFolderPath(), expected_result_path, "Result path from file is not loaded correctly")
        self.assertEqual(self.config.getSimulationTime(), expected_simulation_time, "Simulation time from file is not loaded correctly")
        self.assertEqual(self.config.getDeltaToWrite(), expected_delta_to_write, "Delta to write from file is not loaded correctly")
        self.assertEqual(self.config.isDeltaAdaptive(), expected_is_delta_adaptive, "Delta adaptive flag from file is not loaded correctly")
        self.assertEqual(self.config.getDefaultDelta(), expected_default_delta, "Default delta from file is not loaded correctly")


if __name__ == '__main__':
    unittest.main()
