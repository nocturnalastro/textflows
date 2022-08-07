import json
from typing import Any
from . import registries


class Parser:
    def __init__(self, registries=registries):
        self.registries = registries

    def parse(self, definition: Any, loader=json.loads):
        loaded_definition: dict = loader(definition)
        return registries.mainflows.parse(self.registries, loaded_definition)
