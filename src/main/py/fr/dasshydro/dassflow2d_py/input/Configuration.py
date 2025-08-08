from fr.dasshydro.dassflow2d_py.resolution.ResolutionMethod import TemporalScheme, SpatialScheme

class Configuration:
    """
    This class holds all configuration namespaces and link them to a corresponding getter.
    This class does not support data source resolution
    (i.e. it does not remember for each namespace, the source of the associated value)
    """

    # Define default values and valid namespaces at the same time
    DEFAULT = {
        'temporal-scheme': 'euler',
        'spatial-scheme': 'first',
        'mesh-file': 'mesh.geo',
        'initial-state-file': 'dof_init.txt',
        'bathymetry-file': 'bathymetry.txt',
        'manning-file': 'manning.txt',
        'result-path': 'output/',
        'simulation-time': '10000',
        'delta-to-write': '100',
        'is-delta-adaptative': 'False',
        'default-delta': '0.01'
    }

    def __init__(self):
        raise NotImplementedError("Not yet implemented.")

    def getTemporalScheme(self) -> TemporalScheme:
        raise NotImplementedError("Not yet implemented.")

    def getSpatialScheme(self) -> SpatialScheme:
        raise NotImplementedError("Not yet implemented.")
    
    def getMeshFile(self) -> str:
        raise NotImplementedError("Not yet implemented.")
    
    def getInitialStateFile(self) -> str:
        raise NotImplementedError("Not yet implemented.")

    def getBathymetryFile(self) -> str:
        raise NotImplementedError("Not yet implemented.")

    def getManningFile(self) -> str:
        raise NotImplementedError("Not yet implemented.")
    
    def getResultFilePath(self) -> str:
        raise NotImplementedError("Not yet implemented.")
    
    def getSimulationTime(self) -> float:
        raise NotImplementedError("Not yet implemented.")
    
    def getDeltaToWrite(self) -> float:
        raise NotImplementedError("Not yet implemented.")
    
    def isDeltaAdaptative(self) -> bool:
        raise NotImplementedError("Not yet implemented.")
    
    def getDefaultDelta(self) -> float:
        raise NotImplementedError("Not yet implemented.")
    
    def updateValues(self, values: dict[str, str]):
        raise NotImplementedError("Not yet implemented.")


def load_from_file(file_path: str) -> Configuration:
    raise NotImplementedError("Not yet implemented.")
