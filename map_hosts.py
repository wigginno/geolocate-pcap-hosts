'''Convert response from ipinfo.io to a GeoJSON multipoint map.'''

from pathlib import Path
import argparse
import json


def main():
    '''Convert response from ipinfo.io to a GeoJSON multipoint map.'''
    # Get file path to list of IPs from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument('ipinfo', help='Path to ipinfo.io responses file (1 response per line)')
    args = parser.parse_args()
    output_dir = Path(args.ipinfo).parent

    # Read in the ipinfo.io response file (each line is a json string)
    with open(args.ipinfo, 'r') as f:
        ip_info_list = [json.loads(line) for line in f.readlines()]

    # Create an empty GeoJSON multipoint map
    geojson = {
        'type': 'FeatureCollection',
        'features': []
    }

    # Add features to the GeoJSON map
    for ip_info in ip_info_list:
        geojson = add_feature(geojson, ip_info)

    # Write the GeoJSON map to a file
    with open(output_dir / 'hosts_map.json', 'w') as f:
        json.dump(geojson, f, indent=4)


def add_feature(geojson: dict, ip_info: dict) -> dict:
    '''
    Add a feature to a GeoJSON multipoint map.
    Args:
        geojson (dict): GeoJSON multipoint map
        ip_info (dict): ipinfo.io response for a host
    '''

    geojson = geojson.copy()

    # Make sure the IP address is not bogon
    if 'bogon' in ip_info:
        return geojson

    # Get the latitude and longitude from the ipinfo.io response
    latitude, longitude = [float(coord) for coord in ip_info['loc'].split(',')]

    # Create a GeoJSON feature (point) for the ipinfo.io response
    new_feature = {
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': [longitude, latitude]
        },
        'properties': {}
    }

    # Add properties of the host to the GeoJSON feature
    property_list = ['ip', 'hostname', 'city', 'region', 'country', 'org', 'postal', 'timezone']
    for property in property_list:
        property_value = ip_info.get(property, "Unknown")
        new_feature['properties'][property] = property_value

    # Add the GeoJSON feature to the GeoJSON map and return the map
    geojson['features'].append(new_feature)
    return geojson

if __name__ == '__main__':
    main()
