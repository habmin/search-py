import re
import sys
import pathlib
import os
import argparse

REG_EX=r"created_at"
exceptions = [".git", ".github", ".husky", "data", "migrations", "diagrams", "docker", "fixture", "node_modules", "vendor", "storage"]
counter = 0
root_dir_str = ""

def dirpath_to_md(dirpath_str, f):
    global root_dir_str
    dirpath_str = re.sub(root_dir_str, "", dirpath_str)
    f.write(f"### {dirpath_str}\n\n")

def filename_to_mid(filename_str, f):
    f.write(f" - {filename_str}\n")

# Checks if input is a valid directory and converts to posix.path
def abs_path_check(string_input):
    if os.path.isdir(string_input):
        return pathlib.Path(string_input).absolute()
    else:
        raise NotADirectoryError(string_input)

def parse_files(root_dir, f):
    for child in os.scandir(root_dir):
        if child.name in exceptions:
            continue
        if child.is_dir():
            # dirpath_to_md(f"{child.path}", f)
            # print(indent, "* Dirc: ", child.path)
            parse_files(child.path, f)
        else:
            # print("- File: ", child.path)
            try:
                found = False
                lines_string = ""
                file = open(child.path, "r")
                for i, line in enumerate(file):
                    if re.search(REG_EX, line):
                        found = True
                        # dirpath_to_md(child.path, f)
                        lines_string += f" - Line {i}: `{line}`\n"
                        # print(f"{i}: {line}")
                        global counter
                        counter += 1
                if found:
                    dirpath_to_md(child.path, f)
                    f.write(lines_string)

            except UnicodeDecodeError:
                pass



def driver(*args, **kwargs):
    parser = argparse.ArgumentParser(description = "Find matching string in directory/files and output where they're found into markdown")
    parser.add_argument(dest = 'path', type = abs_path_check)
    
    args = parser.parse_args()

    f = open(r'TEST.md', 'w+')

    global root_dir_str
    root_dir_str = str(args.path)
    print(root_dir_str)

    parse_files(args.path, f)

    print(counter)

    f.close()

if __name__ == '__main__':
    driver(*sys.argv)