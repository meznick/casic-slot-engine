import random
import json
from itertools import groupby
from decimal import Decimal

class SlotMachine:
    def __init__(self, config_path):
        self.config = self.read_config(config_path)
        self.matrix = [["x"]*self.config["scale"][0] for i in range(self.config["scale"][1])] #создание матрицы символов нужного размера
        probability_coef = self.symbol_probability() #расчет веротяности выпадения сивола с редкостью 1
        symbols_list = self.symbol_list(probability_coef) #получение списка символов и их параметров
        
        #создание списка символов слота класса SlotMachine.Symbol
        self.symbols = list()
        for symbol in symbols_list:
            self.symbols.append(self.Symbol(symbol["tag"],symbol["multiplier"],symbol["probability"],symbol["range"]))
        for symbol in self.symbols:
            symbol.print()
        lines_ = self.lines_list() #получение списка линий слота на основе шаблона из конфига за вычетом линий, не влезающих в слот
        
        #создание списка линий слота класса SlotMachine.Line
        self.lines = list()
        for line in lines_:
            symbols_ = list()
            for pos in line:
                symbols_.append(self.Line.Symbol([pos[0],pos[1]],None))
            self.lines.append(self.Line(symbols_))
        
        self.lines_multiplier = self.config["lines_multiplier"] #создание списка коэффицентов множителей по линиям
        self.min_line = self.config["min_line"] #извлечение из конфига минимального числа сыгровок по линиям
        self.win_lines = list()
        #self.RTP_calculator()
    
    def RTP_calculator(self):
        pos = list()
        for i in range(self.config["scale"][1]):
            for j in range(self.config["scale"][0]):
                pos.append(self.symbols[0])
        global RTP 
        global total_prob
        global overall
        global unique
        overall = 0
        unique = 0
        def alt_place(n,i=1,sequence = []):
            print(i) 
            #for pos in sequence:
            #    print(pos)
            print(len(sequence))
            if i > n:
                return sequence
            else:
                new_sequence = list()
                if len(sequence) == 0:
                    for symbol in self.symbols:
                        new_sequence.append([symbol])
                    return alt_place(n,i+1,new_sequence)
                else:
                    for symbol in self.symbols:
                        for pos in sequence:
                            comb = list()
                            comb.append(symbol)
                            for sym in pos:
                                comb.append(sym)
                            new_sequence.append(comb)
                    return alt_place(n,i+1,new_sequence)
        
        comb_list = alt_place(self.config["scale"][1]*self.config["scale"][0])

        win_positions = list()
        for line in self.lines:
            line_ = list()
            for sym in line.symbols:
                line_.append(self.Line.Symbol(sym.indexes[0]*self.config["scale"][0]+sym.indexes[1],None))
            win_positions.append(self.Line(line_))
        for pos_ in win_positions:
            print(pos_)
        
        RTP = Decimal(0)
        total_prob = Decimal(0)        
        for comb in comb_list:
            self.win_lines = list()
            for line_ in win_positions:
                for sym_ in line_.symbols:
                    sym_.symbol = comb[sym_.indexes]
            self.pick_wining_lines(win_positions)
            prob = Decimal(0)
            total_win = Decimal(0)
            for line in self.win_lines:
                win_symbol = self.Symbol()
                for symbol in line.symbols:
                    win_symbol = symbol
                    if symbol.symbol.tag != " wild":
                        break
                total_win = total_win + Decimal(win_symbol.symbol.multiplier)*Decimal(self.lines_multiplier[str(len(line.symbols))])
            if len(self.win_lines) != 0:
                prob = Decimal(1)
                for pos_ in comb:
                    prob = prob*Decimal(pos_.probability)
            total_prob = total_prob + prob
            RTP = RTP + total_win*prob
        print("Theoretical chance to win(alt_place): " + str(total_prob))
        print("Theoretical RTP(alt_place): " + str(RTP))                  
        
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
        """создает матрицу, заполненную тегами символов, для вывода в json"""
        tag_matrix = [["x"]*self.config["scale"][0] for i in range(self.config["scale"][1])]
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                tag_matrix[i][j] = str(self.matrix[i][j])
        return tag_matrix

    def print_win_matrix(self):
        """выводит в консоль матрицу, где сыгровки выделены капсом"""
        tag_matrix = self.create_tag_matrix()
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                tag_matrix[i][j] = str(self.matrix[i][j])
        for line in self.win_lines:
            for symbol in line.symbols:
                tag_matrix[symbol.indexes[0]][symbol.indexes[1]] = tag_matrix[symbol.indexes[0]][symbol.indexes[1]].upper()
        matrix = ""
        for string in tag_matrix:
            for cell in string:
                matrix += "| " + str(cell) + " "
            matrix += "|\n"
        print(matrix)
    
    def symbol_probability(self):
        """рассчитывает вероятность события с редкостью 1"""
        summ = 0
        for symbol in self.config["symbols"]: 
            summ += 1/symbol["rarity"]
        return 1/summ

    def symbol_list(self, coef):
        """создает список словарей с информацией о сиволах (название, множитель, вероятность выпадения, границы отрезка для рандома)"""
        summ = 0
        symbols_ = list()
        for symbol in self.config["symbols"]:            
            symbols_.append({"tag":symbol["tag"], "multiplier":symbol["multiplier"], "probability":coef / symbol["rarity"],"range": summ})
            summ += coef/symbol["rarity"]
        return symbols_

    def lines_list(self):
        """создает наборы индексов, соответствующих типам линий, убирает лишние, возвращает в виде списка"""
        line_list = list()
        for lin in self.config["lines"]:
            for i in range(len(self.matrix)):
                line = list()
                line.append([i,0])
                k = 1
                l = i
                for dir in lin:
                    if dir == "s":
                        l = l
                    elif dir == "d":
                        l = l + 1
                    elif dir == "u":
                        l = l - 1
                    line.append([l,k])
                    k = k + 1
                line_list.append(line)
        blacklist = list()
        for i in range(len(line_list)):
            for pos in line_list[i]:
                if pos[0] < 0 or pos[0] > self.config["scale"][1]-1:
                    blacklist.append(i)
                    break
        lines_ = list()
        for i in range(len(line_list)):
            if i not in blacklist:
                lines_.append(line_list[i])
        return lines_

    def read_config(self, config_path):
        with open(config_path) as conf:
            return json.load(conf) #подсос джысына
    
    def generate_symbols(self):
        """в каждой из ячеек матрицы слота генерируем символы согласно их вероятностям, возвращает матрицу экземпляра слота"""
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                throw = random.uniform(0,1)

                for k in range(len(self.symbols)-1):
                    if (throw >= self.symbols[k].range) and (throw <= self.symbols[k+1].range):
                        self.matrix[i][j] = self.symbols[k]
                        break
                if throw >= self.symbols[len(self.symbols)-1].range:
                    self.matrix[i][j] = self.symbols[len(self.symbols)-1]
        return self.matrix

    def fill_lines_with_symbols(self, matrix = None, lines = None):
        """заполняет список линий слота символами на основе матрицы символов"""
        if matrix == None:
            matrix = self.matrix
        if lines == None:
            lines = self.lines
        for line in lines:
            for pos in line.symbols:
                pos.symbol = matrix[pos.indexes[0]][pos.indexes[1]]
        return lines

    def pick_wining_lines(self, lines = None):
        """выбирает из списка линий слота выигрышные и убирает ненужные повторы, укорачивает их, 
        если нужно, создает список self.win_lines класса Line, возвращает его"""
        if lines == None:
            lines = self.lines
        win_lines = list()
        for line in lines:
            line_ = self.Line([])
            line_.symbols.append(line.symbols[0])
            for i in range(1,len(line.symbols)):
                check = False
                if line.symbols[i-1].symbol.tag == " wild":
                    if line.symbols[i].symbol.tag == " wild":
                        check = True
                    else:
                        check = True
                        k = 0
                        while (k < i):
                            if (line.symbols[k].symbol.tag != line.symbols[i].symbol.tag) and (line.symbols[k].symbol.tag != " wild"):
                                check = False
                                break
                            k = k + 1
                else:
                    if (line.symbols[i].symbol.tag == line.symbols[i-1].symbol.tag) or (line.symbols[i].symbol.tag == " wild"):
                        check = True
                if check:
                    line_.symbols.append(line.symbols[i])
                else:
                    break
            if len(line_.symbols) >= self.min_line:
                win_lines.append(line_)
        
        #удаление ненужных линий (повторы, одна линия уже содержится в другой):
        blacklist = list()
        for i in range(len(win_lines)):
            for k in range(len(win_lines)):
                if i != k:    
                    if len(win_lines[i].symbols) <= len(win_lines[k].symbols):
                        if (win_lines[i].symbols == win_lines[k].symbols[:len(win_lines[i].symbols)]):
                            blacklist.append(i)
        lines_out = list()
        for i in range(len(win_lines)):
            if i not in blacklist:
                lines_out.append(win_lines[i])
        
        self.win_lines = lines_out
        return self.win_lines

    def output_json(self):
        """на основе матрицы системи и набора выигравших линий формирует JSON-строку для вывода информации"""
        win_lines_out = list()
        for line in self.win_lines:
            symbol_info_ = list()
            indexes_ = list()
            for symbol in line.symbols:
                if symbol.symbol.tag == " wild":
                    symbol_info_ = [symbol.symbol.tag,symbol.symbol.multiplier]
                else:
                    symbol_info_ = [symbol.symbol.tag,symbol.symbol.multiplier]
                    break
            for symbol in line.symbols:
                indexes_.append([symbol.indexes[0],symbol.indexes[1]])
            win_lines_out.append({"indexes":indexes_,"symbol":symbol_info_[0],"multiplier":symbol_info_[1]*self.lines_multiplier[str(len(line.symbols))]})

        roll_output = {
            "matrix": self.create_tag_matrix(),
            "win_lines": win_lines_out
            }
        return json.dumps(roll_output)

    def roll(self, debug = True):  
        self.win_lines = list() #очищаем список выигравших линий
        self.generate_symbols()
        self.fill_lines_with_symbols()
        self.pick_wining_lines()
        if debug:
            self.print_win_matrix()
        
        output = self.output_json()
        if debug:
            for win_line in json.loads(output)["win_lines"]:
                print(win_line)
        
        return output


    class Symbol:
        def __init__(self, tag = "x", multiplier = 1, probability = 1, _range = 1):
            self.tag = tag
            self.multiplier = multiplier
            self.probability = probability
            self.range = _range
        
        def __eq__(self,other):
            return other is not None and self.tag == other.tag

        def print(self):
            print(f'{self.tag}, {self.probability}, {self.range}')
    
        def __str__(self):
            return str(self.tag)

    class Line:
        def __init__(self,symbols):
            self.symbols = symbols
        
        class Symbol:
            def __init__(self,indexes,symbol):
                self.indexes = indexes
                self.symbol = symbol
            def __eq__(self,other):
                return self.indexes == other.indexes and self.symbol.tag == other.symbol.tag

        def __str__(self):
            string = ""
            for symbol in self.symbols:
                tag = ""
                if symbol.symbol != None:
                    tag = str(symbol.symbol.tag)
                string = string + str(symbol.indexes) + ", tag: " + tag + "; "
            return string

