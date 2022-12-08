import json
from os import path
from unittest.mock import Mock



def get_mock_workato_dict(filename):
    basepath = path.dirname(__file__)
    filepath = path.join(basepath, filename)
    mock_workato_json = open(filepath, 'r').read()
    mock_workato_dict = json.loads(mock_workato_json)
    return mock_workato_dict


def get_mock_workato_from_file(filename):
    mock_workato_dict = get_mock_workato_dict(filename)
    mock_workato = Mock()
    mock_workato.managed_users.get_all.return_value = mock_workato_dict['managed_users']
    mock_workato.connections.get_all.return_value = mock_workato_dict['connections']
    mock_workato.folders.get_all.return_value = mock_workato_dict['folders']
    mock_workato.recipes.get_all.return_value = mock_workato_dict['recipes']
    return mock_workato


def get_mock_workato():
    return get_mock_workato_from_file('mock_workato.json')


def compare_dict_keys(dict1, dict2):
    """
    Compare dict1 keys with dict2 keys and see
    if dict1 has extra keys compared to dict2

    Parameters:
        dict1 (dict): response dict from API
        dict2 (dict): mock dict

    Returns:
        Set of keys
    """
    return dict1.keys() - dict2.keys()
