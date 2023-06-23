import re
import sys
import pathlib
import os
import argparse

def driver(*args, **kwargs):
    parser = argparse.ArgumentParser(description = "Find matching string in directory/files and output where they're found into markdown")
    parser.add_argument(dest='path', type = lambda p: pathlib.Path(p).absolute())
    
    args = parser.parse_args()

    print(args.path)

if __name__ == '__main__':
    driver(*sys.argv)