import pytest

from slot_machine import SlotMachine, PlacedSymbol

GOOD_CONFIG_PATH = 'tests/good_config.json'


@pytest.fixture()
def slot():
    return SlotMachine(GOOD_CONFIG_PATH)


class MockSymbol(PlacedSymbol):
    def __init__(self, tag: str, multiplier=1, indexes: tuple = (0, 0)):
        super().__init__(indexes, tag, multiplier, 1, 1)


PICKING_WIN_LINES_TEST_MATRICES = [
    [
        [
            MockSymbol('10'),
            MockSymbol('10'),
            MockSymbol('jack'),
            MockSymbol('10'),
        ],
        [
            MockSymbol('wild'),
            MockSymbol('10'),
            MockSymbol('jack'),
            MockSymbol('10'),
        ],
        [
            MockSymbol('10'),
            MockSymbol('10'),
            MockSymbol('10'),
            MockSymbol('10'),
        ],
        [
            MockSymbol('10'),
            MockSymbol('wild'),
            MockSymbol('10'),
            MockSymbol('10'),
        ],
        [
            MockSymbol('jack'),
            MockSymbol('10'),
            MockSymbol('10'),
            MockSymbol('10'),
        ]
    ],
    [
        [
            MockSymbol('10', 1),
            MockSymbol('10', 1),
            MockSymbol('10', 1),
            MockSymbol('jack', 2),
            MockSymbol('king', 3),
            MockSymbol('king', 3),
            MockSymbol('king', 3),
        ],
        [
            MockSymbol('ace', 4),
            MockSymbol('ace', 4),
            MockSymbol('ace', 4),
            MockSymbol('jack', 2),
            MockSymbol('king', 3),
            MockSymbol('king', 3),
            MockSymbol('king', 3),
        ],
        [
            MockSymbol('10', 1),
            MockSymbol('jack', 2),
            MockSymbol('10', 1),
            MockSymbol('10', 1),
            MockSymbol('10', 1),
            MockSymbol('10', 1),
            MockSymbol('jack', 2),
        ],
    ],
    [
        [
            MockSymbol('10', 1, (0, 0)),
            MockSymbol('10', 1, (0, 1)),
            MockSymbol('10', 1, (0, 2)),
            MockSymbol('10', 1, (0, 3)),
        ],
        [
            MockSymbol('10', 1, (1, 0)),
            MockSymbol('jack', 2, (1, 1)),
            MockSymbol('10', 1, (1, 2)),
            MockSymbol('10', 1, (1, 3)),
        ],
        [
            MockSymbol('10', 1, (2, 0)),
            MockSymbol('king', 3, (2, 1)),
            MockSymbol('10', 1, (2, 2)),
            MockSymbol('10', 1, (2, 3)),
        ]
    ]
]

PICKING_WIN_LINES_TARGET_WIN_LINES = [
    [
        ['10', '10', '10', '10'],
        ['10', 'wild', '10', '10'],
        ['10', '10', '10']
    ],
    [
        ['king', 'king', 'king'],
        ['ace', 'ace', 'ace'],
        ['10', '10', '10', '10']
    ],
    [
        ['10', '10', '10', '10']
    ]
]

PICKING_WIN_LINES_CONFIGS = [
    'tests/good_config.json',
    'tests/good_config_2.json',
    'tests/good_config_3.json'
]

FILLING_LINES_TEST_MATRIX = [[
    MockSymbol('10'),
    MockSymbol('10'),
    MockSymbol('jack'),
    MockSymbol('10'),
]]
