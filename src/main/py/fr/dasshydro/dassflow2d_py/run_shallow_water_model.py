# imports
import input.Configuration as cfg
from input.MeshReader import MeshReader
from mesh.Mesh import MeshType, MeshShape
from resolution.ResolutionMethod import TemporalScheme, SpatialScheme, ResolutionMethod


def get_mesh_reader(mesh_type: MeshType, mesh_shape: MeshShape) -> MeshReader:
    """
    Decide what MeshReader to use based on mesh type and shape

    
    """
    if mesh_type == MeshType.DASSFLOW:
        import input.DassflowMeshReader
        return input.DassflowMeshReader()
    else:
        raise NotImplementedError("Not yet implemented.")


def get_resolution_method(temporal_scheme: TemporalScheme, spatial_scheme: SpatialScheme) -> ResolutionMethod:
    if temporal_scheme == TemporalScheme.EULER:

        if spatial_scheme == SpatialScheme.FIRST:

            # TODO: configure euler time step here (porosity, infiltration...)
            from resolution.EulerTimeStep import EulerTimeStep
            return EulerTimeStep()
        
        elif spatial_scheme == SpatialScheme.MUSCL:

            raise NotImplementedError("Euler with MUSCL spatial scheme is not yet implemented.")
        
    elif temporal_scheme == TemporalScheme.RK2:

        if spatial_scheme == SpatialScheme.FIRST:

            raise NotImplementedError("RK2 with FIRST spatial scheme is not yet implemented.")
        
        elif spatial_scheme == SpatialScheme.MUSCL:
            
            raise NotImplementedError("RK2 with MUSCL spatial scheme is not yet implemented.")


def run_shallow_water_model(temporal_scheme: TemporalScheme,
                            spatial_scheme: SpatialScheme,
                            input_folder_path: str,
                            configuration_file: str,
                            mesh_file: str):
    """
    Configure and run the shallow water model using data from the specified input folder.

    This function is responsible for setting up any necessary data required for the shallow water model and then executing the
    model using the configured data.

    :param str input_folder_path: The path to the folder containing the input files for the shallow water model.
        This folder is assumed to contains all information necessary for the shallow water model to run
    :param str configuration_file: The name of the file inside the input folder path that represent the configuration file.
    :raises: NotImplementedError: This function is not implemented yet and will raise a NotImplementedError when called.
    """

    configuration = cfg.load_from_file(f"{input_folder_path}/{configuration_file}")
    mesh_type = configuration.getMeshType()
    mesh_shape = configuration.getMeshShape()
    mesh_reader = get_mesh_reader(mesh_type, mesh_shape)
    incomplete_mesh = mesh_reader.read(f"{input_folder_path}/{mesh_file}")

    mesh = incomplete_mesh.complete()

    # Instantiate used resolution method based on parameters
    resolution_method = get_resolution_method(
        temporal_scheme,
        spatial_scheme
        # later optional configuration inputs will go here (like infiltration_file)
    )

    # TODO: Initialise first time step state

    # TODO: Iterative call loop will go here


import argparse
from resolution.ResolutionMethod import TemporalScheme, SpatialScheme

def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(description="Process a folder path")

    parser.add_argument(
        "temporal_scheme",
        type=str, choices=["euler", "rk2"],
        help="Which temporal scheme for resolution method to use"
    )

    parser.add_argument(
        "spatial_scheme",
        type=str, choices=["first", "muscl"],
        help="Which spatial scheme for resolution method to use"
    )

    parser.add_argument(
        "--folder_path", "-i",
        type=str,
        help="Path to the folder containing input files",
        default="inputs", required=False
    )

    parser.add_argument(
        "--configuration-file", "-c",
        type=str,
        help="Configuration file name",
        default="input.txt", required=False
    )

    parser.add_argument(
        "--mesh-file", "-m",
        type=str,
        help="Mesh file name",
        default="mesh.geo", required=False
    )

    args = parser.parse_args()

    # Run model with parsed values
    try:
        temporal_scheme = TemporalScheme(args.temporal_scheme)
        spatial_scheme = SpatialScheme(args.spatial_scheme)
    except ValueError as e:
        print(e)
        return None
    
    run_shallow_water_model(
        temporal_scheme,
        spatial_scheme,
        args.folder_path,
        args.configuration_file,
        args.mesh_file
    )

if __name__ == "__main__":
    main()
