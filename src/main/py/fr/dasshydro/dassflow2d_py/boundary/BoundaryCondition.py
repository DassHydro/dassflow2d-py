from abc import ABC, abstractmethod
from typing import Type, Callable

from fr.dasshydro.dassflow2d_py.input.Configuration import Configuration
from fr.dasshydro.dassflow2d_py.input.file_reading import extract, _next_line
from fr.dasshydro.dassflow2d_py.mesh.Mesh import Mesh, Cell, Boundary, BoundaryType
from fr.dasshydro.dassflow2d_py.d2dtime.TimeStepState import TimeStepState
from fr.dasshydro.dassflow2d_py.boundary.Discharge1 import Discharge1


class BoundaryCondition(ABC):

    def __init__(self, configuration: Configuration, boundaries: list[Boundary], *args):
        self.boundaries = boundaries

    @abstractmethod
    def getBoundaryType(self) -> BoundaryType:
        pass

    @abstractmethod
    def update(self, mesh: Mesh, bathymetry: dict[Cell, float], current_state: TimeStepState, current_simulation_time: float):
        pass


boundary_conditions_classes_from_namespace: dict[str, Type[BoundaryCondition]] = {
}

def createBoundaryConditions(
    configuration: Configuration,
    boundaries: list[Boundary],
    boundaries_group: dict[Boundary, int],
) -> list[BoundaryCondition]:
    
    bc_filepath = configuration.getBoundaryConditionFile()
    
    # Step 1: Group boundaries by group number
    grouped_boundaries: dict[int, list[Boundary]] = {}

    for boundary in boundaries:
        boundary_group = boundaries_group[boundary]
        boundary_group_list = grouped_boundaries.setdefault(boundary_group, [])
        boundary_group_list.append(boundary)

    # Step 2: Read bc_file to map group numbers to boundary condition arguments
    boundary_condition_arguments: dict[int, tuple] = {}

    with open(bc_filepath, 'r') as bc_file:
        boundary_conditions_number, = extract(bc_file, (int,))
        for _ in range(boundary_conditions_number):
            current_bc_line = _next_line(bc_file)
            current_bc_arguments = current_bc_line.strip().split()
            group_number = int(current_bc_arguments[0])
            boundary_condition_arguments[group_number] = tuple(current_bc_arguments)

    # Step 4: Create boundary conditions
    boundary_conditions: list[BoundaryCondition] = []

    for group_number, boundary_list in grouped_boundaries.items():

        bc_args = boundary_condition_arguments[group_number]
        bc_namespace = bc_args[1]
        boundary_condition_class = boundary_conditions_classes_from_namespace.get(bc_namespace)
        if boundary_condition_class is None:
            raise NotImplementedError("Not yet implemented.")
        new_boundary_condition = boundary_condition_class(configuration, boundary_list, bc_args)
        boundary_conditions.append(new_boundary_condition)

    return boundary_conditions
