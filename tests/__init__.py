import pytest

from slot_machine import SlotMachine

GOOD_CONFIG_PATH = 'tests/good_config.json'
BAD_CONFIG_PATH = 'tests/bad_config.json'


@pytest.fixture()
def slot():
    return SlotMachine(GOOD_CONFIG_PATH)
