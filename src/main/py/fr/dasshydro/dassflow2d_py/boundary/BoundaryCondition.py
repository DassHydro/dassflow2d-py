from abc import ABC, abstractmethod

from fr.dasshydro.dassflow2d_py.input.Configuration import Configuration
from fr.dasshydro.dassflow2d_py.mesh.Mesh import Mesh, Cell, Boundary, BoundaryType
from fr.dasshydro.dassflow2d_py.d2dtime.TimeStepState import TimeStepState


class BoundaryCondition(ABC):

    def __init__(self, configuration: Configuration, boundaries: list[Boundary], *args):
        self.boundaries = boundaries

    @abstractmethod
    def getBoundaryType(self) -> BoundaryType:
        pass

    @abstractmethod
    def update(self, mesh: Mesh, bathymetry: dict[Cell, float], current_state: TimeStepState, current_simulation_time: float):
        pass


def createBoundaries(
    configuration: Configuration,
    boundaries: list[Boundary],
    boundaries_group: dict[Boundary, int],
) -> list[BoundaryCondition]:
    raise NotImplementedError("Not yet implemented.")
