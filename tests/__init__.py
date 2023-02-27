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
    [
        [
            MockSymbol('king', 4, (0, 0)),
            MockSymbol('ace', 4, (0, 1)),
            MockSymbol('wild', 10,(0, 2)),
            MockSymbol('10', 1,(0, 3)),
            MockSymbol('10', 1,(0, 4)),
        ],
        [
            MockSymbol('jack', 2, (1, 0)),
            MockSymbol('jack', 2, (1, 1)),
            MockSymbol('jack', 2, (1, 2)),
            MockSymbol('wild', 2, (1, 3)),
            MockSymbol('jack', 10, (1, 4)),
        ],
        [
            MockSymbol('10', 1, (2, 0)),
            MockSymbol('jack', 2, (2, 1)),
            MockSymbol('wild', 10, (2, 2)),
            MockSymbol('ace', 4, (2, 3)),
            MockSymbol('wild', 10, (2, 4)),
        ],
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
    ],
    [
        ['jack', 'jack', 'jack', 'wild', 'jack']
    ],
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
    'tests/good_config_4.json'
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
    [
        [
            MockSymbol('king', 4, (0, 0)),
            MockSymbol('ace', 4, (0, 1)),
            MockSymbol('wild', 10, (0, 2)),
            MockSymbol('10', 1, (0, 3)),
            MockSymbol('10', 1, (0, 4)),
        ],
        [
            MockSymbol('jack', 2, (1, 0)),
            MockSymbol('jack', 2, (1, 1)),
            MockSymbol('jack', 2, (1, 2)),
            MockSymbol('wild', 2, (1, 3)),
            MockSymbol('jack', 10, (1, 4)),
        ],
        [
            MockSymbol('10', 1, (2, 0)),
            MockSymbol('jack', 2, (2, 1)),
            MockSymbol('wild', 10, (2, 2)),
            MockSymbol('ace', 4, (2, 3)),
            MockSymbol('wild', 10, (2, 4)),
        ],
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
    [
        ['king', 'ace', 'wild', '10', '10'],
        ['jack', 'jack', 'jack', 'wild', 'jack'],
        ['10', 'jack', 'wild', 'ace', 'wild'],
        ['king', 'ace', 'jack', 'wild', 'jack'],
        ['jack', 'jack', 'wild', 'ace', 'wild'],
        ['jack', 'jack', 'wild', '10', '10'],
        ['10', 'jack', 'jack', 'wild', 'jack'],
        ['king', 'ace', 'wild', 'wild', 'jack'],
        ['jack', 'jack', 'jack', 'ace', 'wild'],
        ['jack', 'jack', 'jack', '10', '10'],
        ['10', 'jack', 'wild', 'wild', 'jack'],
    ]
]

ROLL_INPUT_MATRICES = [
    [
        [
            MockSymbol('king', 4, (0, 0)),
            MockSymbol('10', 1, (0, 1)),
            MockSymbol('jack', 2, (0, 2)),
            MockSymbol('queen', 3, (0, 3)),
            MockSymbol('queen', 3, (0, 4)),
        ],
        [
            MockSymbol('king', 4, (1, 0)),
            MockSymbol('king', 4, (1, 1)),
            MockSymbol('jack', 2, (1, 2)),
            MockSymbol('10', 1, (1, 3)),
            MockSymbol('queen', 3, (1, 4)),
        ],
        [
            MockSymbol('king', 4, (2, 0)),
            MockSymbol('queen', 3, (2, 1)),
            MockSymbol('wild', 10, (2, 2)),
            MockSymbol('jack', 2, (2, 3)),
            MockSymbol('jack', 2, (2, 4)),
        ]
    ],
    [
        [
            MockSymbol('jack', 2, (0, 0)),
            MockSymbol('ace', 5, (0, 1)),
            MockSymbol('jack', 2, (0, 2)),
            MockSymbol('jack', 2, (0, 3)),
            MockSymbol('jack', 2, (0, 4)),
        ],
        [
            MockSymbol('jack', 2, (1, 0)),
            MockSymbol('jack', 2, (1, 1)),
            MockSymbol('jack', 2, (1, 2)),
            MockSymbol('jack', 2, (1, 3)),
            MockSymbol('10', 1, (1, 4)),
        ],
        [
            MockSymbol('queen', 3, (2, 0)),
            MockSymbol('10', 1, (2, 1)),
            MockSymbol('jack', 2, (2, 2)),
            MockSymbol('jack', 2, (2, 3)),
            MockSymbol('ace', 5, (2, 4)),
        ],
    ],
    [
        [
            MockSymbol('ace', 5, (0, 0)),
            MockSymbol('queen', 3, (0, 1)),
            MockSymbol('10', 1, (0, 2)),
            MockSymbol('wild', 10, (0, 3)),
            MockSymbol('ace', 5, (0, 4)),
        ],
        [
            MockSymbol('king', 4, (1, 0)),
            MockSymbol('wild', 10, (1, 1)),
            MockSymbol('king', 4, (1, 2)),
            MockSymbol('king', 4, (1, 3)),
            MockSymbol('10', 1, (1, 4)),
        ],
        [
            MockSymbol('10', 1, (2, 0)),
            MockSymbol('jack', 2, (2, 1)),
            MockSymbol('jack', 2, (2, 2)),
            MockSymbol('queen', 3, (2, 3)),
            MockSymbol('queen', 3, (2, 4)),
        ],
    ]
]

ROLL_TARGET_WIN_LINES = [
    [
        [(1, 0), (1, 1), (2, 2)]
    ],
    [
        [(1, 0), (1, 1), (0, 2), (0, 3), (0, 4)]
    ],
    [
        [(1, 0), (1, 1), (1, 2), (1, 3)]    # last element can also be (0, 3)
    ]
]

OUTPUT_WIN_LINES = [
    [
        [
            MockSymbol('king', 4, (1, 0)),
            MockSymbol('king', 4, (1, 1)),
            MockSymbol('wild', 10, (2, 2)),
        ],
    ],
]

OUTPUT_TARGET_WIN_LINES = [
    [
        [[1, 0], [1, 1], [2, 2]],
    ],
]
