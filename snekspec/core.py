import typing as t
import collections as c

import hypothesis
import hypothesis.strategies as hst


class PredSpec:
    def __init__(self, f):
        self.f = f

    def explain(self, x, orig_x, trace):
        if not self.f(x):
            yield Explanation(x, self, 'pred failed', orig_x, trace)

    def strategy(self):
        return hst.none()


class KeysSpec:
    def __init__(self, key_specs: t.Mapping, st_kwargs={}):
        self.key_specs = key_specs
        self.st_kwargs = st_kwargs

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

    def strategy(self):
        return hst.fixed_dictionaries({k: s.strategy() for k, s in self.key_specs.items()},
                                      **self.st_kwargs)


class CollOfSpec:
    def __init__(self, element_spec, st_kwargs={}):
        self.element_spec = element_spec
        self.st_kwargs = st_kwargs

    def explain(self, x, orig_x, trace):
        if not isinstance(x, t.Collection):
            yield Explanation(x, self, 'Not a Collection', orig_x, trace)
        for i, e in enumerate(x):
            yield from self.element_spec.explain(e, orig_x, trace + [i])

    def strategy(self):
        return hst.lists(self.element_spec.strategy(), **self.st_kwargs)


class AndSpec:
    def __init__(self, specs):
        self.specs = specs

    def explain(self, x, orig_x, trace):
        for spec in self.specs:
            yield from spec.explain(x, orig_x, trace)

    def strategy(self):
        generative, *discriminative = self.specs
        result = generative.strategy()
        for spec in discriminative:
            result = result.filter(lambda x: is_valid(spec, x))
        return result


class TupleSpec:
    def __init__(self, element_specs):
        self.element_specs = element_specs

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

    def strategy(self):
        return hst.tuples(*(s.strategy() for s in self.element_specs))


class NilableSpec:
    def __init__(self, subspec):
        self.subspec = subspec

    def explain(self, x, orig_x, trace):
        if x is None:
            # return []
            return
        else:
            yield from self.subspec.explain(x, orig_x, trace)

    def strategy(self):
        return hst.one_of(hst.none(),
                          self.subspec.strategy())


class TypeSpec:
    def __init__(self, type_, strategy):
        self.type_ = type_
        self.strategy_ = strategy

    def explain(self, x, orig_x, trace):
        if not isinstance(x, self.type_):
            yield Explanation(x, self, 'invalid type', orig_x, trace)

    def strategy(self):
        return self.strategy_


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


def _make_instance_check(klass):
    return lambda x: isinstance(x, klass)


def is_string(st_kwargs={}):
    return TypeSpec(str, hst.text(**st_kwargs))


def is_any():
    return PredSpec(lambda x: True)


def is_float(st_kwargs={}):
    return TypeSpec(float, hst.floats(**st_kwargs))


def is_int(st_kwargs={}):
    return TypeSpec(int, hst.integers(**st_kwargs))


def explain(spec, x):
    return list(spec.explain(x, orig_x=x, trace=[]))


def is_valid(spec, x):
    return [] == explain(spec, x)


def gen(spec):
    return spec.strategy()


def generate(spec_gen):
    return spec_gen.example()
