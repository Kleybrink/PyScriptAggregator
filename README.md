# PyScriptAggregator: Python Codebase Consolidator

**What is PyScriptAggregator?**  
PyScriptAggregator is a Python tool designed to consolidate Python code from various files within a directory and its subdirectories. Whether you're looking to batch together multiple scripts or get a summary of definitions across a project, this tool can help. A primary use case is efficiently consolidating codebases for language models like ChatGPT.

## Installation

### From GitHub

To get the latest version directly from the repository:

```bash
git clone https://github.com/Kleybrink/PyScriptAggregator.git
cd PyScriptAggregator
pip install .
```

**Note**: Instead of installing the requirements via `requirements.txt`, we're suggesting the use of `pip install .`, as this method will also make the `sagg` script globally available in your environment.

## Usage

Once installed, you can use `sagg` from any directory in your command line:

```bash
sagg --output=OUTPUT_FILENAME.txt
```

**Options:**  
- `--remove-comments`: Removes comments and docstrings from the Python files.
- `--output` or `-o`: Specifies the name of the output file (default is `combined_code.txt`).
- `--depth` or `-d`: Sets the maximum directory depth to search (default is 1, meaning only the next directory level).
- `--show-defs` or `-s`: Instead of showing the full content, only show definitions (functions, classes, variables) in the output.
- `--no-filter-for` or `-e`: Specify a filename for which you want to show the full content, excluding it from other filters. For example, `-e special_script.py` will show the complete content of `special_script.py`.

**Example:** To consolidate all Python files in the current directory and its immediate subdirectories, excluding comments, and only showing definitions:

```bash
sagg --remove-comments --depth=1 --show-defs --output=consolidated_summary.txt
```