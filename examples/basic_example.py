import logging

from visualdiff import vd

if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger('visualdiff').setLevel(logging.DEBUG)

    assert not vd('http://example.com')
