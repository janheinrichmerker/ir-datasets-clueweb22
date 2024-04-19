[![PyPi](https://img.shields.io/pypi/v/ir-datasets-clueweb22?style=flat-square)](https://pypi.org/project/ir-datasets-clueweb22/)
[![CI](https://img.shields.io/github/actions/workflow/status/heinrichreimer/ir-datasets-clueweb22/ci.yml?branch=main&style=flat-square)](https://github.com/heinrichreimer/ir-datasets-clueweb22/actions/workflows/ci.yml)
[![Code coverage](https://img.shields.io/codecov/c/github/heinrichreimer/ir-datasets-clueweb22?style=flat-square)](https://codecov.io/github/heinrichreimer/ir-datasets-clueweb22/)
[![Python](https://img.shields.io/pypi/pyversions/ir-datasets-clueweb22?style=flat-square)](https://pypi.org/project/ir-datasets-clueweb22/)
[![Issues](https://img.shields.io/github/issues/heinrichreimer/ir-datasets-clueweb22?style=flat-square)](https://github.com/heinrichreimer/ir-datasets-clueweb22/issues)
[![Commit activity](https://img.shields.io/github/commit-activity/m/heinrichreimer/ir-datasets-clueweb22?style=flat-square)](https://github.com/heinrichreimer/ir-datasets-clueweb22/commits)
[![Downloads](https://img.shields.io/pypi/dm/ir-datasets-clueweb22?style=flat-square)](https://pypi.org/project/ir-datasets-clueweb22/)
[![License](https://img.shields.io/github/license/heinrichreimer/ir-datasets-clueweb22?style=flat-square)](LICENSE)

# 💾 ir-datasets-clueweb22

Extension for accessing the [ClueWeb22](https://lemurproject.org/clueweb22/) via [ir_datasets](https://ir-datasets.com/).

## Installation

Install the package from PyPI:

```shell
pip install ir-datasets-clueweb22
```

## Usage

Using this extension is simple. Just register the additional datasets by calling `register()`. Then you can load the datasets with [ir_datasets](https://ir-datasets.com/python.html) as usual:

```python
from ir_datasets import load
from ir_datasets_clueweb22 import register

# Register the ClueWeb22 datasets.
register()
# Use ir_datasets as usual.
dataset = load("clueweb22/b")
```

If you want to use the [CLI](https://ir-datasets.com/cli.html), just use the `ir_datasets_clueweb22` instead of `ir_datasets`. All CLI commands will work as usual, e.g., to list the available datasets:

```shell
ir_datasets_clueweb22 list
```

## Development

To build this package and contribute to its development you need to install the `build`, `setuptools`, and `wheel` packages (pre-installed on most systems):

```shell
pip install build setuptools wheel
```

Create and activate a virtual environment:

```shell
python3.10 -m venv venv/
source venv/bin/activate
```

### Dependencies

Install the package and test dependencies:

```shell
pip install -e .[tests]
```

### Testing

Verify your changes against the test suite to verify.

```shell
ruff check .                   # Code format and LINT
mypy .                         # Static typing
bandit -c pyproject.toml -r .  # Security
pytest .                       # Unit tests
```

Please also add tests for your newly developed code.

### Build wheels

Wheels for this package can be built with:

```shell
python -m build
```

## Support

If you have any problems using this package, please file an [issue](https://github.com/heinrichreimer/ir-datasets-clueweb22/issues/new).
We're happy to help!

## License

This repository is released under the [MIT license](LICENSE).
