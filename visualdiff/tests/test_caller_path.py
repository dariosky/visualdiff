from pathlib import Path

from visualdiff.caller_path import get_caller_path


class TestCallerPath:
    this_script_path = Path(__file__).resolve().parent

    def test_default(self):
        """ Check that test_caller_paths return the path of the calling script
            all internal callers in the visualdiff should be ignored
        """
        assert get_caller_path() == self.this_script_path

    def test_zero(self):
        # when going zero back, it's the get_caller_path itself
        assert get_caller_path(0) == self.this_script_path.parent
