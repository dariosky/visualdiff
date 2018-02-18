import inspect
import os
from pathlib import Path


def get_caller_path() -> Path:
    visual_diff_path = Path(__name__).resolve().parent.parent
    visual_diff_path_str = str(visual_diff_path)
    for caller in inspect.stack():
        caller_path = os.path.abspath(caller[1])
        if not caller_path.startswith(visual_diff_path_str):
            return Path(caller_path).parent
    else:
        return visual_diff_path
