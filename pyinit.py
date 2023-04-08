#!/usr/bin/env python3
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
"""
    This script creates my Python project directory and the
    necessary subdirectories, __init__.py, and Makefile.
    Program uses my environment variable for copying the Makefile.

    Global:
        - SUB_DIRS


    Typical usage example:
        create:
            pyinit -n "foo"
        tidy up a specific project:
            pyinit -n "foo" --tidy
"""
import sys
import shutil
import argparse
from os import getenv
from typing import List
from pathlib import Path

SUB_DIRS: List[str] = ["docs", "src", "tests", "site", "data"]

def tidy(parent_dir: Path) -> None:
    """Removes empty (unused) subdirectories."""
    if Path(parent_dir).exists():
        for sub_dir in SUB_DIRS:
            try:
                Path(parent_dir).joinpath(sub_dir).rmdir()
            except OSError: # triggered when directory is not empty
                continue

def flags() -> argparse.Namespace:
    """Handles command-line flag parsing."""
    desc: str = ("Creates the directory structure for my python"
                 "projects. Includes: subdirectories, __init__.py,"
                 "and Makefile.")
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("-n", "--name", type=str, help="project name")
    parser.add_argument("--tidy",action="store_true",
                        help="remove empty (unused) directories")
    return parser.parse_args()

def create_subdirectories(parent_dir: Path) -> None:
    """Takes a path to a parent directory and creates its subdirectories.
    Additionally, if the subdirectory is either "src" or "tests",
    then an "__init__.py" is created inside those two subdirectories.
    """
    for sub_dir in SUB_DIRS:
        Path(parent_dir).joinpath(sub_dir).mkdir()
        if "src" in sub_dir or "tests" in sub_dir:
            Path(parent_dir).joinpath(sub_dir, "__init__.py").touch()

def usage() -> None:
    print("[-n/--name] of project needs to be passed!")
    print("usage:")
    print("     create:")
    print("         pyinit [-n/--name] <project>")
    print("     tidy:")
    print("         pyinit [-n/--name] <project> [--tidy]")

def main() -> None:
    args: argparse.Namespace = flags()
    path: Path = Path.cwd()
    if args.name is None:
        usage()
        sys.exit(1)
    elif args.name is not None and args.tidy is False:
        path = path.joinpath(args.name)
        if not Path(path).exists():
            Path(path).mkdir()
            create_subdirectories(path)
            shutil.copy(Path(getenv("GITLAB")).joinpath("pyinit","util",
                                                        "Makefile"),path)
        else:
            print(f"{args.name} project already exists.")
            sys.exit(1)
    else:
        tidy(path.joinpath(args.name))

if __name__ == "__main__":
    main()
