import snekspec.core as s

import hypothesis.strategies as hst
import hypothesis as h


def _spec():
    rating_spec = s.is_float()
    good_rating_spec = s.and_(rating_spec,
                              s.PredSpec(lambda x: x > 0.6))
    return s.keys({'first': s.is_any(),
                   'last': s.is_string(),
                   'ratings': s.coll_of(good_rating_spec),
                   'career_span': s.tuple_(s.is_int(), s.is_int())})


class TestExamples:
    def test_valid_obj(self):
        obj = {'first': 'Kamaal',
               'last': 'Fareed',
               'ratings': [0.9, 0.7, 0.9],
               'career_span': (1990, 2019)}
        assert [] == s.explain(_spec(), obj)
        assert s.is_valid(_spec(), obj)

    def test_missing_keys(self):
        obj = {'first': 'Q-Tip'}
        assert [] != s.explain(_spec(), obj)
        assert not s.is_valid(_spec(), obj)

    def test_invalid_value(self):
        obj = {'first': 'KRS',
               'last': 1,
               'ratings': [0.8, 0.7, 0.9]}
        assert [] != s.explain(_spec(), obj)
        assert not s.is_valid(_spec(), obj)

    def test_invalid_tuple_value(self):
        obj = {'first': 'Kamaal',
               'last': 'Fareed',
               'ratings': [0.9, 0.7, 0.9],
               'career_span': (1990, '*')}
        assert [] != s.explain(_spec(), obj)
        assert not s.is_valid(_spec(), obj)

    def test_invalid_tuple_size(self):
        obj = {'first': 'Kamaal',
               'last': 'Fareed',
               'ratings': [0.9, 0.7, 0.9],
               'career_span': (1990, )}
        assert [] != s.explain(_spec(), obj)
        assert not s.is_valid(_spec(), obj)

    def test_invalid_nested_value(self):
        obj = {'first': 'KRS',
               'last': '1',
               'ratings': [0.99, 0.7, 0.8, 0.5]}
        assert [] != s.explain(_spec(), obj)
        assert not s.is_valid(_spec(), obj)

    def test_invalid_none(self):
        obj = None
        assert [] != s.explain(_spec(), obj)
        assert not s.is_valid(_spec(), obj)

    def test_none_with_nilable(self):
        obj = None
        spec = s.nilable(_spec())
        assert [] == s.explain(spec, obj)
        assert s.is_valid(spec, obj)


class TestStrategyGeneratesValidValue:
    @h.settings(deadline=1000.0)
    @h.given(hst.data())
    def test_keys(self, data):
        spec = s.keys({'a': s.StringSpec(),
                       'b': s.NilableSpec(s.StringSpec())})
        val = data.draw(spec.strategy())
        assert s.is_valid(spec, val)

    # @h.settings(deadline=1000.0)
    @h.given(hst.data())
    def test_coll_of(self, data):
        spec = s.coll_of(s.NilableSpec(s.StringSpec()))
        val = data.draw(spec.strategy())
        assert s.is_valid(spec, val)
