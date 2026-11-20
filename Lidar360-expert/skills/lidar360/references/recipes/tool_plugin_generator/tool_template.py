from typing import Callable, Dict, List, Any, Optional, Tuple
import json


def execute(input: dict, progress_callback: Callable[[float, str], bool]) -> Tuple[int, dict, str]:
    """
    {{DESCRIPTION_ZH}}
    """
    try:
        {{INPUT_PARAMS}}

        {{PROCESSING_STEPS}}

        return 0, {{RESULT_DICT}}, ""
    except Exception as e:
        return 1, {}, str(e)
