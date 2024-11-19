# Python Code Metrics Analyzer

## Overview

This Python script analyzes Python files in a given directory (or a single file) and computes various code metrics:

- **Lines of Code (LOC)**: Total number of lines in the source code.
- **Number of Functions**: Count of functions and async functions defined.
- **Number of Classes**: Count of classes defined.
- **Cyclomatic Complexity**: Sum of cyclomatic complexities for all functions.

## Features

- **Recursive Analysis**: Analyzes all `.py` files in the specified directory and its subdirectories.
- **Cyclomatic Complexity Calculation**: Uses the `ast` module to parse and compute complexity.
- **Formatted Output**: Presents results in a neatly formatted table using `tabulate`.
- **Command-Line Interface**: Accepts a file or directory path as an argument.
- **Intricate Code**: Demonstrates advanced use of Python features and standard libraries.

## Requirements

- Python 3.6 or higher
- Install dependencies:

  ```bash
  pip install tabulate
  ```