import argparse

from fr.dasshydro.dassflow2d_py.input.Configuration import Configuration, load_from_file
from fr.dasshydro.dassflow2d_py.ShallowWaterModel import ShallowWaterModel, LoopListener


def main():
    args_name = []
    # Setup argument parser
    parser = argparse.ArgumentParser(description="Process a folder path")

    parser.add_argument(
        "--config-file", "-c",
        type=str,
        help="Configuration file path",
        default="inputs/config.yaml",
        required=True
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
    configuration = load_from_file(args.config_file)

    # Update configuration values with command line arguments
    configuration_values = {}
    for arg_name in args_name:
        arg_value = getattr(args, arg_name)
        if arg_value is not None:
            configuration_values[arg_name] = arg_value

    configuration.updateValues(configuration_values)

    shallow_water_model = ShallowWaterModel(configuration)

    """
    EXAMPLE LISTENER USE CASE
    class PrintLoopListener(LoopListener):
        def endOfLoop(self, current_delta, current_state, current_simulation_time):
            print(current_simulation_time)

    loop_listener = PrintLoopListener()

    shallow_water_model.subscribe(loop_listener)
    """

    shallow_water_model.run()

if __name__ == "__main__":
    main()
