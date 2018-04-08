import asyncio
from pathlib import Path
from typing import Union

from visualdiff.core import VisualDiff
from visualdiff.paths import absolute_master_path


class DiffHelper():
    def __init__(self) -> None:
        super().__init__()
        self.vd = VisualDiff()

    def __call__(self, url: str, master_path: Union[str, Path],
                 **kwargs):
        """
        A wrapper to easily automate diff-tests

        :param url: the url to retrieve to get a screenshot
        :param master_path: the url (if not absolute, it's relative to the caller file)
        :keyword width: the screenshot width
        :keyword height: the screenshot height
        :keyword master_should_exist: bool
        :return: None if there are no diff, otherwise a tuple with the area changed

        :type master_should_exist:bool
        """
        loop = asyncio.get_event_loop()
        master_path = absolute_master_path(url, master_path, callers_ago=2)
        diff = loop.run_until_complete(
            self.vd.compare(url,
                            master_path=master_path,
                            **kwargs)
        )
        return diff


vd = DiffHelper()
