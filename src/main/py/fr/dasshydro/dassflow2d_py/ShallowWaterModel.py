from abc import ABC, abstractmethod

# input
from fr.dasshydro.dassflow2d_py.input.Configuration import Configuration
from fr.dasshydro.dassflow2d_py.input.MeshReader import MeshReader
from fr.dasshydro.dassflow2d_py.input.InitialStateReader import InitialStateReader
# output
from fr.dasshydro.dassflow2d_py.output.ResultWriter import ResultWriter

# mesh and geometry context
from fr.dasshydro.dassflow2d_py.mesh.Mesh import Cell, Boundary, RawInlet, RawOutlet
from fr.dasshydro.dassflow2d_py.mesh.MeshImpl import MeshImpl
from fr.dasshydro.dassflow2d_py.boundary.BoundaryCondition import createBoundaryConditions

# time and state
import fr.dasshydro.dassflow2d_py.d2dtime.delta as dt
from fr.dasshydro.dassflow2d_py.d2dtime.TimeStepState import TimeStepState, Node

# resolution (a lot is in dynamic imports)
from fr.dasshydro.dassflow2d_py.resolution.ResolutionMethod import ResolutionMethod, TemporalScheme, SpatialScheme


class LoopListener(ABC):

    @abstractmethod
    def endOfLoop(self, current_delta: float, current_state: TimeStepState, current_simulation_time: float):
        """
        Gets triggered when a loop has ended

        Args:
            current_delta (float): delta used in for resolution
            current_state (TimeStepState): state result of the loop
            current_simulation_time (float): simulation time at this loop end
        """
        pass


class ShallowWaterModel:

    def __init__(self, configuration: Configuration):
        """
        Configure and run the shallow water model using data from the specified input folder.

        This function is responsible for setting up any necessary data required for the shallow water model and then executing the
        model using the configured data.

        :param Configuration configuration: Configuration of the launch
        :raises: NotImplementedError: This function is not implemented yet and will raise a NotImplementedError when called.
        """

        self.loop_listeners: list[LoopListener] = []

        ####################### Reading #######################

        # Read mesh
        mesh_reader = self._get_mesh_reader()
        mesh_file = configuration.getMeshFile()
        raw_info = mesh_reader.read(mesh_file)
        raw_mesh_info = raw_info[:4]

        # Read bathymetry
        _, cell_bathymetry = raw_info[4:6]

        # Read first time step state
        initial_state_reader = InitialStateReader()
        initial_state_file = configuration.getInitialStateFile()

        ##################### Initialize ######################

        ### Create the mesh
        boundary_origin: dict[Boundary, RawInlet|RawOutlet] = {}
        mesh = MeshImpl.createFromPartialInformation(*(*raw_mesh_info, boundary_origin))
        self.mesh = mesh

        ### Create boundary condition
        # create boundary groups
        boundary_groups = {}
        for boundary in mesh.getBoundaries():
            raw_boundary = boundary_origin.get(boundary)
            if raw_boundary is None:
                boundary_groups[boundary] = 0
            else:
                boundary_groups[boundary] = raw_boundary.group_number

        self.boundary_conditions = createBoundaryConditions(
            configuration,
            mesh.getBoundaries(),
            boundary_groups
        )

        ### Create bathymetry dictionary
        bathymetry = {}

        # fill bathymetry dict with all cell's values
        for cell in mesh.getCells():
            bathymetry[cell] = cell_bathymetry[cell.getID()]

        # adds ghost cell bathymetry
        for boundary in mesh.getBoundaries():
            boundary_edge = boundary.getEdge()
            cell = boundary_edge.getCells()[0]
            ghost_cell = boundary_edge.getGhostCell()
            bathymetry[ghost_cell] = bathymetry[cell]

        # update ghost cell bathymetry for inflow and outflow
        for flow_boundary, raw_boundary in boundary_origin.items():
            boundary_edge = flow_boundary.getEdge()
            ghost_cell = boundary_edge.getGhostCell()
            bathymetry[ghost_cell] = raw_boundary.ghost_cell_bathymetry


        self.bathymetry = bathymetry

        ### Create initial state
        raw_initial_state = initial_state_reader.read(initial_state_file, mesh.getCellNumber())
        node_dictionary = {}
        for i, cell in enumerate(mesh.getCells()):
            node_dictionary[cell] = raw_initial_state[i]

        # fill state with empty node for ghost cells
        for boundary in mesh.getBoundaries():
            boundary_edge = boundary.getEdge()
            ghost_cell = boundary_edge.getGhostCell()
            node_dictionary[ghost_cell] = Node(0.0, 0.0, 0.0)

        self.initial_state = TimeStepState(node_dictionary)

        # Instantiate used resolution method based on parameters
        self.resolution_method = self._get_resolution_method(configuration)

        # Initialize time variables
        self.use_cfl = configuration.isDeltaAdaptative()
        self.default_delta = configuration.getDefaultDelta() # used only if not adaptative
        delta_to_write = configuration.getDeltaToWrite()

        # Instantiate result writer
        result_file_path = configuration.getResultFilePath()
        self.result_writer = ResultWriter(mesh, result_file_path, delta_to_write)

        # Initialize runner variables
        self.simulation_time = configuration.getSimulationTime()
        self.output_mode = configuration.getOutputMode()

    def _get_mesh_reader(self) -> MeshReader:
        """
        Get the correct implementation of Mesh reader according to the needs

        Returns:
            MeshReader: correct implementation of a mesh reader
        """

        from fr.dasshydro.dassflow2d_py.input.DassflowMeshReader import DassflowMeshReader
        return DassflowMeshReader()

    def _get_resolution_method(self, configuration: Configuration) -> ResolutionMethod:
        """
        Get the correct implementation of Mesh reader according to the needs

        Returns:
            MeshReader: correct implementation of a mesh reader
        """

        temporal_scheme = configuration.getTemporalScheme()
        spatial_scheme = configuration.getSpatialScheme()

        if temporal_scheme is TemporalScheme.EULER and spatial_scheme is SpatialScheme.HLLC:

            from fr.dasshydro.dassflow2d_py.resolution.EulerHLLC import EulerHLLC
            return EulerHLLC(configuration)

        else:

            raise NotImplementedError(f"Combination of {temporal_scheme} temporal scheme and {spatial_scheme} spatial scheme is not supported yet.")

    def subscribe(self, loop_listener: LoopListener):
        self.loop_listeners.append(loop_listener)

    def run(self):
        """
        Starts a run on the shallow water model
        """

        delta = self.default_delta
        current_simulation_time = 0.0
        current_state = self.initial_state

        # Iterative call loop
        while current_simulation_time < self.simulation_time:

            # update all boundary conditions
            for bc in self.boundary_conditions:
                bc.update(self.bathymetry, current_state, current_simulation_time)

            # get time step
            if self.use_cfl:
                delta = dt.get_delta_using_cfl(current_state, self.mesh)

            # resolve using resolution method
            current_state = self.resolution_method.resolve(current_state, delta, self.mesh, self.bathymetry)

            current_simulation_time += delta

            if self.result_writer.isTimeToWrite(current_simulation_time):

                self.result_writer.save(current_state, current_simulation_time)

            # call all end of loop listeners
            for listener in self.loop_listeners:
                listener.endOfLoop(delta, current_state, current_simulation_time)

        ############### Results post-treatment ################=

        self.result_writer.writeAll(self.output_mode)