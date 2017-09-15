# geo_assigner

*A command-line tool and Python module to assign a property from one set of
GeoJSON features to another*

`geo_assigner` operates on two set of GeoJSON features: the sources and the
targets. For each target, it copies a chosen property from all sources that
intersect the target to the target.


## Examples

Say you have a file `trees.geojson` containing the trees in your city and a
file `districts.geojson` containing the city's districts. We'll assume that
every tree has a property `TreeID` with a unique ID and that each district has
a property `DistrictName` holding its name.

To add to each tree the name of the district it is located in:

    geo_assigner districts.geojson trees.geojson DistrictName output.geojson

To add to each district a list of all IDs of its trees:

    geo_assigner -s list trees.geojson districts.geojson TreeID output.geojson


## Installation

    pip install -e git+https://https://github.com/stadt-karlsruhe/geo_assigner.git#egg=geo_assigner


## Usage

    $ geo_assigner --help
    usage: geo_assigner.py [-h] [--strategy {list,last}]
                           SOURCE TARGET PROPERTY OUTPUT

    Assign a property from one set of GeoJSON features to another.

    positional arguments:
      SOURCE                Source GeoJSON file
      TARGET                Target GeoJSON file
      PROPERTY              Property name
      OUTPUT                Output file

    optional arguments:
      -h, --help            show this help message and exit
      --strategy {list,last}, -s {list,last}
                            Conflict resolution strategy in case of multiple
                            matches. Can either be "last" (use the value of the
                            last match, default) or "list" (collect the values
                            from all matches).


## License

Copyright (c) 2017, Stadt Karlsruhe (www.karlsruhe.de)

Distributed under the MIT license, see the file `LICENSE` for details.

