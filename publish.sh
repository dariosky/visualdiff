#!/usr/bin/env bash

pandoc --from=markdown --to=rst README.md -o README.rst
make docs

rm dist/*
python setup.py sdist
# ** to install: **
# pip install -e .

twine upload dist/*
