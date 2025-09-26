from dassflow2d_py.boundary.BoundaryCondition import BoundaryCondition

from dassflow2d_py.mesh.Mesh import Cell, Boundary, BoundaryType
from dassflow2d_py.d2dtime.TimeStepState import TimeStepState


class Wall(BoundaryCondition):
    def __init__(self, configuration, boundaries: list[Boundary], *args):
        super().__init__(configuration, boundaries, *args)

    def getBoundaryType(self) -> BoundaryType:
        return BoundaryType.WALL

    def update(self, bathymetry: dict[Cell, float], current_state: TimeStepState, current_simulation_time: float):
        """
        Update the boundary condition for a wall.
        For a wall, the right state is a reflection of the left state:
        - hR = hL + zL - zR
        - uR = -uL
        - vR = vL
        """
        for boundary in self.boundaries:
            edge = boundary.getEdge()
            ghost_cell = edge.getGhostCell()
            left_cell = edge.getCells()[0]  # Assuming the left cell is the first cell

            # Get left cell values
            hL = current_state.getNode(left_cell).h
            uL = current_state.getNode(left_cell).u
            vL = current_state.getNode(left_cell).v
            zL = bathymetry[left_cell]
            zR = bathymetry[ghost_cell]

            # Calculate right cell values for wall boundary
            hR = hL + zL - zR
            uR = -uL
            vR = vL

            # Update ghost cell values
            current_state.getNode(ghost_cell).h = hR
            current_state.getNode(ghost_cell).u = uR
            current_state.getNode(ghost_cell).v = vR