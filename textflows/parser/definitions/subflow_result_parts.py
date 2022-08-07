from dataclasses import dataclass
from typing import Any
from .basic import SubFlowResultPart
from ..registry import registries


@registries.subflow_result_parts.register
@dataclass
class ValueSubFlowResultPart(SubFlowResultPart):
    value: Any


@registries.subflow_result_parts.register
@dataclass
class SourceSubFlowResultPart(SubFlowResultPart):
    source: str
