from textflows.parser import Parser
import json


def test_parser():
    Parser().parse(
        {
            "conditions": [
                {
                    "name": "checkme",
                    "check": "is_true",
                    "args": [{"value": True}],
                }
            ],
            "flows": [
                {
                    "name": "init",
                    "tasks": [
                        {
                            "type": "update_state",
                            "source": "source",
                            "destination": "dest",
                        }
                    ],
                },
            ],
            "entry_point": "init",
            "inital_state": {
                "source": 1,
            },
            "meta": {},
        },
        loader=lambda x: x,
    )
