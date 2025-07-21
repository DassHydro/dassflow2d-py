from enum import Enum

class TemporalScheme(Enum):
    EULER = "euler"
    RK2 = "rk2"

class SpatialScheme(Enum):
    FIRST = "first"
    MUSCL = "muscl"

from abc import ABC, abstractmethod
from resolution.TimeStepState import TimeStepState
from mesh.Mesh import Mesh

class ResolutionMethod(ABC):
    @abstractmethod
    def resolve(self, previous_time_step: TimeStepState, mesh: Mesh) -> TimeStepState:
        pass
