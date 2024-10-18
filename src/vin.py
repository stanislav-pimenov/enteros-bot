# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import csv
import re


class InvalidVINException(Exception):
    """Custom exception for invalid VIN numbers."""
    def __init__(self, vin, message="Invalid VIN"):
        self.vin = vin
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}: {self.vin}'


def validate_vin(vin: str):
    """Validates a VIN number. Raises an exception if invalid."""
    vin_regex = r'^[A-HJ-NPR-Z0-9]{17}$'

    if not re.match(vin_regex, vin):
        raise InvalidVINException(vin)

    return True


def read_csv_dic(csv_name):
    with open(csv_name, mode='r', encoding="utf8") as infile:
        reader = csv.DictReader(infile, delimiter=';')
        # return [row for row in reader]
        # return list(reader)
        dict = {}
        for row in reader:
            dict[row['code']] = row['name']
        return dict


def decode_vin(vin_str):
    validate_vin(vin_str)
    vin_dict = {}
    vin_dict['manufacturing_continent_code'] = vin_str[:1]
    vin_dict['manufacturing_country_code'] = vin_str[:2]
    vin_dict['manufacturer_code'] = vin_str[:3]
    # print(f'vin: {vin_dict}')
    vin_decoded_dict = {}
    vin_decoded_dict['country'] = find_value_by_key(vin_dict['manufacturing_country_code'],
                                                    manufacturer_country_code_dict)
    vin_decoded_dict['continent'] = find_value_by_key(vin_dict['manufacturing_continent_code'],
                                                      manufacturer_continent_code_dict)
    vin_decoded_dict['manufacturer'] = find_value_by_key(vin_dict['manufacturer_code'], manufacturer_code_dict)
    vin_decoded_dict['body_style'] = body_styles.get(vin_str[3], 'Unknown')
    vin_decoded_dict['engine_type'] = engine_types.get(vin_str[4], 'Unknown')
    return vin_decoded_dict
    # print(f'vin decoded: {vin_decoded_dict}')


def is_in_range(key, range_key):
    # Splitting range key by '-'
    start, end = range_key.split('-')
    # Check if key is within the alphabetical range
    return start <= key <= end


def match_the_first_part(key, range_key):
    start = range_key.split('/')
    return start == key


def find_value_by_key(key, dictionary):
    # Check if exact match exists
    if key in dictionary:
        return dictionary[key]

    # If not, check for range matches
    for complex_key in dictionary:
        if '/' in complex_key:
            if match_the_first_part(key, complex_key):
                return dictionary[complex_key]
        if '-' in complex_key:  # Only consider keys that define a range
            if is_in_range(key, complex_key):
                return dictionary[complex_key]

    return None  # If no match is found


manufacturer_code_dict = read_csv_dic('csv/manufacturer_code.csv')
manufacturer_continent_code_dict = read_csv_dic('csv/manufacturing_continent_code.csv')
manufacturer_country_code_dict = read_csv_dic('csv/manufacturing_country_code.csv')

# Example mappings (these would need to be extended based on manufacturer data)
body_styles = {
    'S': 'Sedan',
    'C': 'Coupe',
    'H': 'Hatchback',
    'T': 'Truck',
    'U': 'SUV'
}

engine_types = {
    'A': 'Gasoline',
    'D': 'Diesel',
    'E': 'Electric',
    'H': 'Hybrid'
}