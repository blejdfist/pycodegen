"""Simple JSON frontend"""


def register_arguments(_argument_parser):
    pass


def run(filename, _options=None):
    import json

    with open(filename, "r") as output_file:
        return json.load(output_file)
