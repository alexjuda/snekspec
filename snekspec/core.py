import collections as c
import typing as t


KeysSpec = c.namedtuple('KeysSpec', ['key_specs'])
CollOfSpec = c.namedtuple('CollOfSpec', ['e_spec'])
AndSpec = c.namedtuple('AndSpec', ['specs'])
TupleSpec = c.namedtuple('TupleSpec', ['e_specs'])
NilableSpec = c.namedtuple('NilableSpec', ['subspec'])

class PredSpec:
    def __init__(self, f):
        self._f = f

    def __call__(self, *args, **kwargs):
        return self._f(*args, **kwargs)


Explanation = c.namedtuple('Explanation', 'obj spec fail_reason original_obj trace')


def keys(kv_specs):
    return KeysSpec(kv_specs)


def coll_of(e_spec):
    return CollOfSpec(e_spec)


def and_(*specs):
    return AndSpec(specs)


def tuple_(*e_specs):
    return TupleSpec(e_specs)


def nilable(subspec):
    return NilableSpec(subspec)


def explain(spec, x):
    return list(_explain(spec, x, original_x=x, trace=[]))


def _explain(spec, x, original_x, trace):
    if x is None:
        if isinstance(spec, NilableSpec):
            return
        else:
            yield Explanation(x, spec, 'is None', original_x, trace)
    elif isinstance(spec, PredSpec):
        if not spec(x):
            yield Explanation(x, spec, 'pred failed', original_x, trace)
    elif isinstance(spec, KeysSpec):
        if not isinstance(x, t.Mapping):
            yield Explanation(x, spec, 'not a Mapping', original_x, trace)
        for spec_key, val_spec in spec.key_specs.items():
            if spec_key not in x:
                yield Explanation(spec_key, spec, 'key missing', original_x, trace)
                continue
            yield from _explain(val_spec, x[spec_key], original_x, trace + [spec_key])
    elif isinstance(spec, CollOfSpec):
        if not isinstance(x, t.Collection):
            yield Explanation(x, spec, 'not a Collection', original_x, trace)
        for i, e in enumerate(x):
            yield from _explain(spec.e_spec, e, original_x, trace + [i])
    elif isinstance(spec, AndSpec):
        for s in spec.specs:
            yield from _explain(s, x, original_x, trace)
    elif isinstance(spec, TupleSpec):
        if not isinstance(x, t.Collection):
            yield Explanation(x, spec, 'is not a Collection', original_x, trace)
        if len(spec.e_specs) != len(x):
            yield Explanation(x, spec, 'invalid number of elements', original_x, trace)
        for i, (e_spec, e) in enumerate(zip(spec.e_specs, x)):
            yield from _explain(e_spec, e, original_x, trace + [i])
    elif spec != x:
        yield Explanation(x, spec, 'is not equal', original_x, trace)


def is_valid(spec, x):
    return [] == explain(spec, x)


def _make_instance_check(klass):
    return lambda x: isinstance(x, klass)


def is_string():
    return PredSpec(_make_instance_check(str))


def is_any():
    return PredSpec(lambda x: True)


def is_float():
    return PredSpec(_make_instance_check(float))


def is_int():
    return PredSpec(_make_instance_check(int))


