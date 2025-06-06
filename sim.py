#!/usr/bin/env python3
"""A script to compile, simulate, and clean SystemVerilog projects using Xilinx tools."""

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
  help=f'Specify top-level module name. Assumes <top>.f file list. (default: {DEFAULT_TOP_MODULE})'
)

args = parser.parse_args()


def build():
  """Compiles the SystemVerilog source files listed in <top>.f."""

  system(f'xvlog -work work -sv -f {args.top}.f')


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
