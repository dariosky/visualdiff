#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
from distutils.util import convert_path

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()


def get_version(path):
    ver_path = convert_path(path)
    main_ns = {}
    with open(ver_path) as ver_file:
        exec(ver_file.read(), main_ns)
    return main_ns['__version__']


version = get_version('visualdiff/version.py')
requirements = ['pillow',
                'pyppeteer', ]

dependency_links = [
    'git+https://github.com/miyakogi/pyppeteer.git@dev',
]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ] + requirements

setup(
    author="Dario Varotto",
    author_email='dario.varotto@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    description="Automate chrome browser render diffs for website testing",
    install_requires=requirements,
    dependency_links=dependency_links,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='visualdiff',
    name='visualdiff',
    packages=find_packages(include=['visualdiff']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/dariosky/visualdiff',
    version=version,
    zip_safe=False,
)
