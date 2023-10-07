# ScriptAggregator: Python Codebase Consolidator

**What is ScriptAggregator?**  
ScriptAggregator is a Python tool designed to consolidate Python code from various files within a directory and its subdirectories. A primary use case is efficiently consolidating codebases for language models like ChatGPT.

## Installation

### From GitHub

To get the latest version directly from the repository:

```bash
git clone https://github.com/Kleybrink/ScriptAggregator.git
cd ScriptAggregator
pip install .
```

**Note**: Instead of installing the requirements via `requirements.txt`, we're suggesting the use of `pip install .`, as this method will also make the `sagg` script globally available in your environment.

## Usage

Once installed, you can use `sagg` from any directory in your command line:

```bash
sagg --output=OUTPUT_FILENAME.txt
```

**Options:**  
- `--remove-comments`: Removes comments from the Python files.
- `--output`: Specifies the name of the output file (default is `combined_code.txt`).
- `--depth`: Sets the maximum directory depth to search (default is 1, meaning only the next directory level).

**Example:** To consolidate all Python files in the current directory and its immediate subdirectories, excluding comments:

```bash
sagg --remove-comments --depth=1 --output=consolidated_code.txt
```
