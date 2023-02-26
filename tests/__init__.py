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
            MockSymbol('wild'),
            MockSymbol('10'),
        ]
    ],
    [
        [
            MockSymbol('wild'),
            MockSymbol('wild'),
            MockSymbol('10'),
            MockSymbol('10'),
        ],
    ],
    [
        [
            MockSymbol('10'),
            MockSymbol('10'),
            MockSymbol('10'),
            MockSymbol('10'),
        ],
    ],
    [
        [
            MockSymbol('10'),
            MockSymbol('wild'),
            MockSymbol('10'),
            MockSymbol('10'),
        ],
    ],
    [
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
    ],
    [
        [
            MockSymbol('ace', 4),
            MockSymbol('ace', 4),
            MockSymbol('ace', 4),
            MockSymbol('jack', 2),
            MockSymbol('king', 3),
            MockSymbol('king', 3),
            MockSymbol('king', 3),
        ],
    ],
    [
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
            MockSymbol('wild'),
            MockSymbol('wild'),
            MockSymbol('wild'),
            MockSymbol('wild'),
        ]
    ],
]

PICKING_WIN_LINES_TARGET_WIN_LINES = [
    [
        ['10', '10', 'wild', '10']
    ],
    [
        ['wild', 'wild', '10', '10'],
    ],
    [
        ['10', '10', '10', '10'],
    ],
    [
        ['10', 'wild', '10', '10'],
    ],
    [
    ],
    [
        ['10', '10', '10'],
    ],
    [
        ['ace', 'ace', 'ace'],
    ],
    [
    ],
    [
        ['wild', 'wild', 'wild', 'wild']
    ]
]

PICKING_WIN_LINES_CONFIGS = [
    'tests/good_config.json',
    'tests/good_config.json',
    'tests/good_config.json',
    'tests/good_config.json',
    'tests/good_config.json',
    'tests/good_config_2.json',
    'tests/good_config_2.json',
    'tests/good_config_2.json',
    'tests/good_config.json',
]

FILLING_LINES_TEST_MATRICES = [
    [
        [
            MockSymbol('10'),
            MockSymbol('ace'),
            MockSymbol('jack'),
            MockSymbol('king'),
            MockSymbol('wild')
        ],
        [
            MockSymbol('ace'),
            MockSymbol('ace'),
            MockSymbol('10'),
            MockSymbol('wild'),
            MockSymbol('ace')
        ],
        [
            MockSymbol('10'),
            MockSymbol('king'),
            MockSymbol('ace'),
            MockSymbol('10'),
            MockSymbol('ace')
        ]
    ],
    [
        [
            MockSymbol('ace', 5, (0, 0)),
            MockSymbol('jack', 1, (0, 1)),
            MockSymbol('jack', 1, (0, 2)),
            MockSymbol('10', 1, (0, 3)),
            MockSymbol('10', 1, (0, 4)),
        ],
        [
            MockSymbol('10', 1, (1, 0)),
            MockSymbol('10', 1, (1, 1)),
            MockSymbol('10', 1, (1, 2)),
            MockSymbol('10', 1, (1, 3)),
            MockSymbol('ace', 5, (1, 4)),
        ],
        [
            MockSymbol('ace', 5, (2, 0)),
            MockSymbol('10', 1, (2, 1)),
            MockSymbol('king', 3, (2, 2)),
            MockSymbol('10', 1, (2, 3)),
            MockSymbol('10', 1, (2, 4)),
        ]
    ],
]

FILLING_LINES_TARGET_LINES = [
    [
        ['10', 'ace', 'jack', 'king', 'wild'],
        ['ace', 'ace', '10', 'wild', 'ace'],
        ['10', 'king', 'ace', '10', 'ace'],
        ['10', 'ace', '10', 'wild', 'ace'],
        ['ace', 'ace', 'ace', '10', 'ace'],
        ['ace', 'ace', 'jack', 'king', 'wild'],
        ['10', 'king', '10', 'wild', 'ace'],
        ['10', 'ace', 'jack', 'wild', 'ace'],
        ['ace', 'ace', '10', '10', 'ace'],
        ['ace', 'ace', '10', 'king', 'wild'],
        ['10', 'king', 'ace', 'wild', 'ace'],
    ],
    [
        ['ace', 'jack', 'jack', '10', '10'],
        ['10', '10', '10', '10', 'ace'],
        ['ace', '10', 'king', '10', '10'],
        ['ace', 'jack', '10', '10', 'ace'],
        ['10', '10', 'king', '10', '10'],
        ['10', '10', 'jack', '10', '10'],
        ['ace', '10', '10', '10', 'ace'],
        ['ace', 'jack', 'jack', '10', 'ace'],
        ['10', '10', '10', '10', '10'],
        ['10', '10', '10', '10', '10'],
        ['ace', '10', 'king', '10', 'ace'],
    ],
]
