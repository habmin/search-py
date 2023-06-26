import re
import sys
import pathlib
import os
import argparse
import datetime
class SearchToMd:
    def __init__(self,
                 root_dir,
                 output_file, 
                 search_terms = ["created_at", "updated_at", "deleted_at"], 
                 exceptions = [".git", ".github", ".husky", "data", "migrations", "diagrams", "docker", "fixture", "node_modules", "vendor", "storage"],
                 open = False):
        self.root_dir = root_dir
        self.output_file = output_file
        self.search_terms = search_terms
        self.exceptions = exceptions
        self.open = open

        self.output_file.write(f"# Searching in {self.root_dir.name}/\n\n")

        self.output_file.write(f"## Searching terms\n")
        for term in self.search_terms:
            self.output_file.write(f" - {term}\n")

        
        self.output_file.write("## Ignored directories\n")
        for exception in self.exceptions:
            self.output_file.write(f" - {exception}\n")

        for term in self.search_terms:
            self.output_file.write(f"# {term}\n\n")
            self.parse_files(self.root_dir, term, self.output_file)
            self.output_file.write("\n")

        self.output_file.close()

    def dirpath_to_md(self, dirpath_str, counter, f):
        dirpath_str = re.sub(str(self.root_dir), "", dirpath_str)
        open = "open" if self.open else ""
        f.write(f"<details {open}>\n<summary><b>{dirpath_str} ({counter})</b></summary>\n\n")

    def filename_to_mid(self, filename_str, f):
        f.write(f" - {filename_str}\n")

    def parse_files(self, root_dir, term, f):
        for child in os.scandir(root_dir):
            if child.name in self.exceptions:
                continue
            if child.is_dir():
                self.parse_files(child.path, term, f)
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
                        self.dirpath_to_md(child.path, counter, f)
                        f.write(f"{lines_string}\n</details>\n\n")
                    file.close()

                except UnicodeDecodeError:
                    pass

# Checks if input is a valid directory and converts to posix.path
def abs_path_check(string_input):
    if os.path.isdir(string_input):
        return pathlib.Path(string_input).absolute()
    else:
        raise NotADirectoryError(string_input)
    
def return_file(string_input):
    os.makedirs(f"{os.getcwd()}/results", exist_ok = True)
    output_dir = f"{os.getcwd()}/results"
    if string_input:
        string_input = re.sub(r"/","-", string_input)
        if re.findall(r".md$", string_input):
            return open(f"{output_dir}/{string_input}", "w+")
        else:
            return open(f"{output_dir}/{string_input}.md", "w+")
    else:
        time = datetime.datetime.now()
        filename = f"Results-{time.year}-{time.month}-{time.day}-{time.hour}:{time.minute}:{time.second}.md"
        return open(f"{output_dir}/results/{filename}", "w+")

def driver(*args, **kwargs):
    parser = argparse.ArgumentParser(description = "Find matching string in directory/files and output where they're found into markdown")
    parser.add_argument(dest = 'path', type = abs_path_check)
    parser.add_argument("--open", dest = 'open', action = 'store_true')
    parser.add_argument("-o", "--output", dest = "output", type = return_file, default = "")
    
    args = parser.parse_args()

    SearchToMd(args.path, args.output, open = args.open)

if __name__ == '__main__':
    driver(*sys.argv)