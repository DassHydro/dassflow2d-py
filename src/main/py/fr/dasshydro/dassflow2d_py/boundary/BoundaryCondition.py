from abc import ABC, abstractmethod
from typing import Type, Iterable, Sequence

from fr.dasshydro.dassflow2d_py.input.Configuration import Configuration
from fr.dasshydro.dassflow2d_py.input.file_reading import extract, next_line
from fr.dasshydro.dassflow2d_py.mesh.Mesh import Mesh, Cell, Boundary, BoundaryType
from fr.dasshydro.dassflow2d_py.d2dtime.TimeStepState import TimeStepState


class BoundaryCondition(ABC):

    def __init__(self, configuration: Configuration, boundaries: list[Boundary], *args):
        self.boundaries = boundaries

    @abstractmethod
    def getBoundaryType(self) -> BoundaryType:
        pass

    @abstractmethod
    def update(self, bathymetry: dict[Cell, float], current_state: TimeStepState, current_simulation_time: float):
        """
        Do all necessary operations for a boundary condition to correctly force it's condition

        Args:
            mesh (Mesh): mesh geometry
            bathymetry (dict[Cell, float]): bathymetry z for each cell
            current_state (TimeStepState): every node value in the simulation
            current_simulation_time (float): current simulation time at the call time of this function
        """
        pass


# implementations imports here ...
from fr.dasshydro.dassflow2d_py.boundary.Discharge1 import Discharge1
from fr.dasshydro.dassflow2d_py.boundary.RatingCurve import RatingCurve

default_boundary_condition_class: dict[str, Type[BoundaryCondition]] = {
    "discharg1": Discharge1,
    "ratcurve": RatingCurve
}


def createBoundaryConditions(
    configuration: Configuration,
    boundaries: Iterable[Boundary] | Sequence[Boundary],
    boundaries_group: dict[Boundary, int],
    boundary_condition_class: dict[str, Type[BoundaryCondition]] = default_boundary_condition_class
) -> list[BoundaryCondition]:
    """
    Create all boundary condition objects for all groups.

    Args:
        configuration (Configuration): configuration containing file paths needed
        boundaries (Iterable[Boundary]|Sequence[Boundary]): all boundaries object that will be linked to boundary conditions
        boundaries_group (dict[Boundary, int]): associated group for every boundary in boundaries

    Raises:
        NotImplementedError: A namespace contained in boundary condition file doesn't have an implementation

    Returns:
        list[BoundaryCondition]: all created boundary conditions
    """

    bc_filepath = configuration.getBoundaryConditionFile()

    # Step 1: Group boundaries by group number
    grouped_boundaries: dict[int, list[Boundary]] = {}

    for boundary in boundaries:

        # fill the lists for all group number
        boundary_group = boundaries_group[boundary]
        # get the list of the group, create it if it don't exists
        boundary_group_list = grouped_boundaries.setdefault(boundary_group, [])
        boundary_group_list.append(boundary)


    # Step 2: Read bc_file to map group numbers to boundary condition arguments
    boundary_condition_arguments: dict[int, tuple] = {}

    with open(bc_filepath, 'r') as bc_file:

        # first content line should be the number of boundary conditions
        boundary_conditions_number, = extract(bc_file, (int,))

        for _ in range(boundary_conditions_number):

            current_bc_line = next_line(bc_file)
            current_bc_arguments = current_bc_line.strip().split()
            group_number = int(current_bc_arguments[0])
            # store the whole line as "args" for the boundary condition
            boundary_condition_arguments[group_number] = tuple(current_bc_arguments)


    # Step 4: Create boundary conditions
    boundary_conditions: list[BoundaryCondition] = []

    for group_number, boundary_list in grouped_boundaries.items():

        bc_args = boundary_condition_arguments.get(group_number)
        # if a group is not specified in bc.txt, it is considered a wall
        bc_args = bc_args if bc_args is not None else (0, 'wall')
        # second argument in the line should be the boundary condition namespace
        bc_namespace = bc_args[1]
        # retrieve the associated class from namespace
        bc_class = boundary_condition_class.get(bc_namespace)
        # raise error if there is no implementation for that namespace
        if bc_class is None:
            raise NotImplementedError(f"{bc_namespace} Not yet implemented.")
        # finally, create and add the boundary condition
        new_boundary_condition = bc_class(configuration, boundary_list, *bc_args)
        boundary_conditions.append(new_boundary_condition)


    return boundary_conditions
