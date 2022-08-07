from dataclasses import dataclass
from typing import Optional
from .basic import SubFlow, Condition
from ..registry import registries


class ForLoopDefintion:
    source: str
    count_var: Optional[str]  # if count var is set then it will be placed in count_var


class WhileLoopDefintion:
    condition: Condition
    count_var: Optional[str]  # if count var is set then it will be placed in count_var


@registries.subflows.register
@dataclass
class LoopSubFlow(SubFlow):
    loop: ForLoopDefintion | WhileLoopDefintion
