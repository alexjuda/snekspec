import pprint

import snekspec.core as s
import snekspec.wiadro as wiadro


def _spec():
    rating_spec = s.is_float()
    good_rating_spec = s.and_(rating_spec,
                              s.PredSpec(lambda x: x > 0.6))
    return s.keys({'first': s.is_any(),
                   'last': s.is_string(),
                   'ratings': s.coll_of(good_rating_spec),
                   'career_span': s.tuple_(s.is_int(), s.is_int())})


def main():
    spec = _spec()
    gen = s.gen(spec)
    for _ in range(10):
        pprint.pprint(s.generate(gen))

    print('ssssss')


if __name__ == '__main__':
    main()
