from visualdiff import vd


class TestVisualDifferences:

    def test_didnt_change(self):
        assert not vd('http://example.com',
                      master_path='visualdiff_masters/example_same.png')

    def test_did_change(self):
        assert vd('http://example.com',
                  master_path='visualdiff_masters/example_changed.png')
