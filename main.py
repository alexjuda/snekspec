import pprint

import snekspec.core as s
import snekspec.wiadro as wiadro


def _spec():
    return s.keys({'first': s.is_any(),
                   'last': s.is_string()})


def main():
    spec = _spec()
    st = spec.strategy()
    pprint.pprint(st)
    for _ in range(10):
        pprint.pprint(st.example())

    print('ssssss')


if __name__ == '__main__':
    main()
