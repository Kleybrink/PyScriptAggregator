"""
This is a script that performs aggregation of Python scripts.
"""

import argparse
import ast
import logging
import os
import tokenize
from io import StringIO

import tiktoken


def setup_logging():
    """Setup basic logging configuration."""
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )


def remove_comments(source_code):
    """Remove comments and docstrings from Python source code."""
    result = StringIO()
    last_lineno = -1
    last_col = 0

    for tok in tokenize.generate_tokens(source_code.readline):
        token_type = tok[0]
        token_string = tok[1]
        start_line, start_col = tok[2]
        end_line, end_col = tok[3]

        # For multiline docstrings/comments
        if token_type == tokenize.STRING and (
            token_string.startswith('"""') or token_string.startswith("'''")
        ):
            continue

        # If it's a single line comment
        if token_type == tokenize.COMMENT:
            continue

        if start_line > last_lineno:
            last_col = 0
        if start_col > last_col:
            result.write(" " * (start_col - last_col))

        result.write(token_string)
        last_col = end_col
        last_lineno = end_line

    return result.getvalue()


def extract_definitions(source_code):
    """Extract definitions from Python source code."""
    try:
        root = ast.parse(source_code)
    except SyntaxError as e:
        return f"Error parsing source code: {e}"

    classes = []
    functions = []
    variables = []

    for node in root.body:
        try:
            if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
                func_name = node.name
                arguments = [arg.arg for arg in node.args.args]
                functions.append(f"{func_name}({', '.join(arguments)})")
            elif isinstance(node, ast.ClassDef) and not node.name.startswith("_"):
                init_args = []
                for child in node.body:
                    if isinstance(child, ast.FunctionDef) and child.name == "__init__":
                        init_args = [
                            arg.arg for arg in child.args.args if arg.arg != "self"
                        ]
                class_repr = node.name
                if init_args:
                    class_repr += f"({', '.join(init_args)})"
                classes.append(class_repr)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and not target.id.startswith("_"):
                        variables.append(target.id)
        except (SyntaxError, AttributeError) as e:
            return f"Error processing node {node}: {e}"

    output = []

    if classes:
        output.append("Classes:")
        for c in classes:
            output.append(f"  {c}")

    if functions:
        output.append("Functions:")
        for f in functions:
            output.append(f"  {f}")

    if variables:
        output.append("Variables:")
        for v in variables:
            output.append(f"  {v}")

    return "\n".join(output)


def main():
    """This is the main function of the script."""
    parser = argparse.ArgumentParser(
        description="Combine .py files from current directory and subdirectories."
    )

    parser.add_argument(
        "-r",
        "--remove-comments",
        action="store_true",
        help="Remove comments from the .py files.",
    )
    parser.add_argument(
        "-o",
        "--output-file",
        default="combined_code.txt",
        help="Specify the filename for the output file.",
    )
    parser.add_argument(
        "-d",
        "--search-depth",
        type=int,
        default=1,
        help="Maximum directory depth to search. Default is 1, which means only the "
        "next level of folders.",
    )
    parser.add_argument(
        "-s",
        "--show-defs",
        action="store_true",
        help="Show only definitions instead of full file content.",
    )
    parser.add_argument(
        "-e",
        "--no-filter-for",
        default=None,
        help="Specify the filename for which you want to show the full content, "
        "excluding it from other filters.",
    )

    args = parser.parse_args()

    if os.path.exists(args.output_file):
        logging.warning(
            "Output file %s already exists. It will be overwritten.", args.output_file
        )

    current_directory = os.getcwd()
    start_depth = current_directory.count(os.path.sep)
    included_files = []

    with open(args.output_file, "w", encoding="utf-8") as output_file:
        for dirpath, dirnames, filenames in os.walk(current_directory):
            current_depth = dirpath.count(os.path.sep) - start_depth
            if current_depth > args.search_depth:
                del dirnames[:]
                continue

            for filename in filenames:
                if filename.endswith(".py"):
                    relative_path = os.path.relpath(dirpath, current_directory)
                    filepath = (
                        os.path.join(relative_path, filename)
                        if relative_path != "."
                        else filename
                    )
                    try:
                        with open(
                            os.path.join(dirpath, filename), "r", encoding="utf-8"
                        ) as file:
                            content = file.read()
                            if args.no_filter_for and filepath == args.no_filter_for:
                                pass
                            else:
                                if args.remove_comments:
                                    content = remove_comments(StringIO(content))
                                if args.show_defs:
                                    content = extract_definitions(content)
                            output_file.write(f"===== {filepath} =====\n")
                            output_file.write(content + "\n\n")
                            included_files.append(filepath)
                    except (FileNotFoundError, PermissionError) as e:
                        logging.error("Failed to process %s. Error: %s", filepath, e)

    enc = tiktoken.encoding_for_model("gpt-4")
    with open(args.output_file, "r", encoding="utf-8") as f:
        content = f.read()
        token_count = len(enc.encode(content))

    print("Summary:")
    print(f"Included Files: {len(included_files)}")
    for file in included_files:
        print(f"  - {file}")
    print(f"Written to: {args.output_file}")
    print(f"Total Tokens in {args.output_file}: {token_count}")


if __name__ == "__main__":
    setup_logging()
    main()
