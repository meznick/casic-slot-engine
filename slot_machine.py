import logging
import random
import json


class SlotMachine:
    instances = ()

    @classmethod
    def choose_available_instance(cls, instance_num=None):
        if instance_num:
            if cls.instances[instance_num].status == 'ready':
                return cls.instances[instance_num]
        for instance in cls.instances:
            if instance.status == 'ready':
                return instance

    @classmethod
    def add_instance(cls, new):
        cls.instances = cls.instances + (new,)

    def __init__(self, config_path=None, logger=None):
        if not config_path:
            return

        self.id = len(self.instances)
        SlotMachine.add_instance(self)
        self.status = 'ready'

        if logger:
            self.log = logger
        else:
            self._set_default_logger()

        self.config = self.read_config(config_path)
        #  creating a character matrix of the desired size
        self.matrix = [
            [Symbol('x')] * self.config["scale"][0]
            for i in range(self.config["scale"][1])
        ]
        #  calculation of the probability of a
        #  symbol falling out with a rarity of 1
        probability_coef = self.symbol_probability()
        #  getting a list of symbols and their parameters
        symbols_list = self.symbol_list(probability_coef)

        #  creating a list of slot symbols of class SlotMachine.Symbol
        self.symbols = list()
        for symbol in symbols_list:
            self.symbols.append(
                Symbol(
                    symbol["tag"],
                    symbol["multiplier"],
                    symbol["probability"],
                    symbol["range"],
                )
            )

        for symbol in self.symbols:
            symbol.print()
        # getting a list of slot lines based on a template from
        # the config minus lines that do not fit into the slot
        lines_ = self.lines_list()

        #  creating a list of slot lines
        self.lines = list()
        for line in lines_:
            symbols_ = list()
            for pos in line:
                symbols_.append(PlacedSymbol(pos))
            self.lines.append(symbols_)

        #  creating a list of multiplier coefficients by lines
        self.lines_multiplier = self.config["lines_multiplier"]
        #  extracting from the config the minimum number of replays by lines
        self.min_line = self.config["min_line"]
        #  creating a list of winning lines
        self.win_lines = list()

    def _set_default_logger(self):
        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.DEBUG)

    @staticmethod
    def _convert_to(number, base):
        digits = '0123456789abcdefghijklmnopqrstuvwxyz'
        result = ''
        while number > 0:
            result = digits[number % base] + result
            number //= base
        return result

    @classmethod
    def _str_representation(cls, value, base, repr_len):
        value = cls._convert_to(value, base)
        return '0' * (repr_len - len(str(value))) + str(value)

    def generate_all_combinations(self):
        n = self.config['scale'][0] * self.config['scale'][1]
        base = len(self.symbols)
        combination_num = 0
        while combination_num < len(self.symbols) ** n:
            self._str_representation(combination_num, base, n)
            yield [
                self.symbols[int(x)]
                for x in self._str_representation(combination_num, base, n)
            ]
            combination_num += 1

    def calculate_probability_and_rtp(self):
        rtp = 0
        total_prob = 0
        for comb in self.generate_all_combinations():
            lines = self.fill_lines_with_symbols(comb, self.win_positions, "1d")
            win_lines = self.pick_wining_lines(lines)
            prob = 0
            total_win = 0
            for line in win_lines:
                win_symbol = Symbol()
                for symbol in line:
                    win_symbol = symbol
                    if symbol.tag != " wild":
                        break
                total_win += (
                        win_symbol.multiplier *
                        self.lines_multiplier[str(len(line))]
                )
            if len(win_lines) != 0:
                prob = 1
                for pos_ in comb:
                    prob = prob * pos_.probability
            total_prob = total_prob + prob
            rtp = rtp + total_win * prob
        self.log.info("Theoretical chance to win(alt_place): " + str(total_prob))
        self.log.info("Theoretical RTP(alt_place): " + str(rtp))
        return total_prob, rtp

    @property
    def win_positions(self):
        # turning a list of slot lines into a
        # one-dimensional array of positions
        win_positions = list()
        for line in self.lines:
            line_ = list()
            for sym in line:
                line_.append(
                    PlacedSymbol(
                        sym.indexes[0] * self.config["scale"][0] +
                        sym.indexes[1] - 1
                    )
                )
            win_positions.append(line_)
        return win_positions

    def __str__(self):
        matrix = str()
        for string in self.matrix:
            for cell in string:
                matrix += "| " + str(cell) + " "
            matrix += "|\n"
        return matrix

    def print(self, matrix):
        out = ""
        for string in matrix:
            for cell in string:
                out += "| " + str(cell) + " "
            out += "|\n"
        print(out)

    def create_tag_matrix(self):
        """Creates a matrix filled with character tags to output to json."""
        tag_matrix = [
            ["x"] * self.config["scale"][0]
            for i in range(self.config["scale"][1])
        ]
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                tag_matrix[i][j] = str(self.matrix[i][j]).strip()
        return tag_matrix

    def print_win_matrix(self):
        """
        Prints a matrix to the console, where the performances are
        highlighted with caps.
        """
        tag_matrix = self.create_tag_matrix()
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                tag_matrix[i][j] = str(self.matrix[i][j])
        for line in self.win_lines:
            for symbol in line:
                tag_matrix[symbol.indexes[0]][symbol.indexes[1]] = tag_matrix[
                    symbol.indexes[0]
                ][symbol.indexes[1]].upper()
        matrix = ""
        for string in tag_matrix:
            for cell in string:
                matrix += "| " + str(cell) + " "
            matrix += "|\n"
        print(matrix)

    def symbol_probability(self):
        """calculates the probability of an event with a rarity of 1"""
        summ = 0
        for symbol in self.config["symbols"]:
            summ += 1 / symbol["rarity"]
        return 1 / summ

    def symbol_list(self, coef):
        """
        Creates a list of dictionaries with information about symbols
        (name, multiplier, probability of falling out, segment
        boundaries for random).
        """
        summ = 0
        symbols_ = list()
        for symbol in self.config["symbols"]:
            symbols_.append(
                {
                    "tag": symbol["tag"],
                    "multiplier": symbol["multiplier"],
                    "probability": coef / symbol["rarity"],
                    "range": summ,
                }
            )
            summ += coef / symbol["rarity"]
        return symbols_

    def lines_list(self):
        """
        Creates sets of indices corresponding to line types, removes unnecessary
        ones, returns as a list.
        """
        line_list = list()
        for _line in self.config["lines"]:
            for y in range(len(self.matrix)):
                line = [(y, 0)]
                x = 1
                for direction in _line[1:]:
                    if direction == "s":
                        y = y
                    elif direction == "d":
                        y = y + 1
                    elif direction == "u":
                        y = y - 1
                    line.append((y, x))
                    x = x + 1
                line_list.append(line)

        #  removal of lines that crawl out of the slot
        def remove_line(line):
            for pos in line:
                if (pos[0] < 0) or (pos[0] > self.config["scale"][1] - 1):
                    return False
            return True

        return list(filter(remove_line, line_list))

    @staticmethod
    def read_config(config_path):

        class ConfigEXception(Exception):
            pass

        with open(config_path) as conf:
            config = json.load(conf)
            max_line = max([len(l) for l in config['lines']])
            min_line = min([len(l) for l in config['lines']])

            if max_line != min_line:
                raise ConfigEXception('Varying line length!')

            if config['scale'][0] != max_line:
                raise ConfigEXception('Bad line lengths!')

            for line in config['lines']:
                h1 = len([1 for s in line if s == 'd']) + 1
                h2 = len([1 for s in line if s == 'u']) + 1
                max_line_height = max(h1, h2)
                if max_line_height > config['scale'][1]:
                    raise ConfigEXception(f'Too tall line! {line}')

        return config

    def generate_symbols(self):
        """
        In each of the cells of the slot matrix, we generate symbols according
        to their probabilities, returns the matrix of the slot instance.
        """
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                throw = random.uniform(0, 1)
                for k in range(len(self.symbols) - 1):
                    if (throw >= self.symbols[k].range) and (
                        throw <= self.symbols[k + 1].range
                    ):
                        self.matrix[i][j] = self.symbols[k]
                        break
                if throw >= self.symbols[len(self.symbols) - 1].range:
                    self.matrix[i][j] = self.symbols[len(self.symbols) - 1]
        return self.matrix

    def fill_lines_with_symbols(self, matrix=None, lines=None, line_type="2d"):
        """
        Populates a list of slot lines with characters
        based on a character matrix.
        """
        if matrix is None:
            matrix = self.matrix

        if lines is None:
            lines = self.lines

        for line in lines:
            for symbol in line:
                if line_type == "2d":
                    symbol.set_symbol(
                        matrix[symbol.indexes[0]][symbol.indexes[1]]
                    )

                if line_type == "1d":
                    symbol.set_symbol(matrix[symbol.indexes])

        return lines

    def pick_wining_lines(self, lines=None):
        """
        Chooses winning lines from the list of slots and removes
        unnecessary repetitions, shortens them,
        if necessary, creates a list of winning lines filled
        with symbols (class Placed_Symbol).
        """
        if lines is None:
            lines = self.lines

        win_lines = list()
        for line in lines:
            # each line can have multiple combos, but we should choose highest
            combination = list()
            # select first tag as target to compare
            combination.append(line[0])
            target_tag = combination[0].tag
            for s in line[1:]:
                if target_tag == 'wild':
                    target_tag = s.tag

                if s.tag in (target_tag, 'wild'):
                    combination.append(s)
                else:
                    break

            # filter too short lines
            if len(combination) >= self.min_line:
                win_lines.append(combination)

        if len(win_lines) > 1:
            # order win lines by descending multiplier
            win_lines.sort(
                key=lambda l: self.calculate_line_multiplier(l[0].multiplier, l),
                reverse=True
            )

        # remove lines except one having shared symbol
        if len(win_lines) > 1:
            cleared_win_lines = [win_lines[0]]
            for line in win_lines[1:]:
                check = True
                for symbol in line:
                    check = symbol.indexes not in [
                        s.indexes for wl in cleared_win_lines for s in wl
                    ]
                    if not check:
                        break
                if check:
                    cleared_win_lines.append(line)
        else:
            cleared_win_lines = win_lines


        return cleared_win_lines

    def output_json(self, win_lines):
        """
        Based on the system matrix and the set of winning lines,
        generates a JSON string for displaying information.
        """
        win_lines_out = list()
        for line in win_lines:
            symbol_info_ = list()
            indexes_ = list()
            for symbol in line:
                if symbol.tag == " wild":
                    symbol_info_ = [symbol.tag, symbol.multiplier]
                else:
                    symbol_info_ = [symbol.tag, symbol.multiplier]
                    break
            for symbol in line:
                indexes_.append([symbol.indexes[0], symbol.indexes[1]])
            win_lines_out.append(
                {
                    "indexes": indexes_,
                    "symbol": symbol_info_[0],
                    "multiplier": self.calculate_line_multiplier(symbol_info_[1], line),
                }
            )

        roll_output = {
            "matrix": self.create_tag_matrix(),
            "win_lines": win_lines_out
        }
        return roll_output

    def calculate_line_multiplier(self, symbol_multiplier, line):
        return symbol_multiplier * self.lines_multiplier[str(len(line))]

    def roll(self):
        self.generate_symbols()
        return self.output_json(
            self.pick_wining_lines(
                self.fill_lines_with_symbols()
            )
        )


class Symbol:
    def __init__(self, tag="x", multiplier=1, probability=1, _range=1):
        self.tag = tag
        self.multiplier = multiplier
        self.probability = probability
        self.range = _range

    def print(self):
        print(f"{self.tag}, {self.probability}, {self.range}")

    def __str__(self):
        return str(self.tag)


class PlacedSymbol(Symbol):
    def __init__(self, indexes, tag="x", multiplier=1, probability=1, _range=1):
        super().__init__(tag, multiplier, probability, _range)
        self.indexes = indexes

    def set_symbol(self, symbol: Symbol):
        self.tag = symbol.tag
        self.multiplier = symbol.multiplier
        self.probability = symbol.probability
        self.range = symbol.range

    def __str__(self):
        return str(self.indexes) + ", " + str(self.tag)

    def __eq__(self, other):
        return (
            other is not None
            and self.tag == other.tag
            and self.indexes == other.indexes
        )
