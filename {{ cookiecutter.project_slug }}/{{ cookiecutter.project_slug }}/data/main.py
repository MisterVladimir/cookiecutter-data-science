# -*- coding: utf-8 -*-
"""Command line interface (CLI) to processing the raw data."""

import argparse
import pathlib
import sys


def _get_cli_arg_parser() -> argparse.ArgumentParser:
    """Return a CLI argument parser."""
    parser = argparse.ArgumentParser(description="Clean the raw data.")
    parser.add_argument(
        "input_directory",
        help="Directory containing the raw data to be processed.",
        type=pathlib.Path,
    )
    parser.add_argument(
        "output_directory",
        help="Directory to write the processed data to.",
        type=pathlib.Path,
    )
    return parser


def _check_cli_args(args: argparse.Namespace) -> None:
    """
    Process the CLI arguments.

    :raise FileNotFoundError:
        The input data directory does not exist.
    """
    input_directory = args.input_directory

    if not input_directory.exists():
        raise FileNotFoundError(
            f"Cannot process the data in {input_directory} because that directory does not exist."
        )

    args.output_directory.mkdir(exist_ok=True)


def main(argv) -> None:
    """
    Run data processing scripts to turn raw data from (../raw) into cleaned
    data ready to be analyzed (saved in ../processed).
    """
    parser = _get_cli_arg_parser()
    args = parser.parse_args(argv)

    _check_cli_args(args)

    # Your code goes here.


if __name__ == "__main__":
    main(sys.argv[1:])
