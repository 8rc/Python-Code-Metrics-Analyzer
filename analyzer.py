#!/usr/bin/env python3

import ast
import os
import sys
import argparse
from collections import defaultdict
from tabulate import tabulate

class ComplexityVisitor(ast.NodeVisitor):
    def __init__(self):
        self.complexity = 0

    def visit_If(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_For(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_While(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_With(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_AsyncWith(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_Try(self, node):
        self.complexity += len(node.handlers) or 1
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        self.complexity += len(node.values) - 1
        self.generic_visit(node)

    def visit_IfExp(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_Compare(self, node):
        self.complexity += len(node.ops) - 1
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id in {'and_', 'or_', 'not_'}:
            self.complexity += 1
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.complexity += 1  # Complexity starts at 1 for the function
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self.complexity += 1  # Complexity starts at 1 for the function
        self.generic_visit(node)

def analyze_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        source = f.read()

    loc = source.count('\n') + 1
    try:
        tree = ast.parse(source, filename=file_path)
    except SyntaxError as e:
        print(f"Syntax error in file {file_path}: {e}")
        return None

    num_functions = 0
    num_classes = 0
    total_complexity = 0

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            num_functions += 1
            visitor = ComplexityVisitor()
            visitor.visit(node)
            total_complexity += visitor.complexity
        elif isinstance(node, ast.ClassDef):
            num_classes += 1

    return {
        'loc': loc,
        'functions': num_functions,
        'classes': num_classes,
        'complexity': total_complexity
    }

def analyze_directory(directory):
    results = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                metrics = analyze_file(path)
                if metrics:
                    results.append({
                        'file': os.path.relpath(path, directory),
                        **metrics
                    })
    return results

def main():
    parser = argparse.ArgumentParser(description='Python Code Metrics Analyzer')
    parser.add_argument('path', help='Path to the Python file or directory')
    args = parser.parse_args()

    if os.path.isfile(args.path) and args.path.endswith('.py'):
        metrics = analyze_file(args.path)
        if metrics:
            results = [{
                'file': os.path.basename(args.path),
                **metrics
            }]
        else:
            sys.exit(1)
    elif os.path.isdir(args.path):
        results = analyze_directory(args.path)
    else:
        print(f"Error: {args.path} is not a valid Python file or directory")
        sys.exit(1)

    if results:
        table = []
        total_loc = total_functions = total_classes = total_complexity = 0
        for res in results:
            table.append([
                res['file'],
                res['loc'],
                res['functions'],
                res['classes'],
                res['complexity']
            ])
            total_loc += res['loc']
            total_functions += res['functions']
            total_classes += res['classes']
            total_complexity += res['complexity']
        table.append([
            'Total',
            total_loc,
            total_functions,
            total_classes,
            total_complexity
        ])
        headers = ['File', 'LOC', 'Functions', 'Classes', 'Complexity']
        print(tabulate(table, headers=headers, tablefmt='fancy_grid'))
    else:
        print("No Python files found.")

if __name__ == '__main__':
    main()
