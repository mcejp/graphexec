from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class Result:
    outputs: Dict[str, Any]
    extra_outputs: Dict[str, Any]
