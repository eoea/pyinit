#!/usr/bin/env python3
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring pylint: disable=missing-function-docstring
"""
    This script creates my Python project directory and the
    necessary subdirectories, __init__.py, main.py, and Makefile.
    Program uses my environment variable for copying the Makefile.

    Global:
        - SUB_DIRS

    Typical usage example:
        create project:
            pyinit -n "foo"
        tidy up a specific project:
            pyinit -n "foo" --tidy
        create only main.py:
            pyinit --main
"""
import sys
import shutil
import argparse
from os import getenv
from typing import List
from pathlib import Path

SUB_DIRS: List[str] = ["docs", "src", "tests", "site", "data"]

def usage() -> None:
    print("[-n/--name] of project needs to be passed!")
    print("usage:")
    print("     create:")
    print("         pyinit [-n/--name] <project>")
    print("     tidy:")
    print("         pyinit [-n/--name] <project> [--tidy]")
    print("     main.py:")
    print("         pyinit [-n/--name] <project> [--main]")

def flags() -> argparse.Namespace:
    """Handles command-line flag parsing."""
    desc: str = ("Creates the directory structure for my python"
                 "projects. Includes: subdirectories, __init__.py,"
                 "and Makefile.")
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("-n", "--name", type=str, help="project name")
    parser.add_argument("--tidy",action="store_true",
                        help="remove empty (unused) directories")
    parser.add_argument("--main",action="store_true",
                        help="create main.py file with a preset main function")
    return parser.parse_args()

def tidy(parent_dir: Path) -> None:
    """Removes empty (unused) subdirectories."""
    if Path(parent_dir).exists():
        for sub_dir in SUB_DIRS:
            try:
                Path(parent_dir).joinpath(sub_dir).rmdir()
            except OSError: # triggered when directory is not empty
                continue

def create_main_py(path: Path) -> None:
    """Creates a main.py file template with a preset main function."""
    if path.joinpath("main.py").is_file():
        print("main.py already exists, remove it if you want to recreate it!")
    else:
        m: str = ("def main() -> None:\n"
                  "    print(\"hello world!\")\n\n"
                  "if __name__ == \"__main__\":\n"
                  "    main()\n")
        with open(path.joinpath("main.py"), "w") as f:
            f.write(m)

def create_subdirectories(parent_dir: Path) -> None:
    """Takes a path to a parent directory and creates its subdirectories.
    Additionally, if the subdirectory is either "src" or "tests",
    then an "__init__.py" is created inside those two subdirectories. A
    main.py is created inside the "src" directory.
    """
    for sub_dir in SUB_DIRS:
        Path(parent_dir).joinpath(sub_dir).mkdir()
        match sub_dir:
            case "src":
                Path(parent_dir).joinpath(sub_dir, "__init__.py").touch()
                create_main_py(Path(parent_dir).joinpath(sub_dir))
            case "tests":
                Path(parent_dir).joinpath(sub_dir, "__init__.py").touch()

def main() -> None:
    args: argparse.Namespace = flags()
    path: Path = Path.cwd()
    if args.name is None:
        if args.main is not None:
            create_main_py(path.cwd())
            sys.exit(0)
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
