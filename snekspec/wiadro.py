import os
import shutil
import json
import typing as t
import types


def default_dir_path():
    return os.path.join('.', '.wiadro')


def is_valid_file_name(s):
    # no_dots = s.replace('.', '')
    # return no_dots.replace().isalnum()
    return (s
            .replace('.', '')
            .replace('_', 'u')
            .isalnum())


def _file_path(base, name, ext):
    return os.path.join(base, name + ext)


def _dump_json(obj, path):
    with open(path, 'w') as f:
        try:
            json.dump(_jsonify(obj), f)
            return True
        except TypeError:
            pass

    os.unlink(path)
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


def dump_all(objs_dict, remove_existing=True, base_path=None):
    if base_path is None:
        base_path = default_dir_path()

    shutil.rmtree(base_path, ignore_errors=True)

    for name, obj in objs_dict.items():
        dump(obj, name, base_path=base_path)


def _jsonify(obj):
    if isinstance(obj, t.Mapping):
        return {_jsonify(k): _jsonify(v) for k, v in obj.items()}
    if isinstance(obj, str):
        return obj
    try:
        fields = obj._asdict()
        return {'kind': 'namedtuple',
                'classname': type(obj).__name__,
                'fields': _jsonify(fields)}
    except AttributeError:
        pass
    if isinstance(obj, t.Iterable):
        return [_jsonify(e) for e in obj]
    if isinstance(obj, (types.FunctionType, types.BuiltinFunctionType)):
        return {'kind': 'function',
                'name': obj.__name__,
                'module': obj.__module__}
    try:
        fields = vars(obj)
        return {'kind': 'custom_class',
                'classname': type(obj).__name__,
                'fields': _jsonify(fields)}
    except TypeError:
        pass

    return obj
