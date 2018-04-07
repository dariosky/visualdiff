import asyncio

from visualdiff.core import VisualDiff


class DiffHelper():
    def __init__(self) -> None:
        super().__init__()
        self.vd = VisualDiff()

    def __call__(self, url: str, **kwargs):
        """
        A wrapper to easily automate diff-tests

        :param url: the url to retrieve to get a screenshot
        :keyword width: the screenshot width
        :keyword height: the screenshot height
        :return: None if there are no diff, otherwise a tuple with the area changed
        """
        loop = asyncio.get_event_loop()
        diff = loop.run_until_complete(
            self.vd.compare(url, **kwargs)
        )
        return diff


vd = DiffHelper()
