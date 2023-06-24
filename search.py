import re
import sys
import pathlib
import os
import argparse

REG_EX=r"created_at"
exceptions = [".git", "data", "migrations", "diagrams", "docker", "fixture", "node_modules", "vendor", "storage"]

# Checks if input is a valid directory and converts to posix.path
def abs_path_check(string_input):
    if os.path.isdir(string_input):
        return pathlib.Path(string_input).absolute()
    else:
        raise NotADirectoryError(string_input)

def parse_files(root_dir):
    for child in os.scandir(root_dir):
        if child.name in exceptions:
            continue
        if child.is_dir():
            # print(indent, "* Dirc: ", child.path)
            parse_files(child.path)
        else:
            # print("- File: ", child.path)
            try:
                file = open(child.path, "r")
                for i, line in enumerate(file):
                    if re.search(REG_EX, line):
                        print(f"In file {child.path}")
                        print(f"{i}: {line}")
            except UnicodeDecodeError:
                pass



def driver(*args, **kwargs):
    parser = argparse.ArgumentParser(description = "Find matching string in directory/files and output where they're found into markdown")
    parser.add_argument(dest = 'path', type = abs_path_check)
    
    args = parser.parse_args()

    parse_files(args.path)

if __name__ == '__main__':
    driver(*sys.argv)