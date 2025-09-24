from fr.dasshydro.dassflow2d_py.resolution.ResolutionMethod import TemporalScheme, SpatialScheme
from fr.dasshydro.dassflow2d_py.output.ResultWriter import OutputMode

class Configuration:
    """
    This class holds all configuration namespaces and link them to a corresponding getter.
    This class does not support data source resolution
    (i.e. it does not remember for each namespace, the source of the associated value)
    """

    # Define default values and valid namespaces at the same time
    DEFAULT = {
        'temporal-scheme': TemporalScheme.EULER.value,
        'spatial-scheme': SpatialScheme.HLLC.value,
        'mesh-file': 'mesh.geo',
        'boundary-condition-file': 'bc.txt',
        'initial-state-file': 'dof_init.txt',
        'bathymetry-file': 'bathymetry.txt',
        'hydrographs-file': 'hydrograph.txt',
        'rating-curve-file': 'rating_curve.txt',
        'manning-file': 'manning.txt',
        'result-path': 'output/',
        'output-mode': OutputMode.GNUPLOT.value,
        'simulation-time': '10000.0',
        'delta-to-write': '100.0',
        'is-delta-adaptative': 'False',
        'default-delta': '0.01'
    }

    def __init__(self):
        self.updateValues(self.DEFAULT)

    def getTemporalScheme(self) -> TemporalScheme:
        return self.temporal_scheme

    def getSpatialScheme(self) -> SpatialScheme:
        return self.spatial_scheme

    def getMeshFile(self) -> str:
        return self.mesh_file

    def getBoundaryConditionFile(self) -> str:
        return self.boundary_condition_file

    def getInitialStateFile(self) -> str:
        return self.initial_state_file

    def getBathymetryFile(self) -> str:
        return self.bathymetry_file

    def getHydrographsFile(self) -> str:
        return self.hydrographs_file

    def getRatingCurvesFile(self) -> str:
        return self.rating_curves_file

    def getManningFile(self) -> str:
        return self.manning_file

    def getResultFilePath(self) -> str:
        return self.result_path

    def getOutputMode(self) -> OutputMode:
        return self.output_mode

    def getSimulationTime(self) -> float:
        return self.simulation_time

    def getDeltaToWrite(self) -> float:
        return self.delta_to_write

    def isDeltaAdaptative(self) -> bool:
        return self.is_delta_adaptative

    def getDefaultDelta(self) -> float:
        return self.default_delta

    def updateValues(self, values: dict[str, str]):
        if 'temporal-scheme' in values:
            self.temporal_scheme = TemporalScheme(values['temporal-scheme'])

        if 'spatial-scheme' in values:
            self.spatial_scheme = SpatialScheme(values['spatial-scheme'])

        if 'mesh-file' in values:
            self.mesh_file = values['mesh-file']

        if 'boundary-condition-file' in values:
            self.boundary_condition_file = values['boundary-condition-file']

        if 'initial-state-file' in values:
            self.initial_state_file = values['initial-state-file']

        if 'bathymetry-file' in values:
            self.bathymetry_file = values['bathymetry-file']

        if 'hydrographs-file' in values:
            self.hydrographs_file = values['hydrographs-file']

        if 'rating-curve-file' in values:
            self.rating_curves_file = values['rating-curve-file']

        if 'manning-file' in values:
            self.manning_file = values['manning-file']

        if 'result-path' in values:
            self.result_path = values['result-path']

        if 'output-mode' in values:
            self.output_mode = OutputMode(values['output-mode'])

        if 'simulation-time' in values:
            self.simulation_time = float(values['simulation-time'])

        if 'delta-to-write' in values:
            self.delta_to_write = float(values['delta-to-write'])

        if 'is-delta-adaptative' in values:
            self.is_delta_adaptative = bool(values['is-delta-adaptative'])

        if 'default-delta' in values:
            self.default_delta = float(values['default-delta'])


import yaml

def load_from_file(file_path: str) -> Configuration:
    """
    Load configuration values from a YAML file and return a Configuration object.
    :param str file_path: configuration yaml file path
    :return: An instance of Configuration with values updated to match configuration yaml file content
    :rtype: Configuration
    """
    config = Configuration()

    with open(file_path, 'r') as file:
        yaml_data = yaml.safe_load(file)

    config.updateValues(yaml_data)

    return config
