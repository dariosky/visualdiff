import inspect
import os
from pathlib import Path


def get_caller_path(callers_ago=1) -> Path:
    visual_diff_path = Path(__name__).resolve().parent.parent
    visual_diff_path_str = str(visual_diff_path)
    selected_caller = inspect.stack()[callers_ago]
    caller_path = os.path.abspath(selected_caller[1])
    return Path(caller_path).parent
