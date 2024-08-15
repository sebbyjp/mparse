import pytest
import json
import yaml
from unittest import mock
from mparse import parse_args_from_string

def test_parse_json():
    arg_string = '{"key1": "value1", "key2": "value2"}'
    result = parse_args_from_string(arg_string)
    expected = {"key1": "value1", "key2": "value2"}
    assert result == expected

def test_parse_yaml():
    arg_string = """
    key1: value1
    key2: value2
    """
    result = parse_args_from_string(arg_string)
    expected = {"key1": "value1", "key2": "value2"}
    assert result == expected

def test_parse_key_value_pairs():
    arg_string = 'key1=value1 key2=value2'
    result = parse_args_from_string(arg_string)
    expected = {"key1": "value1", "key2": "value2"}
    assert result == expected

def test_parse_command_line():
    arg_string = '--key1 value1 --key2 value2'
    result = parse_args_from_string(arg_string)
    expected = {"key1": "value1", "key2": "value2"}
    assert result == expected

def test_parse_ros2_style():
    arg_string = 'key1:=value1 key2:=value2'
    result = parse_args_from_string(arg_string)
    expected = {"key1": "value1", "key2": "value2"}
    assert result == expected

@mock.patch('os.path.isfile', return_value=True)
@mock.patch('builtins.open', mock.mock_open(read_data='{"key1": "value1", "key2": "value2"}'))
def test_parse_from_file(mock_isfile):
    arg_string = 'path/to/file.json'
    result = parse_args_from_string(arg_string, file_contents='{"key1": "value1", "key2": "value2"}')
    expected = {"key1": "value1", "key2": "value2"}
    assert result == expected

@mock.patch('os.path.isfile', return_value=True)
@mock.patch('builtins.open', mock.mock_open(read_data='key1:=value1 key2:=value2'))
def test_parse_ros2_from_file(mock_isfile):
    arg_string = 'path/to/file.ros'
    result = parse_args_from_string(arg_string, file_contents='key1:=value1 key2:=value2')
    expected = {"key1": "value1", "key2": "value2"}
    assert result == expected

@mock.patch('os.path.isfile', return_value=True)
@mock.patch('builtins.open', mock.mock_open(read_data="""
key1: value1
key2: value2
"""))
def test_parse_yaml_from_file(mock_isfile):
    arg_string = 'path/to/file.yaml'
    result = parse_args_from_string(arg_string, file_contents="""
key1: value1
key2: value2
""")
    expected = {"key1": "value1", "key2": "value2"}
    assert result == expected
