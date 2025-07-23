# imports
from input.Configuration import Configuration, load_from_file
from input.MeshReader import MeshReader
from mesh.Mesh import MeshType, MeshShape


def get_mesh_reader(configuration: Configuration) -> MeshReader:
    """
    Decide what MeshReader to use based on mesh type

    :param Configuration configuration: Configuration of the launch
    :return: An instance of MeshReader configured for the specified mesh type
    :rtype: MeshReader
    """
    mesh_type = configuration.getMeshType()
    if mesh_type == MeshType.DASSFLOW:

        from input.DassflowMeshReader import DassflowMeshReader
        return DassflowMeshReader()
    
    else:

        raise NotImplementedError("Not yet implemented.")


from resolution.ResolutionMethod import TemporalScheme, SpatialScheme, ResolutionMethod

def get_resolution_method(configuration: Configuration) -> ResolutionMethod:
    """
    Decide what ResolutionMethod to use based on temporal and spatial schemes

    :param Configuration configuration: Configuration of the launch
    :return: An instance of ResolutionMethod suited for selected schemes
    :rtype: ResolutionMethod
    """
    temporal_scheme = configuration.getTemporalScheme()
    spatial_scheme = configuration.getSpatialScheme()

    if temporal_scheme == TemporalScheme.EULER:

        if spatial_scheme == SpatialScheme.FIRST:

            # TODO: configure euler time step here (porosity, infiltration...)
            from resolution.EulerTimeStep import EulerTimeStep
            return EulerTimeStep(configuration)
        
        elif spatial_scheme == SpatialScheme.MUSCL:

            raise NotImplementedError("Euler with MUSCL spatial scheme is not yet implemented.")
        
    elif temporal_scheme == TemporalScheme.RK2:

        if spatial_scheme == SpatialScheme.FIRST:

            raise NotImplementedError("RK2 with FIRST spatial scheme is not yet implemented.")
        
        elif spatial_scheme == SpatialScheme.MUSCL:
            
            raise NotImplementedError("RK2 with MUSCL spatial scheme is not yet implemented.")


from input.InitialStateReader import InitialStateReader

def run_shallow_water_model(configuration: Configuration):
    """
    Configure and run the shallow water model using data from the specified input folder.

    This function is responsible for setting up any necessary data required for the shallow water model and then executing the
    model using the configured data.

    :param Configuration configuration: Configuration of the launch
    :raises: NotImplementedError: This function is not implemented yet and will raise a NotImplementedError when called.
    """
    mesh_reader = get_mesh_reader(configuration)
    mesh_file = configuration.getMeshFile()
    incomplete_mesh = mesh_reader.read(mesh_file)

    mesh = incomplete_mesh.complete()

    # Instantiate used resolution method based on parameters
    resolution_method = get_resolution_method(configuration)

    # Initialise first time step state
    initial_state_reader = InitialStateReader()
    initial_state_file = configuration.getInitialStateFile()
    initial_state = initial_state_reader.read(initial_state_file)

    # TODO: Iterative call loop will go here


import argparse

def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(description="Process a folder path")

    parser.add_argument(
        "--config", "-c",
        type=str,
        help="Configuration file path",
        default="inputs/config.yaml",
        required=False
    )

    parser.add_argument(
        "--mesh-type", "-mt",
        type=str,
        choices=["basic", "dassflow"],
        help="Temporal scheme for resolution method",
        required=False
    )

    parser.add_argument(
        "--mesh-shape", "-ms",
        type=str,
        choices=["triangular", "quadrilateral", "hybrid"],
        help="Temporal scheme for resolution method",
        required=False
    )

    parser.add_argument(
        "--mesh-file", "-m",
        type=str,
        help="Mesh file name",
        required=False
    )

    parser.add_argument(
        "--temporal-scheme", "-ts",
        type=str,
        choices=["euler", "rk2"],
        help="Temporal scheme for resolution method",
        required=False
    )

    parser.add_argument(
        "--spatial-scheme", "-ss",
        type=str,
        choices=["first", "muscl"],
        help="Spatial scheme for resolution method",
        required=False
    )

    args = parser.parse_args()

    # Load configuration from file
    configuration = load_from_file(args.config)

    # Set configuration values using setters
    if args.mesh_type:
        configuration.setMeshType(MeshType(args.mesh_type))

    if args.mesh_shape:
        configuration.setMeshShape(MeshShape(args.mesh_shape))

    if args.temporal_scheme:
        configuration.setTemporalScheme(TemporalScheme(args.temporal_scheme))

    if args.spatial_scheme:
        configuration.setSpatialScheme(SpatialScheme(args.spatial_scheme))

    if args.mesh_file:
        configuration.setMeshFile(args.mesh_file)

    run_shallow_water_model(configuration)

if __name__ == "__main__":
    main()
