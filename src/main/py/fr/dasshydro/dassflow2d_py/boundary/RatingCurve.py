from dassflow2d_py.boundary.DynamicBoundaryCondition import DynamicBoundaryCondition

from dassflow2d_py.input.Configuration import Configuration
from dassflow2d_py.mesh.Mesh import Boundary, BoundaryType
from dassflow2d_py.d2dtime.TimeStepState import TimeStepState, Node
from dassflow2d_py.input.file_reading import extract, next_line

class RatingCurve(DynamicBoundaryCondition):
    def __init__(self, configuration: Configuration, boundaries, *args):
        super().__init__(configuration, boundaries, configuration.getRatingCurvesFilePath, *args)

    def getBoundaryType(self) -> BoundaryType:
        return BoundaryType.OUTFLOW

    def update(self, bathymetry, current_state: TimeStepState, current_simulation_time: float):
        """Update the boundary condition."""

        q_out = self.interpolate_dynamic_value(current_simulation_time)

        # Compute sum_pow_h
        sum_pow_h = 0.0
        for boundary in self.boundaries:
            h = current_state.getNode(boundary.getEdge().getGhostCell()).h
            h = max(0.0001, h)  # Avoid zero or negative values
            sum_pow_h += (h ** (5/3)) * boundary.getEdge().getLength()

        # Distribute q_out across boundaries
        for boundary in self.boundaries:
            h = current_state.getNode(boundary.getEdge().getGhostCell()).h
            h = max(0.0001, h)
            outflow = q_out * (h ** (2/3)) / sum_pow_h
            current_state.getNode(boundary.getEdge().getGhostCell()).u = outflow
