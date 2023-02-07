import json
from unittest import TestCase, main

from slot_machine import SlotMachine

CONFIG_PATH = 'tests/test_config.json'


class TestMachine(TestCase):
    def test_config_reading(self):
        slot = SlotMachine()
        with open(CONFIG_PATH, 'r') as cfg:
            config = json.loads(cfg.read())
        assert len(slot.matrix) == config['scale'][0]
        for i in slot.matrix:
            assert len(i) == config['scale'][1]

    def test_symbol_probability(self):
        pass

    def test_sybol_list(self):
        pass

    def test_matrix_on_roll_generation(self):
        pass

    def test_line_on_roll_filling(self):
        pass

    def test_duplicate_win_lines(self):
        pass


if __name__ == "__main__":
    main()
