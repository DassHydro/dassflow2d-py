from enum import Enum

class TemporalScheme(Enum):
    EULER = "euler"
    SSP_RK2 = "ssp-rk2"
    IMEX = "imex"

class SpatialScheme(Enum):
    HLLC = "hllc"
    MUSCL = "muscl"
    LOW_FROUDE = "low-froude"

from abc import ABC, abstractmethod
from fr.dasshydro.dassflow2d_py.d2dtime.TimeStepState import TimeStepState
from fr.dasshydro.dassflow2d_py.mesh.Mesh import Mesh, Cell

class ResolutionMethod(ABC):
    @abstractmethod
    def resolve(self, previous_time_step: TimeStepState, delta: float, mesh: Mesh, bathymetry: dict[Cell, float]) -> TimeStepState:
        pass
