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

'''
Command line interface.
'''

import argparse
import sys

from . import *


STRATEGIES = {
    'last': LastValueStrategy,
    'list': ListValuesStrategy,
}

parser = argparse.ArgumentParser(description='Assign a property from ' +
                                 'one set of GeoJSON features to another.')
parser.add_argument('source_filename', metavar='SOURCE',
                    help='Source GeoJSON file')
parser.add_argument('target_filename', metavar='TARGET',
                    help='Target GeoJSON file')
parser.add_argument('property_name', metavar='PROPERTY',
                    help='Property name')
parser.add_argument('output_filename', metavar='OUTPUT',
                    help='Output file')
parser.add_argument('--strategy', '-s', default='last', choices=STRATEGIES,
                    help='Conflict resolution strategy in case of ' +
                    'multiple matches. Can either be "last" (use the ' +
                    'value of the last match, default) or "list" ' +
                    '(collect the values from all matches).')


def progress(current, total):
    sys.stdout.write('.')
    sys.stdout.flush()


def main():
    args = parser.parse_args()
    strategy = STRATEGIES[args.strategy](args.property_name)
    source_geojson = load_json(args.source_filename)
    target_geojson = load_json(args.target_filename)
    assign(source_geojson, target_geojson, strategy, progress)
    print()
    save_json(target_geojson, args.output_filename)

