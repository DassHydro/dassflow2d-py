import yaml

from dassflow2d_py.resolution.ResolutionMethod import TemporalScheme, SpatialScheme
from dassflow2d_py.output.ResultWriter import OutputMode


# Define constants for configuration keys
TEMPORAL_SCHEME = 'temporal-scheme'
SPATIAL_SCHEME = 'spatial-scheme'
MESH_FILE = 'mesh-file'
BOUNDARY_CONDITION_FILE = 'boundary-condition-file'
INITIAL_STATE_FILE = 'initial-state-file'
BATHYMETRY_FILE = 'bathymetry-file'
HYDROGRAPHS_FILE = 'hydrographs-file'
RATING_CURVE_FILE = 'rating-curve-file'
MANNING_FILE = 'manning-file'
RESULT_PATH = 'result-path'
OUTPUT_MODE = 'output-mode'
SIMULATION_TIME = 'simulation-time'
DELTA_TO_WRITE = 'delta-to-write'
IS_DELTA_ADAPTIVE = 'is-delta-adaptive'
DEFAULT_DELTA = 'default-delta'
CONFIG_FILE = 'config_file'

class Configuration:
    """
    This class holds all configuration namespaces and link them to a corresponding getter.
    This class does not support data source resolution
    (i.e. it does not remember for each namespace, the source of the associated value)
    """
    # Define default values and valid namespaces at the same time
    DEFAULT = {
        TEMPORAL_SCHEME: 'euler',
        SPATIAL_SCHEME: 'hllc',
        MESH_FILE: 'mesh.geo',
        BOUNDARY_CONDITION_FILE: 'bc.txt',
        INITIAL_STATE_FILE: 'dof_init.txt',
        BATHYMETRY_FILE: 'bathymetry.txt',
        HYDROGRAPHS_FILE: 'hydrograph.txt',
        RATING_CURVE_FILE: 'rating_curve.txt',
        MANNING_FILE: 'manning.txt',
        RESULT_PATH: 'output/',
        OUTPUT_MODE: 'gnuplot',
        SIMULATION_TIME: '10000.0',
        DELTA_TO_WRITE: '100.0',
        IS_DELTA_ADAPTIVE: 'False',
        DEFAULT_DELTA: '0.01'
    }

    def __init__(self, source):
        self.values = {}
        self.sources = {}
        self.updateValues(self.DEFAULT, source)

    def update_from_file(self, file_path: str, source):
        """
        Load configuration values from a YAML file and return a Configuration object.

        Args:
            file_path (str): configuration yaml file path
            source (_type_): source object to associate to each modified values
        """
        with open(file_path, 'r') as file:
            yaml_data = yaml.safe_load(file)
        self.updateValues(yaml_data, source)

    def updateValues(self, values: dict[str, str], source):
        """
        Update values from dictionary

        Args:
            values (dict[str, str]): dictionary containing values
            source (_type_): source object to associate to each modified values
        """

        if TEMPORAL_SCHEME in values:
            self.values[TEMPORAL_SCHEME] = TemporalScheme(values[TEMPORAL_SCHEME])
            self.sources[TEMPORAL_SCHEME] = source

        if SPATIAL_SCHEME in values:
            self.values[SPATIAL_SCHEME] = SpatialScheme(values[SPATIAL_SCHEME])
            self.sources[SPATIAL_SCHEME] = source

        if MESH_FILE in values:
            self.values[MESH_FILE] = values[MESH_FILE]
            self.sources[MESH_FILE] = source

        if BOUNDARY_CONDITION_FILE in values:
            self.values[BOUNDARY_CONDITION_FILE] = values[BOUNDARY_CONDITION_FILE]
            self.sources[BOUNDARY_CONDITION_FILE] = source

        if INITIAL_STATE_FILE in values:
            self.values[INITIAL_STATE_FILE] = values[INITIAL_STATE_FILE]
            self.sources[INITIAL_STATE_FILE] = source

        if BATHYMETRY_FILE in values:
            self.values[BATHYMETRY_FILE] = values[BATHYMETRY_FILE]
            self.sources[BATHYMETRY_FILE] = source

        if HYDROGRAPHS_FILE in values:
            self.values[HYDROGRAPHS_FILE] = values[HYDROGRAPHS_FILE]
            self.sources[HYDROGRAPHS_FILE] = source

        if RATING_CURVE_FILE in values:
            self.values[RATING_CURVE_FILE] = values[RATING_CURVE_FILE]
            self.sources[RATING_CURVE_FILE] = source

        if MANNING_FILE in values:
            self.values[MANNING_FILE] = values[MANNING_FILE]
            self.sources[MANNING_FILE] = source

        if RESULT_PATH in values:
            self.values[RESULT_PATH] = values[RESULT_PATH]
            self.sources[RESULT_PATH] = source

        if OUTPUT_MODE in values:
            self.values[OUTPUT_MODE] = OutputMode(values[OUTPUT_MODE])
            self.sources[OUTPUT_MODE] = source

        if SIMULATION_TIME in values:
            self.values[SIMULATION_TIME] = float(values[SIMULATION_TIME])
            self.sources[SIMULATION_TIME] = source

        if DELTA_TO_WRITE in values:
            self.values[DELTA_TO_WRITE] = float(values[DELTA_TO_WRITE])
            self.sources[DELTA_TO_WRITE] = source

        if IS_DELTA_ADAPTIVE in values:
            self.values[IS_DELTA_ADAPTIVE] = bool(values[IS_DELTA_ADAPTIVE])
            self.sources[IS_DELTA_ADAPTIVE] = source

        if DEFAULT_DELTA in values:
            self.values[DEFAULT_DELTA] = float(values[DEFAULT_DELTA])
            self.sources[DEFAULT_DELTA] = source

    def getSources(self) -> dict:
        return self.sources

    def getTemporalScheme(self):
        return self.values[TEMPORAL_SCHEME]

    def getSpatialScheme(self):
        return self.values[SPATIAL_SCHEME]

    def getMeshFilePath(self):
        return self.values[MESH_FILE]

    def getBoundaryConditionFilePath(self):
        return self.values[BOUNDARY_CONDITION_FILE]

    def getInitialStateFilePath(self):
        return self.values[INITIAL_STATE_FILE]

    def getBathymetryFilePath(self):
        return self.values[BATHYMETRY_FILE]

    def getHydrographsFilePath(self):
        return self.values[HYDROGRAPHS_FILE]

    def getRatingCurvesFilePath(self):
        return self.values[RATING_CURVE_FILE]

    def getManningFilePath(self):
        return self.values[MANNING_FILE]

    def getResultFolderPath(self):
        return self.values[RESULT_PATH]

    def getOutputMode(self):
        return self.values[OUTPUT_MODE]

    def getSimulationTime(self) -> float:
        return float(self.values[SIMULATION_TIME])

    def getDeltaToWrite(self) -> float:
        return float(self.values[DELTA_TO_WRITE])

    def isDeltaAdaptive(self) -> bool:
        return bool(self.values[IS_DELTA_ADAPTIVE])

    def getDefaultDelta(self) -> float:
        return float(self.values[DEFAULT_DELTA])
