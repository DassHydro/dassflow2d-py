# imports

from fr.dasshydro.dassflow2d_py.input.Configuration import Configuration, load_from_file
from fr.dasshydro.dassflow2d_py.resolution.ResolutionMethod import TemporalScheme, SpatialScheme, ResolutionMethod

def get_resolution_method(configuration: Configuration) -> ResolutionMethod:
    """
    Decide what ResolutionMethod to use based on temporal and spatial schemes

    :param Configuration configuration: Configuration of the launch
    :return: An instance of ResolutionMethod suited for selected schemes
    :rtype: ResolutionMethod
    """
    temporal_scheme = configuration.getTemporalScheme()
    spatial_scheme = configuration.getSpatialScheme()

    if temporal_scheme == TemporalScheme.EULER and spatial_scheme == SpatialScheme.HLLC:

        # TODO: configure euler time step here (porosity, infiltration...)
        from fr.dasshydro.dassflow2d_py.resolution.EulerTimeStep import EulerTimeStep
        return EulerTimeStep(configuration)

    else:

        raise NotImplementedError("As for now, only Euler with HLLC is supported.")


from fr.dasshydro.dassflow2d_py.input.DassflowMeshReader import DassflowMeshReader
from fr.dasshydro.dassflow2d_py.input.CellBathymetryDict import CellBathymetryDict
from fr.dasshydro.dassflow2d_py.input.InitialStateReader import InitialStateReader
from fr.dasshydro.dassflow2d_py.output.ResultWriter import ResultWriter
from fr.dasshydro.dassflow2d_py.mesh.MeshImpl import MeshImpl
import fr.dasshydro.dassflow2d_py.d2dtime.delta as dt

def run_shallow_water_model(configuration: Configuration):
    """
    Configure and run the shallow water model using data from the specified input folder.

    This function is responsible for setting up any necessary data required for the shallow water model and then executing the
    model using the configured data.

    :param Configuration configuration: Configuration of the launch
    :raises: NotImplementedError: This function is not implemented yet and will raise a NotImplementedError when called.
    """

    ####################### Reading #######################

    # Read mesh
    mesh_reader = DassflowMeshReader()
    mesh_file = configuration.getMeshFile()
    raw_info = mesh_reader.read(mesh_file)
    raw_mesh_info = raw_info[:4]

    # Read bathymetry
    _, cell_bathymetry = raw_info[4:6]

    # Read first time step state
    initial_state_reader = InitialStateReader()
    initial_state_file = configuration.getInitialStateFile()
    initial_state = initial_state_reader.read(initial_state_file)

    ##################### Initialize ######################

    # Create the mesh
    mesh = MeshImpl.createFromPartialInformation(*raw_mesh_info)

    # Instantiate used resolution method based on parameters
    resolution_method = get_resolution_method(configuration)

    # Create bathymetry dictionary
    bathymetry = CellBathymetryDict(cell_bathymetry)

    # Initialize time variables
    use_cfl = configuration.isDeltaAdaptative()
    delta = configuration.getDefaultDelta() # used only if not adaptative
    delta_to_write = configuration.getDeltaToWrite()

    # Instantiate result writer
    result_file_path = configuration.getResultFilePath()
    result_writer = ResultWriter(mesh, result_file_path, delta_to_write)

    # Initialize runner variables
    current_state = initial_state
    simulation_time = configuration.getSimulationTime()
    current_simulation_time = 0.0

    ######################### Run #########################

    # Iterative call loop
    while current_simulation_time < simulation_time:
        # get time step
        if use_cfl:
            delta = dt.get_delta_using_cfl(current_state, mesh)

        # resolve using resolution method
        current_state = resolution_method.resolve(current_state, delta, mesh, bathymetry)

        current_simulation_time += delta

        if result_writer.isTimeToWrite(current_simulation_time):

            result_writer.save(current_state, current_simulation_time)

    ############### Results post-treatment ################

    output_mode = configuration.getOutputMode()

    result_writer.writeAll(output_mode)

import argparse

def main():
    args_name = []
    # Setup argument parser
    parser = argparse.ArgumentParser(description="Process a folder path")

    parser.add_argument(
        "--config-file", "-c",
        type=str,
        help="Configuration file path",
        default="inputs/config.yaml",
        required=False
    )
    args_name.append("config_file")

    parser.add_argument(
        "--mesh-type", "-mt",
        type=str,
        choices=["basic", "dassflow"],
        help="Temporal scheme for resolution method",
        required=False
    )
    args_name.append("mesh_type")

    parser.add_argument(
        "--mesh-shape", "-ms",
        type=str,
        choices=["triangular", "quadrilateral", "hybrid"],
        help="Temporal scheme for resolution method",
        required=False
    )
    args_name.append("mesh_shape")

    parser.add_argument(
        "--mesh-file", "-m",
        type=str,
        help="Mesh file name",
        required=False
    )
    args_name.append("mesh_file")

    parser.add_argument(
        "--temporal-scheme", "-ts",
        type=str,
        choices=["euler", "rk2"],
        help="Temporal scheme for resolution method",
        required=False
    )
    args_name.append("temporal_scheme")

    parser.add_argument(
        "--spatial-scheme", "-ss",
        type=str,
        choices=["first", "muscl"],
        help="Spatial scheme for resolution method",
        required=False
    )
    args_name.append("spatial_scheme")

    args = parser.parse_args()

    # Load configuration from file
    configuration = load_from_file(args.config)

    # Update configuration values with command line arguments
    configuration_values = {}
    for arg_name in args_name:
        arg_value = getattr(args, arg_name)
        if arg_value is not None:
            configuration_values[arg_name] = arg_value

    configuration.updateValues(configuration_values)

    run_shallow_water_model(configuration)

if __name__ == "__main__":
    main()
