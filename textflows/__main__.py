from . import core
from . import parser

parser.Parser().parse(
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
            }
        ],
        "entry_point": "init",
        "inital_state": {},
        "meta": {},
    },
    loader=lambda x: x,
)
