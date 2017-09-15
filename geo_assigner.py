#!/usr/bin/env python3

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


def geojson_to_shapely(feature_collection):
    '''
    Convert GeoJSON features to Shapely shapes.

    Returns a list of 2-tuples. Each tuple consists of the GeoJSON
    feature and the corresponding Shapely shape. The feature and the
    shape share their list of coordinates.
    '''
    return [(feature, shapely.geometry.asShape(feature['geometry']))
            for feature in feature_collection['features']]


class ConflictResolutionStrategy:

    def __init__(self, property_name):
        self.property_name = property_name

    def begin(self, target_feature, target_shape):
        pass

    def intersection(self, source_feature, source_shape, target_feature,
                     target_shape, intersection, property_value):
        pass

    def end(self, target_feature, target_shape):
        pass


class LastValueStrategy(ConflictResolutionStrategy):

    def begin(self, target_feature, target_shape):
        try:
            del target_feature['properties'][self.property_name]
        except KeyError:
            pass

    def intersection(self, source_feature, source_shape, target_feature,
                     target_shape, intersection):
        value = source_feature['properties'][self.property_name]
        target_feature['properties'][self.property_name] = value


class ListValuesStrategy(ConflictResolutionStrategy):

    def begin(self, target_feature, target_shape):
        target_feature['properties'][self.property_name] = []

    def intersection(self, source_feature, source_shape, target_feature,
                     target_shape, intersection):
        value = source_feature['properties'][self.property_name]
        target_feature['properties'][self.property_name].append(value)


def assign(source_geojson, target_geojson, strategy, progress=None):
    '''
    Assign a property from one set of GeoJSON features to another.

    Modifies ``target_geojson`` in-place.
    '''
    sources = geojson_to_shapely(source_geojson)
    targets = geojson_to_shapely(target_geojson)
    for i, (target_feature, target_shape) in enumerate(targets):
        if progress:
            progress(i, len(targets))
        strategy.begin(target_feature, target_shape)
        for source_feature, source_shape in sources:
            intersection = target_shape.intersection(source_shape)
            if intersection.is_empty:
                continue
            strategy.intersection(source_feature, source_shape, target_feature,
                                  target_shape, intersection)
        strategy.end(target_feature, target_shape)


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

