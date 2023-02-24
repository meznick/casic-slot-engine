import json
from unittest import TestCase, main

import pytest
from . import slot, GOOD_CONFIG_PATH, BAD_CONFIG_PATH  # noqa: F401

from slot_machine import SlotMachine, PlacedSymbol


class MockSymbol(PlacedSymbol):
    def __init__(self, tag):
        super().__init__(tag, 1, 1, 1)


class TestMachine(TestCase):
    @pytest.fixture(autouse=True)
    def _slot(self, slot):
        self.slot = slot

    def test_config_reading(self):
        assert self.slot.status == 'ready'
        with open(GOOD_CONFIG_PATH, 'r') as cfg:
            config = json.loads(cfg.read())
        assert len(self.slot.matrix) == config['scale'][1]
        for i in self.slot.matrix:
            assert len(i) == config['scale'][0]

    def test_symbol_probability(self):
        stp, symbols = self._get_symbol_theoretical_probs()
        checksum = sum([
            stp[k]
            for k
            in stp.keys()
        ])
        with self.subTest('Checking if total probability is 1'):
            self.assertGreaterEqual(checksum, 0.999)
            self.assertGreaterEqual(1.001, checksum)
        results = 0
        # sd = symbol drops
        sd = {s['tag']: 0 for s in symbols}
        max_results = 20000000
        # generate enough rolls to calculate real probabilities
        while results < max_results:
            roll_result = self.slot.roll()['matrix']
            flatten_result = [
                symbol for line in roll_result for symbol in line
            ]
            results += len(flatten_result)
            # collect drops per symbol
            for symbol in sd.keys():
                sd[symbol] += (
                    len([1 for s in flatten_result if s == symbol.strip()])
                )
        checksum = sum([
            sd[k] for k in sd.keys()
        ])
        assert max_results - 15 <= checksum <= max_results + 15
        for symbol in stp.keys():
            with self.subTest(
                    msg='Testing real symbol probability.',
                    symbol=symbol
            ):
                sq_err = (
                    (sd[symbol] / checksum - stp[symbol]) / stp[symbol]
                ) ** 2
                self.assertLess(sq_err, 0.1 ** 6)

    @staticmethod
    def _get_symbol_theoretical_probs():
        with open(GOOD_CONFIG_PATH, 'r') as cfg:
            symbols = json.loads(cfg.read())['symbols']
        # How to calculate actual probability:
        # x = sum(min_rarity / rarity)
        # symbol probability = min_rarity / (rarity * x)
        min_rarity = min([s['multiplier'] for s in symbols])
        x = sum([min_rarity / s['rarity'] for s in symbols])
        # stp = symbol theoretical probabilities
        stp = {
            s['tag']: min_rarity / (s['rarity'] * x) for s in symbols
        }
        return stp, symbols

    def test_symbol_list(self):
        stp, symbols = self._get_symbol_theoretical_probs()
        # testing all the symbols has correct probability
        for symbol in self.slot.symbols:
            with self.subTest('Testing symbol from list.', symbol=symbol):
                self.assertIn(symbol.tag, [s['tag'] for s in symbols])
                self.assertEqual(symbol.probability, stp[symbol.tag])

        # checking all the sybols from config were collected
        for tag in [s['tag'] for s in symbols]:
            self.assertIn(tag, [s.tag for s in self.slot.symbols])

    def test_matrix_on_roll_generation(self):
        pass

    def test_line_on_roll_filling(self):
        pass

    def test_duplicate_win_lines(self):
        pass

    def test_combination_generation(self):
        combination_target = (
                len(self.slot.symbols) ** (
                    self.slot.config['scale'][0] *
                    self.slot.config['scale'][1]
            )
        )
        combinations = len([c for c in self.slot.generate_all_combinations()])
        with self.subTest('Testing combinations amount'):
            self.assertEqual(combinations, combination_target)

    def test_win_positions(self):
        n = self.slot.config['scale'][0] * self.slot.config['scale'][1]
        for list in self.slot.win_positions:
            for symbol in list:
                self.assertLess(symbol.indexes, n)

    def test_filling_lines(self):
        matrix = [[
            MockSymbol('10'),
            MockSymbol('10'),
            MockSymbol('jack'),
            MockSymbol('10'),
        ]]
        self.slot.fill_lines_with_symbols(matrix=matrix)
        self.assertEqual(
            [s.tag for s in matrix[0]],
            [s.tag for s in self.slot.lines[0]]
        )

    def test_rtp(self):
        _, control_rtp = self.slot.calculate_probability_and_rtp()
        spend = 0
        win = 0
        while spend < 100000:
            spend += 1
            roll_result = self.slot.roll()
            import pdb; pdb.set_trace()
            for line in roll_result['win_lines']:
                win += line['multiplier']
        rtp = win / spend
        self.assertEqual(rtp, control_rtp)


if __name__ == "__main__":
    main()
