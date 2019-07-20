import os
import json


def default_dir_path():
    return os.path.join('.', '.wiadro')


def is_valid_file_name(s):
    no_dots = s.replace('.', '')
    return no_dots.isalnum()


def _file_path(base, name, ext):
    return os.path.join(base, name + ext)


def _dump_json(obj, path):
    with open(path, 'w') as f:
        try:
            json.dump(obj, f)
            return True
        except TypeError:
            return False


def _dump_repr(obj, path):
    with open(path, 'w') as f:
        f.write(repr(obj))


def dump(obj, name: str, base_path=None):
    if base_path is None:
        base_path = default_dir_path()

    assert is_valid_file_name(name), f'Invalid object name: {name}'

    os.makedirs(base_path, exist_ok=True)
    if _dump_json(obj, _file_path(base_path, name, '.json')):
        return
    else:
        _dump_repr(obj, _file_path(base_path, name, '.txt'))
