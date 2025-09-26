from fr.dasshydro.dassflow2d_py.resolution.ResolutionMethod import ResolutionMethod
from fr.dasshydro.dassflow2d_py.input.Configuration import Configuration

class EulerHLLC(ResolutionMethod):

    def __init__(self, configuration: Configuration):
        pass

    def resolve(self, previous_time_step, delta, mesh, bathymetry):
        """
        Implements a resolution method using euler time scheme and the hllc solver
        """
        return previous_time_step