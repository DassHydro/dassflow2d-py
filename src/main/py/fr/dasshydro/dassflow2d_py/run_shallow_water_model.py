# imports
import input.Configuration as cfg

def run_shallow_water_model(input_folder_path: str, configuration_file: str):
    """
    Configure and run the shallow water model using data from the specified input folder.

    This function is responsible for setting up any necessary data required for the shallow water model
    and then executing the model using the configured data.

    :param str input_folder_path: The path to the folder containing the input files for the shallow water model.
        This folder is assumed to contains all informations necessary for the shallow water model to run
    :param str configuration_file: The name of the file inside the input folder path that represent the configuration file.
    :raises: NotImplementedError: This function is not implemented yet and will raise a NotImplementedError when called.
    """
    configuration = cfg.load_from_file(f"{input_folder_path}/{configuration_file}")
    raise NotImplementedError("Not yet implemented.")

import argparse

def main():
    parser = argparse.ArgumentParser(description="Process a folder path")
    parser.add_argument("folder_path", type=str, help="Path to the folder containing input files")
    parser.add_argument("--configuration-file", "-c", type=str, help="Configuration file name", default="input.txt", required=False)

    args = parser.parse_args()
    input_folder_path = args.folder_path
    run_shallow_water_model(input_folder_path, args.configuration_file)

if __name__ == "__main__":
    main()