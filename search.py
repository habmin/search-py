import re
import sys
import pathlib
import os
import argparse

SEARCH_TERMS=["created_at", "updated_at", "deleted_at"]
EXCEPTIONS = [".git", ".github", ".husky", "data", "migrations", "diagrams", "docker", "fixture", "node_modules", "vendor", "storage"]
ROOT_DIR_STR = ""

def dirpath_to_md(dirpath_str, counter, f):
    global ROOT_DIR_STR
    dirpath_str = re.sub(ROOT_DIR_STR, "", dirpath_str)
    f.write(f"<details open>\n<summary><b>{dirpath_str} ({counter})</b></summary>\n\n")

def filename_to_mid(filename_str, f):
    f.write(f" - {filename_str}\n")

# Checks if input is a valid directory and converts to posix.path
def abs_path_check(string_input):
    if os.path.isdir(string_input):
        return pathlib.Path(string_input).absolute()
    else:
        raise NotADirectoryError(string_input)

def parse_files(root_dir, term, f):
    for child in os.scandir(root_dir):
        if child.name in EXCEPTIONS:
            continue
        if child.is_dir():
            parse_files(child.path, term, f)
        else:
            try:
                lines_string = ""
                counter = 0
                file = open(child.path, "r")
                for i, line in enumerate(file):
                    if re.search(term, line):
                        # dirpath_to_md(child.path, f)
                        line = re.sub(r"^\s+|\s+$", "", line)
                        lines_string += f" - Line {i}: `{line}`\n"
                        # print(f"{i}: {line}")
                        counter += 1
                if lines_string:
                    dirpath_to_md(child.path, counter, f)
                    f.write(f"{lines_string}\n</details>\n\n")
                file.close()

            except UnicodeDecodeError:
                pass



def driver(*args, **kwargs):
    parser = argparse.ArgumentParser(description = "Find matching string in directory/files and output where they're found into markdown")
    parser.add_argument(dest = 'path', type = abs_path_check)
    
    args = parser.parse_args()

    f = open(r'TEST.md', 'w+')

    global ROOT_DIR_STR
    ROOT_DIR_STR = str(args.path)

    f.write(f"# Searching in {args.path.name}/\n\n")

    f.write(f"## Searching terms\n")
    for term in SEARCH_TERMS:
        f.write(f" - {term}\n")

    f.write("## Ignored directories\n")
    for exception in EXCEPTIONS:
        f.write(f" - {exception}\n")

    for term in SEARCH_TERMS:
        f.write(f"# {term}\n\n")
        parse_files(args.path, term, f)
        f.write("\n")

    f.close()

if __name__ == '__main__':
    driver(*sys.argv)