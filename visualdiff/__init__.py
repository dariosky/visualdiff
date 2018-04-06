import asyncio

from visualdiff.core import VisualDiff


class DiffHelper():

    def __init__(self) -> None:
        super().__init__()
        self.vd = VisualDiff()

    def __call__(self, url: str, **kwargs):
        loop = asyncio.get_event_loop()
        diff = loop.run_until_complete(
            self.vd.compare(url, **kwargs)
        )
        return diff


vd = DiffHelper()
