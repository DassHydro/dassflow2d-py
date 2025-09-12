from fr.dasshydro.dassflow2d_py.resolution.ResolutionMethod import ResolutionMethod
from fr.dasshydro.dassflow2d_py.input.Configuration import Configuration

class EulerTimeStep(ResolutionMethod):

    def __init__(self, configuration: Configuration):
        raise NotImplementedError("Not yet implemented.")

    def resolve(self, previous_time_step, delta, mesh, bathymetry):
        raise NotImplementedError("Not yet implemented.")