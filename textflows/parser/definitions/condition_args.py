from dataclasses import dataclass
from typing import Any
from .basic import ConditionArg
from .. import registries


@registries.condition_args.register
@dataclass
class ValueConditionArg(ConditionArg):
    value: Any


@registries.condition_args.register
@dataclass
class SourceCoditionArg(ConditionArg):
    source: str
