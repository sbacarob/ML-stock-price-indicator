"""Load configuration files and return them as dicionaries."""
import json
import os


def load_endpoints_info():
    """
    Load the configuration parameters for the endpoints.

    :return: Dictionary with the contents of the proper configuration file.
    """
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    file = open(parent_dir + "/endpoints.json", 'r')
    conf = json.load(file)
    file.close()
    return conf


endpoints = load_endpoints_info()
