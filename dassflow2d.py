import sys
import os

# Add src/main/py to sys.path at the beginning of the script
src_path = os.path.join('src', 'main', 'py')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

import argparse
from enum import Enum, auto

from fr.dasshydro.dassflow2d_py.input.Configuration import Configuration
from fr.dasshydro.dassflow2d_py.ShallowWaterModel import ShallowWaterModel, LoopListener


# Define an enum for configuration sources
class ConfigSource(Enum):
    DEFAULT = auto()
    CONFIG_FILE = auto()
    COMMAND_ARGS = auto()


# ANSI color codes for printing
COLORS = {
    ConfigSource.DEFAULT: "\033[93m",     # Yellow
    ConfigSource.CONFIG_FILE: "\033[94m", # Blue
    ConfigSource.COMMAND_ARGS: "\033[92m" # Green
}
RESET_COLOR = "\033[0m"


def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(description="Process a folder path")
    args_fields = [
        ("config_file", ("--config-file", "-c"), "Configuration file path", None, True),
        ("temporal_scheme", ("--temporal-scheme", "-ts"), "Temporal scheme for resolution method", ["euler", "ssp-rk2", "imex"], False),
        ("spatial_scheme", ("--spatial-scheme", "-ss"), "Spatial scheme for resolution method", ["hllc", "muscl", "low-froude"], False),
        ("mesh_file", ("--mesh-file", "-mf"), "Mesh file path", None, False),
        ("boundary_condition_file", ("--boundary-condition-file", "-bcf"), "Boundary condition description file path", None, False),
        ("initial_state_file", ("--initial-state-file", "-isf"), "Initial state file path", None, False),
        ("bathymetry_file", ("--bathymetry-file", "-bf"), "Bathymetry file path UNUSED", None, False),
        ("hydrographs_file", ("--hydrographs-file", "-hf"), "Hydrographs file path", None, False),
        ("rating_curve_file", ("--rating-curve-file", "-rcf"), "Rating curves file path", None, False),
        ("manning_file", ("--manning-file", "-mnf"), "Manning file path UNUSED", None, False),
        ("result_path", ("--result-path", "-rp"), "Result folder path", None, False),
        ("output_mode", ("--output-mode", "-om"), "Output mode", ["vtk", "tecplot", "gnuplot", "hdf5"], False),
        ("simulation_time", ("--simulation-time", "-st"), "Total simulation duration", None, False),
        ("delta_to_write", ("--delta-to-write", "-dtw"), "Time needed to write a snapshot of the state", None, False),
        ("is_delta_adaptative", ("--is-delta-adaptative", "-da"), "Does delta time adapt to mesh", None, False),
        ("default_delta", ("--default-delta", "-dd"), "Default value of delta (in case of non-adaptive)", None, False)
    ]
    for arg_fields in args_fields:
        # unpack structure
        arg_namespace, arg_aliases, arg_help, arg_choices, arg_required = arg_fields
        parser.add_argument(*arg_aliases, help=arg_help, choices=arg_choices, required=arg_required)

    args = parser.parse_args()

    # Load configuration from file
    configuration = Configuration(ConfigSource.DEFAULT)

    configuration.update_from_file(args.config_file, ConfigSource.CONFIG_FILE)

    # Update configuration values with command line arguments
    configuration_values = {}
    for arg_fields in args_fields:
        arg_namespace = arg_fields[0]
        arg_value = getattr(args, arg_namespace)
        if arg_value is not None:
            configuration_values[arg_namespace] = arg_value

    configuration.updateValues(configuration_values, ConfigSource.COMMAND_ARGS)

    # Print where each parameters comes from
    max_param_length = max(len(param) for param in configuration.getSources().keys())
    for parameter_namespace, parameter_source in configuration.getSources().items():
        color = COLORS.get(parameter_source, "")
        reset = RESET_COLOR
        print(f"{parameter_namespace:<{max_param_length}} : {color}{parameter_source.name.replace('_', ' ').title()}{reset}")

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
