import funkify
import pathlib

@funkify.funkify
def parse_args_from_string(arg_string, file_contents=None):
    if arg_string.startswith('{') and arg_string.endswith('}'):  # JSON
        import json
        return json.loads(arg_string)
    elif arg_string.startswith('key') and ':=' in arg_string:  # ROS2-style
        args_list = arg_string.split()
        pairs = {}
        for arg in args_list:
            key, value = arg.split(':=')
            pairs[key.rstrip(':')] = value
        return pairs
    elif arg_string.startswith('key') and '=' in arg_string:  # Key-value pairs
        args_list = arg_string.split()
        pairs = {}
        for arg in args_list:
            key, value = arg.split('=')
            pairs[key] = value
        return pairs
    elif arg_string.startswith('--') and ' ' in arg_string:  # Command line
        args_list = arg_string.split()
        pairs = {}
        for i in range(0, len(args_list), 2):
            key = args_list[i].lstrip('-')
            value = args_list[i+1]
            pairs[key] = value
        return pairs
    elif file_contents is not None:  # File
        if arg_string.endswith('.json'):
            import json
            return json.loads(file_contents)
        elif arg_string.endswith('.yaml'):
            import yaml
            return yaml.safe_load(file_contents)
        elif arg_string.endswith('.ros'):
            args_list = file_contents.split()
            pairs = {}
            for arg in args_list:
                key, value = arg.split(':=')
                pairs[key.rstrip(':')] = value
            return pairs
        else:
            raise ValueError('Unsupported file format')
    elif ':' in arg_string:  # YAML string
        import yaml
        try:
            return yaml.safe_load(arg_string)
        except yaml.YAMLError:
            raise ValueError('Unsupported input format')
    else:
        raise ValueError('Unsupported input format')
