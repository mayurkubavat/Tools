#!/usr/bin/env python3

"""Compiles and runs a SystemC/UVM-SystemC simulation.

This script takes a specification file as input, which defines project-specific
include paths. It then uses environment variables for SystemC and UVM-SystemC
home directories to construct compiler and linker flags, compiles the
specified C++ source file, and runs the resulting simulation executable
after adjusting its execution stack properties.
"""

import os
import subprocess
import argparse
import importlib.util
import sys


COMPILER = "g++"
EXECSTACK_TOOL = "execstack"
SIM_EXECUTABLE_NAME = "sim"
CONFIG_MODULE_NAME = "project_config"

SYSTEMC_HOME = os.getenv("SYSTEMC_HOME")
UVM_SYSTEMC_HOME = os.getenv("UVM_SYSTEMC_HOME")

SYSTEMC_LIBS_DIR = f"{SYSTEMC_HOME}/lib-linux64"
UVM_SYSTEMC_LIBS_DIR = f"{UVM_SYSTEMC_HOME}/lib-linux64"
SYSTEMC_INC_DIR = f"{SYSTEMC_HOME}/include"
UVM_SYSTEMC_INC_DIR = f"{UVM_SYSTEMC_HOME}/include"


def _parse_arguments():
    """Parses command-line arguments for the script."""
    parser = argparse.ArgumentParser(description="Compile and run SystemC/UVM-SystemC simulation.")
    parser.add_argument(
        "--spec",
        dest="spec",
        required=True,
        help="Path to the Python configuration script for project-specific paths (e.g., spec.py).")
    return parser.parse_args()


def _compile(inc_paths_list, main_source_file):
    """Builds the compilation command and executes it, using global constants."""
    compile_cmd = [
        COMPILER,
        "-I.",  # Include current directory
        *inc_paths_list,
        f"-I{SYSTEMC_INC_DIR}", f"-I{UVM_SYSTEMC_INC_DIR}",
        "-L.",  # Link with libraries in current directory
        f"-L{SYSTEMC_LIBS_DIR}", f"-L{UVM_SYSTEMC_LIBS_DIR}",
        main_source_file,
        "-o",
        SIM_EXECUTABLE_NAME,
        "-lsystemc",
        "-luvm-systemc",
        "-lm"
    ]
    # Print the command for verification (optional)
    # print(f"Compile command: {' '.join(compile_cmd)}")

    print(f"Compiling with: {' '.join(compile_cmd)}")
    subprocess.run(compile_cmd, check=True)
    print("Compilation successful.")


def _simulate():
    """Runs execstack and then executes the compiled simulation."""
    run_sim_cmd = [f"./{SIM_EXECUTABLE_NAME}"]

    print(f"Running simulation: {' '.join(run_sim_cmd)}")
    subprocess.run(run_sim_cmd, check=True)
    print("Simulation run successful.")


def _parse_spec(spec_file_path, config_module_name):
    """Loads and parses the specification file."""
    spec_loader = importlib.util.spec_from_file_location(config_module_name, spec_file_path)
    config_module = importlib.util.module_from_spec(spec_loader)
    spec_loader.loader.exec_module(config_module)

    project_inc_paths_str = getattr(config_module, "INC_PATHS", "")
    main_source_file_config = getattr(config_module, "MAIN_SOURCE_FILE", "")
    inc_paths_list = project_inc_paths_str.split()
    return project_inc_paths_str, main_source_file_config, inc_paths_list


def main():
    args = _parse_arguments()

    _, MAIN_SOURCE_FILE_CONFIG, INC_PATHS_LIST = _parse_spec(args.spec, CONFIG_MODULE_NAME)

    # Compile the simulation
    _compile(INC_PATHS_LIST, MAIN_SOURCE_FILE_CONFIG)

    # Run the simulation
    _simulate()


if __name__ == "__main__":
    main()
