#!/usr/bin/bash

PYTHON=python3.9

cd ..  \
	&& $PYTHON -m pip install build twine \
	&& rm -rf dist \
	&& $PYTHON -m build \
	&& $PYTHON -m twine upload dist/*  --verbose

