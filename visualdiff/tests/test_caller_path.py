from visualdiff.caller_path import get_caller_path


def test_caller_path():
    """ Check that test_caller_paths return the path of the calling script
        all internal callers in the visualdiff should be ignored
    """
    assert get_caller_path()
