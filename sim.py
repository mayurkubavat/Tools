#!/usr/bin/env python3
"""A script to compile, simulate, and clean SystemVerilog projects using Xilinx tools."""
import os
from os import system
import argparse

DEFAULT_TOP_MODULE ='top'

parser = argparse.ArgumentParser( # type: ignore
  description='Compiles and simulates SystemVerilog designs, or cleans generated files.'
) # type: ignore

parser.add_argument( # type: ignore
  '--clean',
  action='store_true',
  help='Clean simulation-generated files and directories.'
) # type: ignore
parser.add_argument( # type: ignore
  '--top',
  type=str,
  default=DEFAULT_TOP_MODULE,
  help=f'Specify top-level module name. Used for elaboration and for the default file list if --filelist or --sv is not provided. (default: {DEFAULT_TOP_MODULE})'
) # type: ignore
parser.add_argument( # type: ignore
  '--filelist',
  type=str,
  help='Specify the Verilog file list (.f file). Overrides --sv and the default <top>.f.'
)
parser.add_argument( # type: ignore
  '--sv',
  type=str,
  help="Specify SystemVerilog source files or pattern (e.g., '*.sv', 'src/*.sv'). Used if --filelist is not provided. Overrides the default <top>.f."
)

args = parser.parse_args()

# Determine the source specification for compilation
compile_source = ""
if args.filelist:
    compile_source = f"-f {args.filelist}"
elif args.sv:
    compile_source = args.sv
else:
  # If neither --filelist nor --sv is provided and not cleaning, it's an error.
  parser.error("Either --filelist or --sv must be provided.")

def build():
  """Compiles the specified SystemVerilog source files."""
  system(f'xvlog -work work -sv {compile_source}')


def sim():
  """Elaborates the design and runs the simulation for the specified top module."""

  system(f'xelab work.{args.top} -R')


def clean():
  """Removes simulation-generated files and directories."""

  print("Cleaning simulation files...")
  system('rm -rf xsim.dir *.log *.pb *.jou')


def main():
  """Main execution flow: either cleans or builds and simulates."""

  if args.clean:
    clean()
  else:
    build()
    sim()


if __name__ == '__main__':
  main()
