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
from dassflow2d_py.d2dtime.TimeStepState import TimeStepState
from dassflow2d_py.mesh.Mesh import Mesh, Cell

class ResolutionMethod(ABC):
    @abstractmethod
    def resolve(self, previous_time_step: TimeStepState, delta: float, mesh: Mesh, bathymetry: dict[Cell, float]) -> TimeStepState:
        """
        Resolution call that should return a new (or modified) TimeStepState with corrected value

        Args:
            previous_time_step (TimeStepState): state at the time of call
            delta (float): time to skip to
            mesh (Mesh): geometry of the problem
            bathymetry (dict[Cell, float]): bathymetry of each cell (including ghost cells)

        Returns:
            TimeStepState: state after delta
        """
        pass
