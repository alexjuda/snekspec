import collections as c
import typing as t
import hypothesis
import hypothesis.strategies as hst


class PredSpec:
    def __init__(self, f):
        self.f = f

    def explain(self, x, orig_x, trace):
        if not self.f(x):
            yield Explanation(x, self, 'pred failed', orig_x, trace)


class KeysSpec(c.namedtuple('_KeysSpec', ['key_specs'])):
    def explain(self, x, orig_x, trace):
        if isinstance(x, t.Mapping):
            for key, val_spec in self.key_specs.items():
                try:
                    val = x[key]
                except KeyError:
                    yield Explanation(key, self, 'key missing', orig_x, trace)
                    continue
                yield from val_spec.explain(val, orig_x, trace + [key])
        else:
            yield Explanation(x, self, 'Not a Mapping', orig_x, trace)


class CollOfSpec(c.namedtuple('_CollOfSpec', ['element_spec'])):
    def explain(self, x, orig_x, trace):
        if not isinstance(x, t.Collection):
            yield Explanation(x, self, 'Not a Collection', orig_x, trace)
        for i, e in enumerate(x):
            yield from self.element_spec.explain(e, orig_x, trace + [i])


class AndSpec (c.namedtuple('_AndSpec', ['specs'])):
    def explain(self, x, orig_x, trace):
        for spec in self.specs:
            yield from spec.explain(x, orig_x, trace)


class TupleSpec(c.namedtuple('_TupleSpec', ['element_specs'])):
    def explain(self, x, orig_x, trace):
        if not isinstance(x, t.Collection):
            yield Explanation(x, self, 'is not a Collection', orig_x, trace)
        if len(self.element_specs) != len(x):
            yield Explanation(x,
                              self,
                              'Invalid number of elements. Expected {}, got {}'.format(len(self.element_specs),
                                                                                       len(x)),
                              orig_x,
                              trace)
        for i, (e_spec, e) in enumerate(zip(self.element_specs, x)):
            yield from e_spec.explain(e, orig_x, trace + [i])


class NilableSpec:
    def __init__(self, subspec):
        self.subspec = subspec

    def explain(self, x, orig_x, trace):
        if x is None:
            # return []
            return
        else:
            yield from self.subspec.explain(x, orig_x, trace)


class StringSpec:
    def __init__(self, st_kwargs={}):
        self.st_kwargs = st_kwargs

    def explain(self, x, orig_x, trace):
        if not isinstance(x, str):
            yield Explanation(x, self, 'invalid type', orig_x, trace)

    def strategy(self):
        return hst.text(**self.st_kwargs)


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
    return list(_explain(spec, x, orig_x=x, trace=[]))


def _explain(spec, x, orig_x, trace):
    yield from spec.explain(x, orig_x, trace)
    # if x is None:
    #     if isinstance(spec, NilableSpec):
    #         return
    #     else:
    #         yield Explanation(x, spec, 'is None', orig_x, trace)
    # elif isinstance(spec, PredSpec):
    #     if not spec(x):
    #         yield Explanation(x, spec, 'pred failed', orig_x, trace)
    # elif isinstance(spec, StringSpec):
    #     if not isinstance(x, str):
    #         yield Explanation(x, spec, 'invalid type', orig_x, trace)
    # elif isinstance(spec, KeysSpec):
    #     if not isinstance(x, t.Mapping):
    #         yield Explanation(x, spec, 'not a Mapping', orig_x, trace)
    #     for spec_key, val_spec in spec.key_specs.items():
    #         if spec_key not in x:
    #             yield Explanation(spec_key, spec, 'key missing', orig_x, trace)
    #             continue
    #         yield from _explain(val_spec, x[spec_key], orig_x, trace + [spec_key])
    # elif isinstance(spec, CollOfSpec):
    #     if not isinstance(x, t.Collection):
    #         yield Explanation(x, spec, 'not a Collection', orig_x, trace)
    #     for i, e in enumerate(x):
    #         yield from _explain(spec.e_spec, e, orig_x, trace + [i])
    # elif isinstance(spec, AndSpec):
    #     for s in spec.specs:
    #         yield from _explain(s, x, orig_x, trace)
    # elif isinstance(spec, TupleSpec):
    #     if not isinstance(x, t.Collection):
    #         yield Explanation(x, spec, 'is not a Collection', orig_x, trace)
    #     if len(spec.e_specs) != len(x):
    #         yield Explanation(x, spec, 'invalid number of elements', orig_x, trace)
    #     for i, (e_spec, e) in enumerate(zip(spec.e_specs, x)):
    #         yield from _explain(e_spec, e, orig_x, trace + [i])
    # elif spec != x:
    #     yield Explanation(x, spec, 'is not equal', orig_x, trace)


def is_valid(spec, x):
    return [] == explain(spec, x)


def _make_instance_check(klass):
    return lambda x: isinstance(x, klass)


def is_string():
    return StringSpec()


def is_any():
    return PredSpec(lambda x: True)


def is_float():
    return PredSpec(_make_instance_check(float))


def is_int():
    return PredSpec(_make_instance_check(int))


def strategy(spec):
    if isinstance(spec, PredSpec):
        # TODO
        return hst.just(None)
    elif isinstance(spec, StringSpec):
        return hst.text()
    elif isinstance(spec, KeysSpec):
        return hst.fixed_dictionaries({k: strategy(val_spec)
                                       for k, val_spec in spec.key_specs.items()})
