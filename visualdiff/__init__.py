import asyncio
import logging

from visualdiff.core import VisualDiff

logger = logging.getLogger("visualdiff.helper")


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
