import re
import sys
import pathlib
import os
import argparse

# Checks if input is a valid directory and converts to posix.path
def abs_path_check(string_input):
    if os.path.isdir(string_input):
        return pathlib.Path(string_input).absolute()
    else:
        raise NotADirectoryError(string_input)

def parse_files(root_dir, indent):
    for child in os.scandir(root_dir):
        if child.name == ".git":
            continue
        if child.is_dir():
            print(indent, "* Dirc: ", child.path)
            indent += " "
            parse_files(child.path, indent)
        else:
            print(indent, "- File: ", child.path)

def driver(*args, **kwargs):
    parser = argparse.ArgumentParser(description = "Find matching string in directory/files and output where they're found into markdown")
    parser.add_argument(dest = 'path', type = abs_path_check)
    
    args = parser.parse_args()

    parse_files(args.path, "")

if __name__ == '__main__':
    driver(*sys.argv)