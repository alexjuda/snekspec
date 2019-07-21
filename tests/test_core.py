import snekspec.core as s


def _spec():
    rating_spec = s.is_float
    good_rating_spec = s.and_(rating_spec,
                              lambda x: x > 0.6)
    return s.keys({'first': s.is_any,
                   'last': s.is_string,
                   'ratings': s.coll_of(good_rating_spec),
                   'career_span': s.tuple_(s.is_int, s.is_int)})


def test_valid_obj():
    obj = {'first': 'Kamaal',
           'last': 'Fareed',
           'ratings': [0.9, 0.7, 0.9],
           'career_span': (1990, 2019)}
    assert s.is_valid(_spec(), obj)
    assert [] == s.explain(_spec(), obj)


def test_missing_keys():
    obj = {'first': 'Q-Tip'}
    assert not s.is_valid(_spec(), obj)
    assert [] != s.explain(_spec(), obj)


def test_invalid_value():
    obj = {'first': 'KRS',
           'last': 1,
           'ratings': [0.8, 0.7, 0.9]}
    assert not s.is_valid(_spec(), obj)
    assert [] != s.explain(_spec(), obj)


def test_invalid_tuple_value():
    obj = {'first': 'Kamaal',
           'last': 'Fareed',
           'ratings': [0.9, 0.7, 0.9],
           'career_span': (1990, '*')}
    assert not s.is_valid(_spec(), obj)
    assert [] != s.explain(_spec(), obj)


def test_invalid_tuple_size():
    obj = {'first': 'Kamaal',
           'last': 'Fareed',
           'ratings': [0.9, 0.7, 0.9],
           'career_span': (1990, )}
    assert not s.is_valid(_spec(), obj)
    assert [] != s.explain(_spec(), obj)


def test_invalid_nested_value():
    obj = {'first': 'KRS',
           'last': '1',
           'ratings': [0.99, 0.7, 0.8, 0.5]}
    assert not s.is_valid(_spec(), obj)
    assert [] != s.explain(_spec(), obj)


def test_invalid_none():
    obj = None
    assert not s.is_valid(_spec(), obj)
    assert [] != s.explain(_spec(), obj)


def test_none_with_nilable():
    obj = None
    spec = s.nilable(_spec())
    assert s.is_valid(spec, obj)
    assert [] == s.explain(spec, obj)
