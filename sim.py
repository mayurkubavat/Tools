#!/usr/bin/env python3

from os import system

import argparse

#Get command line options
parser = argparse.ArgumentParser(description='')

#Get options from command
parser.add_argument('--clean', action='store_true', help='Clean LOGs..')
parser.add_argument('--top', type=str, default='testbench', help='Specify testbench name (default: testbench)')

args = parser.parse_args()


def build():
        system(f'xvlog -sv -f testbench.f')

def sim():
        system(f'xelab work.{args.top} -R')


def clean():
    system('rm -rf xsim.dir *.log *.pb *.jou *.log')


def main():
    if args.clean:
        clean()
    else:
        build()
        sim()


if __name__ == '__main__':
    main()
