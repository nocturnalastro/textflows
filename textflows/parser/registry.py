from __future__ import annotations
from dataclasses import dataclass
import json
from ..core import Registry
from . import exceptions


class ParserRegistry(Registry):
    def parse(self, registries: ParserRegisitries, definition: dict):
        reasons = []
        for el_name in self._elements:
            try:
                el = getattr(self, el_name)
                return el.parse(registries, definition)
            except Exception as e:
                reasons.append(f"{el.__name__}: {str(e)}")
        else:
            raise exceptions.ParseFailed(
                f"Failed to parse: {json.dumps(definition, indent=2)}"
                "\n"
                f"for the following reasons: {','.join(r for r in reasons)}"
            )


class ParserRegisitries:
    mainflows = ParserRegistry("mainflows")
    subflows = ParserRegistry("subflows")
    tasks = ParserRegistry("tasks")
    subflow_result_parts = ParserRegistry("subflow_result_parts")
    condition_args = ParserRegistry("condition_args")
    screen_elements = ParserRegistry("screen_elements")


registries = ParserRegisitries()
