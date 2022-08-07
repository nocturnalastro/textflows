from __future__ import annotations
from dataclasses import KW_ONLY, dataclass, field
from pdb import set_trace
from ..registry import ParserRegisitries, registries
from .. import exceptions
from typing import Optional


class ConditionArg:
    @classmethod
    def parse(cls, registries: ParserRegisitries, definition: dict) -> SubFlowResult:
        return cls(**definition)


@dataclass
class Condition:
    name: str
    check: str
    args: list[ConditionArg]

    @classmethod
    def parse(cls, registries: ParserRegisitries, definition: dict) -> SubFlowResult:
        return cls(
            **(
                definition
                | dict(
                    args=[
                        registries.condition_args.parse(registries, arg)
                        for arg in definition.get("args", [])
                    ]
                )
            )
        )


@dataclass
class SubFlowResultPart:
    destination: str


@dataclass
class SubFlowResult:
    destination: str
    parts: list[SubFlowResultPart]

    @classmethod
    def parse(cls, registries: ParserRegisitries, definition: dict) -> SubFlowResult:
        return cls(
            **(
                definition
                | dict(
                    parts=[
                        registries.subflow_result_parts.parse(registries, part)
                        for part in definition.get("parts", [])
                    ]
                )
            )
        )


@dataclass
class Task:
    _: KW_ONLY
    type: str
    execute_when: list[str] = field(default_factory=list)

    def get_conditions(self):
        yield from self.execute_when


@registries.subflows.register
@dataclass
class SubFlow:
    _: KW_ONLY
    name: str
    tasks: list[Task]
    result: Optional[SubFlowResult] = None
    execute_when: Optional[list[str]] = None

    def get_conditions(self):
        if self.execute_when is not None:
            yield from self.execute_when

        for task in self.tasks:
            yield from task.get_conditions()

    @classmethod
    def parse(cls, registries: ParserRegisitries, definition: dict) -> SubFlow:

        result = None
        if result_definition := definition.get("result", None):
            result = SubFlowResult.parse(registries, result_definition)

        return cls(
            **(
                definition
                | dict(
                    result=result,
                    tasks=[
                        registries.tasks.parse(registries, task)
                        for task in definition.get("tasks", [])
                    ],
                )
            )
        )


@registries.mainflows.register
@dataclass
class Flow:
    entry_point: str
    flows: dict[str, SubFlow]
    conditions: dict[str, Condition]
    inital_state: dict
    meta: dict

    def __post_init__(self):
        if self.flows.get(self.entry_point) is None:
            raise exceptions.InvalidEntrypoint(
                f"{self.entry_point} not found in flows section"
            )

        if missing_conitions := (
            {
                c for f in self.flows.values() for c in f.get_conditions()
            }  # used conditions
            - self.conditions.keys()
        ):
            raise exceptions.MissingConditions(f"{', '.join(iter(missing_conitions))}")

    @classmethod
    def parse(cls, registries: ParserRegisitries, definition: dict) -> Flow:
        parsed_subflows = {}
        for subflow in definition.get("flows", exceptions.MissingSubflows):
            parsed = registries.subflows.parse(registries, subflow)
            parsed_subflows[parsed.name] = parsed

        parsed_conditions = {}
        for condition in definition.get("conditions", exceptions.MissingConditions):
            parsed = Condition.parse(registries, condition)
            parsed_conditions[parsed.name] = parsed

        return cls(
            **(definition | dict(flows=parsed_subflows, conditions=parsed_conditions))
        )
