import os
import argparse
import logging
from io import StringIO
import tokenize
from tiktoken import Tokenizer

def setup_logging():
    """Setup basic logging configuration."""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def remove_comments(source):
    """Remove comments and docstrings from Python source code."""
    result = StringIO()
    prev_toktype = tokenize.INDENT
    last_lineno = -1
    last_col = 0
    inside_multiline_string = False
    current_string_delimiter = None

    for tok in tokenize.generate_tokens(source.readline):
        token_type = tok[0]
        token_string = tok[1]
        start_line, start_col = tok[2]
        end_line, end_col = tok[3]

        if token_string in ['"""', "'''"] and not inside_multiline_string:
            inside_multiline_string = True
            current_string_delimiter = token_string
        elif token_string == current_string_delimiter and inside_multiline_string:
            inside_multiline_string = False
            current_string_delimiter = None
            continue

        if inside_multiline_string:
            continue

        if start_line > last_lineno:
            last_col = 0
        if start_col > last_col:
            result.write(" " * (start_col - last_col))
        if token_type == tokenize.COMMENT:
            pass
        else:
            result.write(token_string)
        prev_toktype = token_type
        last_col = end_col
        last_lineno = end_line

    return result.getvalue()

def main():
    parser = argparse.ArgumentParser(description='Combine .py files from current directory and subdirectories.')
    parser.add_argument('--remove-comments', action='store_true', help='Remove comments from the .py files.')
    parser.add_argument('--output', default="combined_code.txt", help='Specify the filename for the output file.')
    parser.add_argument('--depth', type=int, default=1, help='Maximum directory depth to search. Default is 1, which means only the next level of folders.')
    
    args = parser.parse_args()

    if os.path.exists(args.output):
        logging.error(f"Output file {args.output} already exists. Aborting to prevent overwrite.")
        return

    current_directory = os.getcwd()
    start_depth = current_directory.count(os.path.sep)
    included_files = []
    tokenizer = Tokenizer()

    with open(args.output, "w") as output_file:
        for dirpath, dirnames, filenames in os.walk(current_directory):
            current_depth = dirpath.count(os.path.sep) - start_depth
            if current_depth > args.depth:
                del dirnames[:]
                continue

            for filename in filenames:
                if filename.endswith('.py'):
                    filepath = os.path.join(dirpath, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as file:
                            content = file.read()
                            if args.remove_comments:
                                content = remove_comments(StringIO(content))
                            output_file.write(f"===== {filepath} =====\n")
                            output_file.write(content + "\n\n")
                            included_files.append(filepath)
                    except Exception as e:
                        logging.error(f"Failed to process {filepath}. Error: {e}")

    with open(args.output, "r", encoding="utf-8") as f:
        token_count = tokenizer.count_tokens(f.read())

    print("Summary:")
    print(f"Included Files: {len(included_files)}")
    for file in included_files:
        print(f"  - {file}")
    print(f"Written to: {args.output}")
    print(f"Total Tokens in {args.output}: {token_count}")

if __name__ == "__main__":
    setup_logging()
    main()
