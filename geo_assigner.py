#!/usr/bin/env python3

import collections
import json

import shapely.geometry


def load_json(filename):
    '''
    Load a JSON file.
    '''
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data, filename):
    '''
    Save JSON data to a file.
    '''
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f)


class Element:
    '''
    A geo-data element like a point, line, or polygon.

    This class is a facade for the underlying GeoJSON and Shapely
    objects representing the element's geometry, which are available via
    the ``feature`` and ``shape`` attributes, respectively.

    The GeoJSON properties are also exposed via the dictionary
    interface.
    '''
    def __init__(self, feature):
        '''
        Constructor.

        ``feature`` is a GeoJSON feature.
        '''
        self.feature = feature
        self.shape = shapely.geometry.asShape(feature['geometry'])

    def __getitem__(self, key):
        return self.feature['properties'][key]

    def __setitem__(self, key, value):
        self.feature['properties'][key] = value

    def __delitem__(self, key):
        del self.feature['properties'][key]

    def intersection(self, element):
        '''
        Return the intersection of this element and another element.

        The return value is a Shapely object.
        '''
        return self.shape.intersection(element.shape)


def _geojson_to_elements(feature_collection):
    return [Element(f) for f in feature_collection['features']]


class Strategy:
    '''
    Base class for conflict resolution strategies.

    A resolution strategy handles the assignment of property values from
    sources to the targets they intersect.

    The name of the property that is being assigned is available from the
    ``property_name`` attribute.
    '''
    def __init__(self, property_name):
        self.property_name = property_name

    def begin(self, target):
        '''
        Called for every target element before the intersection tests.

        Can update the target's property in place.
        '''
        pass

    def intersection(self, source, target, intersection):
        '''
        Called for every intersecting source/target pair.

        ``source`` and ``target`` are ``Element`` instances, and
        ``intersection`` is a Shapely object describing their intersection.
        '''
        pass

    def end(self, target):
        '''
        Called for every target after the intersection tests.

        After this call, the target's property must be in its intended state.
        '''
        pass


class LastValueStrategy(Strategy):
    '''
    Strategy that uses the value from the last intersection.
    '''
    def begin(self, target):
        try:
            del target[self.property_name]
        except KeyError:
            pass

    def intersection(self, source, target, intersection):
        target[self.property_name] = source[self.property_name]


class ListValuesStrategy(Strategy):
    '''
    Strategy that collects the values from all intersections in a list.
    '''
    def begin(self, target):
        target[self.property_name] = []

    def intersection(self, source, target, intersection):
        target[self.property_name].append(source[self.property_name])


def assign(source_geojson, target_geojson, strategy, progress=None):
    '''
    Assign a property from one set of GeoJSON features to another.

    ``source_geojson`` and ``target_geojson`` are GeoJSON feature
    collections.

    ``strategy`` is an instance of ``Strategy``.

    ``progress`` is an optional callback that is called each time before
    the next target is being processed. It receives two arguments: The
    number of already processed targets and the number of targets in
    total.

    Modifies ``target_geojson`` in-place.
    '''
    sources = _geojson_to_elements(source_geojson)
    targets = _geojson_to_elements(target_geojson)
    for i, target in enumerate(targets):
        if progress:
            progress(i, len(targets))
        strategy.begin(target)
        for source in sources:
            intersection = target.intersection(source)
            if intersection.is_empty:
                continue
            strategy.intersection(source, target, intersection)
        strategy.end(target)


if __name__ == '__main__':

    import sys

    from shapely.geometry import Point, Polygon

    STRATEGIES = {
        'last': LastValueStrategy,
        'list': ListValuesStrategy,
    }

    if len(sys.argv) != 6:
        sys.exit('Usage: {} SOURCE_FILE TARGET_FILE PROPERTY_NAME STRATEGY OUTPUT_FILE'.format(sys.argv[0]))
    source_filename = sys.argv[1]
    target_filename = sys.argv[2]
    property_name = sys.argv[3]
    strategy_name = sys.argv[4]
    output_filename = sys.argv[5]

    try:
        strategy_cls = STRATEGIES[strategy_name]
    except KeyError:
        sys.exit('Unknown strategy "{}".'.format(strategy_name))
    strategy = strategy_cls(property_name)

    source_geojson = load_json(source_filename)
    target_geojson = load_json(target_filename)

    def progress(current, total):
        sys.stdout.write('.')
        sys.stdout.flush()

    assign(source_geojson, target_geojson, strategy, progress)
    print()

    save_json(target_geojson, output_filename)

