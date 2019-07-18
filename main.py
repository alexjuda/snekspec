import collections as c
import typing as t


KeysSpec = c.namedtuple('KeysSpec', ['key_specs'])
CollOfSpec = c.namedtuple('CollOfSpec', ['e_spec'])
AndSpec = c.namedtuple('AndSpec', ['specs'])


def keys(kv_specs):
    return KeysSpec(kv_specs)


def coll_of(e_spec):
    return CollOfSpec(e_spec)


def and_(*specs):
    return AndSpec(specs)


def is_valid(spec, x):
    if callable(spec):
        return spec(x)
    elif isinstance(spec, KeysSpec):
        if not isinstance(x, t.Mapping):
            return False
        if spec.key_specs.keys() != x.keys():
            return False
        return all(is_valid(val_spec, val)
                   for val_spec, val in zip(spec.key_specs.values(), x.values()))
    elif isinstance(spec, CollOfSpec):
        if not isinstance(x, t.Collection):
            return False
        return all(is_valid(spec.e_spec, e)
                   for e in x)
    elif isinstance(spec, AndSpec):
        return all(is_valid(s, x)
                   for s in spec.specs)
    else:
        return spec == x


def is_string(x):
    return isinstance(x, str)


def is_any(x):
    return True

def is_float(x):
    return isinstance(x, float)


def main():
    rating_spec = is_float
    good_rating_spec = and_(rating_spec,
                            lambda x: x > 0.6)
    spec = keys({'first': is_any,
                 'last': is_string,
                 'ratings': coll_of(good_rating_spec)})

    objs = [{'first': 'Kamaal',
             'last': 'Fareed',
             'ratings': [0.9, 0.7, 0.9]},
            {'first': 'Q-Tip'},
            {'first': 'KRS',
             'last': 1,
             'ratings': [0.8, 0.7, 0.9]},
            {'first': 'KRS',
             'last': '1',
             'ratings': [0.5, 0.7, 0.9]}]
    for i, o in enumerate(objs):
        print(f'obj {i+1} valid? {is_valid(spec, o)}')
    print('ssssss')


if __name__ == '__main__':
    main()