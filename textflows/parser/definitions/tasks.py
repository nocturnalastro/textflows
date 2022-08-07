from __future__ import annotations
from dataclasses import KW_ONLY, dataclass, field
from .. import registries
from .basic import Task
from ..registry import ParserRegisitries


@registries.tasks.register
@dataclass
class UpdateStateTask(Task):
    _: KW_ONLY  # Have to use kw_only otherwise get non-default after default error
    source: str
    destination: str
    type: str = "update_state"

    def __post_init__(self):
        self.type = "update_state"

    @classmethod
    def parse(cls, registries: ParserRegisitries, definition: dict) -> UpdateStateTask:
        if definition.get("type", "update_state") != "update_state":
            raise Exception("Incorrect type")
        return cls(**definition)


class ScreenElements(Task):
    type: str


@registries.tasks.register
@dataclass
class Screen(Task):
    _: KW_ONLY
    elements: list[ScreenElements] = field(default_factory=list)
    type: str = "screen"

    def __post_init__(self):
        self.type = "screen"
