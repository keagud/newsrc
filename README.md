# newsrc

A simple script for generating boilerplate for single source files from templates. For cases where something like cookiecutter would be overkill.  The paradigm use case is something like an Advent of Code or Leetcode problem, where you don't need a full directory and build setup, but you want to save typing out `int main(int argc, char* argv[]) ... ` every single time.

# Installation and Usage

Just run `./install.sh` and a standalone executable will be built using `shiv` (using a virtual environment for the dependency installation) and placed in `~/.local/bin/newsrc`.  The templates folder will be copied to `~/.local/templates/`; the contents of this directory are just placeholder template files using Jinja2 for template syntax. Templates are included for python, C, C++ and scala since that's what I generally need, but you can make your own templates using these as examples. 

When the `newsrc` script is called, it expects a single argument, the name of the file to be created. It then looks in the templates directory for a template with the same extension, renders it, and saves it to that location. If you have an EDITOR environment variable it will also open the new file in that automatically. 

Copyleft 2023, all wrongs reserved 

