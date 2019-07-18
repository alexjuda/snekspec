import collections as c
import typing as t


KeysSpec = c.namedtuple('KeysSpec', ['key_specs'])


def keys():
    pass


def is_valid(spec, x):
    if callable(spec):
        return spec(x)
    elif isinstance(spec, KeysSpec):
        if not isinstance(x, t.Mapping):
            return False
        if set(spec.key_specs) != set(x.keys()):
            return False
        return all(is_valid(key_spec, key)
                   for key_spec, key in zip(spec.key_specs, x.keys()))
    else:
        return spec == x


def main():
    spec = KeysSpec(['first',
                     'last'])
    obj1 = {'first': 'Kamaal',
            'last': 'Fareed'}
    obj2 = {'first': 'Q-Tip'}
    for i, o in enumerate([obj1, obj2]):
        print(f'obj {i+1} valid? {is_valid(spec, o)}')
    print('ssssss')


if __name__ == '__main__':
    main()
