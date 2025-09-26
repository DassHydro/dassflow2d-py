from dassflow2d_py.boundary.DynamicBoundaryCondition import DynamicBoundaryCondition

from dassflow2d_py.input.file_reading import extract, next_line
from dassflow2d_py.input.Configuration import Configuration
from dassflow2d_py.mesh.Mesh import Boundary, BoundaryType, Cell
from dassflow2d_py.d2dtime.TimeStepState import TimeStepState

class Discharge1(DynamicBoundaryCondition):
    def __init__(self, configuration: Configuration, boundaries: list[Boundary], *args):
        super().__init__(configuration, boundaries, configuration.getHydrographsFilePath, *args)

    def getBoundaryType(self) -> BoundaryType:
        return BoundaryType.INFLOW

    def update(self, bathymetry, current_state: TimeStepState, current_simulation_time: float):
        """
        Distribute the interpolated q_in value to each boundaries in the list
        """

        q_in = self.interpolate_dynamic_value(current_simulation_time)

        # Compute
        sum_pow_h = 0.0
        for boundary in self.boundaries:
            edge = boundary.getEdge()
            cell = edge.getCells()[0]
            h = current_state.getNode(cell).h
            h = max(0.0001, h)  # Avoid zero or very small values
            sum_pow_h += (h ** (5/3)) * edge.getLength()

        for boundary in self.boundaries:
            edge = boundary.getEdge()
            cell = edge.getCells()[0]
            h = current_state.getNode(cell).h
            h = max(0.0001, h)  # Avoid zero or very small values
            inflow = -q_in * (h ** (2/3)) / sum_pow_h
            # Update the ghost cell's u (discharge) value
            ghost_cell = edge.getGhostCell()
            ghost_cell_node = current_state.getNode(ghost_cell)
            edge_normal = edge.getNormalVector()
            ghost_cell_node.u = edge_normal[0] * inflow - edge_normal[1] * ghost_cell_node.v
            ghost_cell_node.v = edge_normal[1] * inflow - edge_normal[0] * ghost_cell_node.v
