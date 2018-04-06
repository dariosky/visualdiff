import os

from visualdiff import vd

base_master_path = os.path.abspath(os.path.dirname(__file__))

iphone_description = {
    'name': 'iPhone 5',
    'userAgent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) '
                 'AppleWebKit/601.1.46 (KHTML, like Gecko)'
                 ' Version/9.0 Mobile/13B143 Safari/601.1',
    'viewport': {
        'width': 320,
        'height': 568,
        'deviceScaleFactor': 2,
        'isMobile': True,
        'hasTouch': True,
        'isLandscape': False
    }
}


class TestEmulation:
    def test_iphone6(self):
        assert not vd('http://example.com',
                      master_path=os.path.join(
                          base_master_path,
                          'visualdiff_masters/same_iphone5.png'
                      ),
                      emulate=iphone_description)
