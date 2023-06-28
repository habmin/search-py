# Search-Py
### *Search and filter terms in a directory or repo into a markdown file*

## Description
search-py is a python script that looks for search input terms from an external file, looks through all children directories and files for the terms, and outputs the file and line location where that term was found. 

Its use was designed to be used in repo projects, in order to help collobrate with other developers where any certain function, property, variables, etc. is called. 

## Features
- Search terms list is loaded from external text file.
- Can include a list of exception directories and files to skip searching in.
- Have drop down detail menu open or closed when creating the markdown.
- Include checkboxs or not.
- Custom output file name.
- Include links to github repo at line locations

## How-to
1. Clone/download repo or just `search.py`.
2. Navigation to the directory where script is saved.
3. Create a `terms.txt` file in the same directory and type your search term/s on a single line, like so:
```
Terms
to
Search
for

```
4. Create a `exceptions.txt` file in the same directory and type out any directories or files you wish to skip over. You may have the txt file empty, but you need to at least create it.
5. Run the script with the path to you root directory you wish to search in, can either be absolute or relative.
6. Markdown files will be created in a `results` folder.

