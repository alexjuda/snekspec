import pprint

import snekspec.core as s
import wiadro


def main():
    rating_spec = s.is_float
    good_rating_spec = s.and_(rating_spec,
                              lambda x: x > 0.6)
    spec = s.keys({'first': s.is_any,
                   'last': s.is_string,
                   'ratings': s.coll_of(good_rating_spec),
                   'career_span': s.tuple_(s.is_int, s.is_int)})

    objs = [{'first': 'Kamaal',
             'last': 'Fareed',
             'ratings': [0.9, 0.7, 0.9],
             'career_span': (1990, 2019)},
            {'first': 'Kamaal',
             'last': 'Fareed',
             'ratings': [0.9, 0.7, 0.9],
             'career_span': (1990, '*')},
            {'first': 'Kamaal',
             'last': 'Fareed',
             'ratings': [0.9, 0.7, 0.9],
             'career_span': (1990, )},
            {'first': 'Q-Tip'},
            {'first': 'KRS',
             'last': 1,
             'ratings': [0.8, 0.7, 0.9]},
            {'first': 'KRS',
             'last': '1',
             'ratings': [0.99, 0.7, 0.8, 0.5]}]

    # wiadro.dump(objs, 'objs')
    wiadro.dump_all(locals())

    for i, o in enumerate(objs):
        print(f'obj {i} explanation')
        pprint.pprint(s.explain(spec, o))
    print('ssssss')


if __name__ == '__main__':
    main()
