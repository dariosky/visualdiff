import inspect
import logging
import os
import re
from pathlib import Path

logger = logging.getLogger('visualdiff.paths')


def get_caller_path(callers_ago=1) -> Path:
    selected_caller = inspect.stack()[callers_ago]
    caller_path = os.path.abspath(selected_caller[1])
    return Path(caller_path).parent


def default_master_path(url: str) -> Path:
    result = Path("visualdiff_masters")
    safe_url = re.sub('[^0-9a-zA-Z]', '_', url)
    result /= safe_url + ".png"
    logger.debug(f"URL: {url} => {result}")
    return result


def absolute_master_path(url, master_path, callers_ago=1):
    if isinstance(master_path, str):
        master_path = Path(master_path)
    if master_path is None:
        master_path = default_master_path(url)
    if not master_path.is_absolute():
        master_path = get_caller_path(callers_ago=callers_ago + 1) / master_path
    return master_path
