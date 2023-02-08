from asyncio.windows_events import NULL
import random
import json


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
        
        lines_ = self.lines_list() #получение списка линий слота на основе шаблона из конфига за вычетом линий, не влезающих в слот
        
        #создание списка линий слота класса SlotMachine.Line
        self.lines = list()
        for line in lines_:
            symbols_ = list()
            for pos in line:
                symbols_.append(self.Line.Symbol([pos[0],pos[1]],NULL))
            self.lines.append(self.Line(symbols_))
        
        self.lines_multiplier = self.config["lines_multiplier"] #создание списка коэффицентов множителей по линиям
        self.min_line = self.config["min_line"] #извлечение из конфига минимального числа сыгровок по линиям
        self.win_lines = list()

    def __str__(self):
        matrix = str()
        for string in self.matrix:
            for cell in string:
                matrix += "| " + str(cell) + " "
            matrix += "|\n"
        return matrix

    def create_tag_matrix(self):
        """создает матрицу, заполненную тегами символов, для вывода в json"""
        tag_matrix = [["x"]*self.config["scale"][0] for i in range(self.config["scale"][1])]
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                tag_matrix[i][j] = str(self.matrix[i][j])
        return tag_matrix

    
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

        #for line in line_list:
        #    for pos in line:
        #        if pos[0] < 0 or pos[0] > config["scale"][1]-1:
        #           line_list.remove(line)
        #           break
        #for line in line_list:
        #    print(line)

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

    def fill_lines_with_symbols(self):
        """заполняет список линий слота символами на основе матрицы символов"""
        for line in self.lines:
            for pos in line.symbols:
                pos.symbol = self.matrix[pos.indexes[0]][pos.indexes[1]]
        return self.lines

    def pick_wining_lines(self):
        """выбирает из списка линий слота выигрышные и убирает ненужные повторы, укорачивает их, 
        если нужно, создает список self.win_lines класса Line, возвращает его"""
        win_lines = list()
        for line in self.lines:
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
                        while (k < i-1):
                            if (line.symbols[k].symbol.tag != line.symbols[i].symbol.tag) or (line.symbols[k].symbol.tag != " wild"):
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

    def roll(self):
        self.win_lines = list() #очищаем список выигравших линий
        self.generate_symbols()
        self.fill_lines_with_symbols()
        self.pick_wining_lines()
        self.print_win_matrix()
        
        output = self.output_json()
        for win_line in json.loads(output)["win_lines"]:
            print(win_line)
        return output


    class Symbol:
        def __init__(self, tag, multiplier, probability, _range):
            self.tag = tag
            self.multiplier = multiplier
            self.probability = probability
            self.range = _range
        
        def print(self):
            return f'{self.tag}, {self.probability}, {self.range}'
    
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
                if symbol.symbol != NULL:
                    tag = str(symbol.symbol.tag)
                string = string + str(symbol.indexes[0]) +", " + str(symbol.indexes[1]) + ", " + tag + ";"
            return string

