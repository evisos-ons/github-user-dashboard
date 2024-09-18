# Dummy Project: GitHub User Dashboard

This project is a demo of the design system implemented in Python and Flask, using the GitHub API.

## Setup

For setting up this project, run the below command. pyenv is a Python version management tool that allows switching between multiple Python versions. jq is a JSON preprocessor that is used to fetch the design system's templates using `scripts/load_release.sh`.

```
brew install pyenv jq
```

Install Python and initialise the virtual environment as shown below.
*Note: The Python version is 3.11.*

```
pyenv install
python3 -m venv env && source env/bin/activate
```

Install Poetry, a dependency management and packaging tool, as shown below.

```
pip install poetry
```

All the libraries declared are available in `pyproject.toml`.

To install these dependencies, run `make install`. 

To install these dependencies plus linting and formatting tools, run `make install-dev`.

## Running the Application

To run the flask application **without** the debugger active use:

```
make run
```

To run the flask application **with** the debugger active use:

```
make run-dev
```

## Linting and Formatting

If you have installed the developer dependencies, you are able to lint and format  using black, ruff and mypy.

```
make lint
```

To clean the temporary files created after running the linter, use `make clean`.
