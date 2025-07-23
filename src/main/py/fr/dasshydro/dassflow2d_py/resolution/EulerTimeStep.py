from ResolutionMethod import ResolutionMethod
from input.Configuration import Configuration

class EulerTimeStep(ResolutionMethod):

    def __init__(self, configuration: Configuration):
        raise NotImplementedError("Not yet implemented.")
    
    def resolve(self, previous_time_step, mesh):
        raise NotImplementedError("Not yet implemented.")