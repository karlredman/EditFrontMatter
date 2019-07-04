#!/usr/bin/env bash

# fail on error
set -e

source ~/.bashrc

py_version=$1

echo "Testing with python version ${py_version}...."
pyenv global ${py_version}

# install dependencies
pip install -e .
pip install -r docsource/requirements.txt

flake8 . --exclude venv docsource docs --ignore=E501

make -C docsource clean; TEST_DATA_DIR="../examples/data/" make -C docsource doctest

echo "Test for python version ${py_version}: done."
