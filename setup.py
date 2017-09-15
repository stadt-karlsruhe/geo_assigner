#!/usr/bin/env python3

# Copyright (c) 2017, Stadt Karlsruhe (www.karlsruhe.de)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os.path
import re
import sys

from setuptools import find_packages, setup

HERE = os.path.dirname(__file__)
SOURCE_FILE = os.path.join(HERE, 'geo_assigner', '__init__.py')
REQUIREMENTS_FILE = os.path.join(HERE, 'requirements.txt')

version = None
with open(SOURCE_FILE, encoding='utf8') as f:
    for line in f:
        s = line.strip()
        m = re.match(r"""__version__\s*=\s*['"](.*)['"]""", line)
        if m:
            version = m.groups()[0]
            break
if not version:
    raise RuntimeError('Could not extract version from "%s".' % SOURCE_FILE)

with open(REQUIREMENTS_FILE, encoding='utf8') as f:
    requirements = f.readlines()

long_description = """
A command-line tool and Python module to assign a property from one set of
GeoJSON features to another.
""".strip()

setup(
    name='geo_assigner',
    description='Copy properties between intersecting GeoJSON features',
    long_description=long_description,
    url='https://github.com/stadt-karlsruhe/geo-assigner',
    version=version,
    license='MIT',
    keywords=['geojson'],
    classifiers=[
        # Reference: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Scientific/Engineering :: GIS",
    ],
    author='Stadt Karlsruhe',
    author_email='transparenz@karlsruhe.de',
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'geo_assigner = geo_assigner.__main__:main',
        ],
    },
)

