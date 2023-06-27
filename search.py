import re
import sys
import pathlib
import os
import argparse
import datetime
class SearchToMd:
    def __init__(
        self,
        root_dir,
        output_file, 
        search_terms, 
        exceptions,
        open = False):
        
        self.root_dir = root_dir
        self.output_file = output_file
        self.search_terms = search_terms
        self.exceptions = exceptions
        self.open = open

        self.output_file.write(f"# Searching in {self.root_dir.name}/\n\n")

        self.output_file.write(f"## Search terms\n")
        for term in self.search_terms:
            if term:
                self.output_file.write(f" - {term}\n")

        
        self.output_file.write("\n## Ignored directories\n")
        for exception in self.exceptions:
            if exception:
                self.output_file.write(f" - {exception}\n")
        self.output_file.write("\n")

        for term in self.search_terms:
            if term:
                self.output_file.write(f"# {term}\n\n")
                self.parse_files(self.root_dir, term, self.output_file)
                self.output_file.write("\n")

        self.output_file.close()

    def dirpath_to_md(self, dirpath_str, counter, f):
        dirpath_str = re.sub(str(self.root_dir), "", dirpath_str)
        open = "open" if self.open else ""
        f.write(f"<details {open}>\n<summary><b>{dirpath_str} ({counter})</b></summary>\n\n")

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
                            line = re.sub(r"^\s+|\s+$", "", line)
                            lines_string += f" - Line {i}: `{line}`\n"
                            counter += 1
                    if lines_string:
                        self.dirpath_to_md(child.path, counter, f)
                        f.write(f"{lines_string}\n</details>\n\n")
                    file.close()

                except UnicodeDecodeError:
                    pass

def abs_path_check(string_input : str):
    """
    Checks if input is a valid directory and converts to posix.path

    Parameters
    ----------
    string_input : str
        string of path to repo directory

    Returns
    -------
    Posix.Path.absolute() object
        Return the absolute posix path

    Raises
    ------
        NotADirectory : If string input is not a valid dir
    """
    if os.path.isdir(string_input):
        return pathlib.Path(string_input).absolute()
    else:
        raise NotADirectoryError(string_input)

def return_file(string_input : str):
    """
    Creates a results fodler in current working directory if not present
    If user provides no output file format, then defaults to
        results/Results-{time.year}-{time.month}-{time.day}-{time.hour}:{time.minute}:{time.second}.md
    Otherwise will check to see if file format has .md extension or not, add is not, then set to user output file

    Parameters
    ----------
    string_input : str
        string of file name to save to

    Returns
    -------
    TextIOWrapper
        Opens newly created file

    """
    # Creates 'results' directory in current working directory
    os.makedirs(f"{os.getcwd()}/results", exist_ok = True)

    # Saves path string
    output_dir = f"{os.getcwd()}/results"

    # If user provides custom output file
    if string_input:
        # Replace any slashes
        string_input = re.sub(r"/","-", string_input)

        # Add '.md' if not prensent
        # Return IO Wrapper document in open positions
        if re.findall(r".md$", string_input):
            return open(f"{output_dir}/{string_input}", "w+")
        else:
            return open(f"{output_dir}/{string_input}.md", "w+")
        
    # Returns IOWrapper object with default file name convection
    else:
        time = datetime.datetime.now()
        filename = f"Results-{time.year}-{time.month}-{time.day}-{time.hour}:{time.minute}:{time.second}.md"
        return open(f"{output_dir}/{filename}", "w+")

def driver(*args, **kwargs):
    parser = argparse.ArgumentParser(description =
    "Find matching string/terms in directory/files and output where they're found into markdown file")
    parser.add_argument(dest = 'path', type = abs_path_check)

    parser.add_argument(dest = "terms", type = open, nargs = "?", help = """
    Input file for search terms. Defaults to 'terms.txt' in root directory.
    """)

    parser.add_argument(dest = "exceptions", type = open, nargs = "?", help = """
    Input file for directories to skip over. Defaults to 'exceptions.txt' in root directory.
    """)

    parser.add_argument("--open", dest = 'open', action = 'store_true', help = """
    Display collapsable results as open, showing all occurances by default.
    """)

    parser.add_argument("-o", "--output", dest = "output", type = return_file, default = "", help = """
    Custom output file name. Will output in results folder.
    """)
    
    args = parser.parse_args()

    if args.terms == None:
        args.terms = open("terms.txt")
    
    if args.exceptions == None:
        args.exceptions = open("exceptions.txt")

    SearchToMd(args.path, args.output, search_terms = [term.rstrip() for term in args.terms], exceptions = [exception.rstrip() for exception in args.exceptions], open = args.open)
    
    args.terms.close()
    args.exceptions.close()

if __name__ == '__main__':
    driver(*sys.argv)