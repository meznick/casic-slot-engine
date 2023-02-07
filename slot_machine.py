import random
import json

config_path = "config.json"

class slot:
    def __init__(self):
        self.read_config()
        print(self)
        for symbol in self.symbols:
            print(symbol.print())
        for line in self.lines:
            print(line)
        print("Amount of lines:" + str(len(self.lines)))

    def __str__(self):
        matrix = str()
        for string in self.matrix:
            for cell in string:
                matrix += "| " + str(cell) + " "
            matrix += "|\n"
        return matrix

    def read_config(self):
        with open(config_path) as conf:
            config = json.load(conf) #подсос джысына
            self.matrix = [["x"]*config["scale"][0] for i in range(config["scale"][1])] #инициализация матрицы символов нужного размера
            
            #расчет коэффициента вероятностей на основе редкости
            summ = 0
            for symbol in config["symbols"]: 
                summ += 1/symbol["rarity"]
            x = 1/summ;

            self.symbols = list() #инициализация списка символов класса symbol
            
            #заполнение списка символов на основе данных конфига
            summ = 0
            for symbol in config["symbols"]:            
                self.symbols.append(self.symbol(symbol["tag"], symbol["multiplyer"], x/symbol["rarity"], summ))
                summ += x/symbol["rarity"]

            self.lines = list() #инициализация списка линий класса line
            
            #процедура отбора подходящих линий из конфига и их иницализация в виде списка индексов матрицы
            line_list = list()
            for lin in config["lines"]:
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
                    if pos[0] < 0 or pos[0] > config["scale"][1]-1:
                        blacklist.append(i)
                        break
            for i in range(len(line_list)):
                if i not in blacklist:
                    self.lines.append(self.line(line_list[i]))
            
            self.lines_multiplyer = config["lines_multiplyer"] #подсос из конфига параметров мультпиликатора количества символов в линии
    
    def roll(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                throw = random.uniform(0,1)

                for k in range(len(self.symbols)-1):
                    if (throw >= self.symbols[k].range) and (throw <= self.symbols[k+1].range):
                        self.matrix[i][j] = self.symbols[k]
                        break
                if throw >= self.symbols[len(self.symbols)-1].range:
                    self.matrix[i][j] = self.symbols[len(self.symbols)-1]
        winning_lines = list()
        win_lines = list()
        past_lines_signature = list()
        for line in self.lines:
            count = 1
            current_line = list()
            current_line.append([line.indexes[0][0],line.indexes[0][1]])
            current_line_signature = str(line.indexes[0][0])+str(line.indexes[0][0])
            for i in range(1,len(line.indexes)):

                if self.matrix[line.indexes[i-1][0]][line.indexes[i-1][1]].tag == self.matrix[line.indexes[i][0]][line.indexes[i][1]].tag:
                    count = count + 1
                    current_line.append([line.indexes[i][0],line.indexes[i][1]])
                    current_line_signature = current_line_signature + str(line.indexes[i][0])+str(line.indexes[i][0])
                else:
                    break
            if count >= 3:
                if current_line_signature not in past_lines_signature:
                    winning_lines.append([current_line,current_line_signature])
                past_lines_signature.append(current_line_signature)
        
        #удаление ненужных линий (повторы, одна линия уже содержится в другой):
        blacklist = list()
        for i in range(len(winning_lines)):
            for k in range(len(winning_lines)):
                if i != k:    
                    if winning_lines[i][1] in winning_lines[k][1]:
                        blacklist.append(i)
        for i in range(len(winning_lines)):
            if i not in blacklist:
                #win_lines.append([winning_lines[i][0],self.matrix[winning_lines[i][0][0][0]][winning_lines[i][0][0][1]].tag, self.lines_multiplyer[str(count)]+self.matrix[winning_lines[i][0][0][0]][winning_lines[i][0][0][1]].multiplyer])
                 win_lines.append([winning_lines[i][0],self.matrix[winning_lines[i][0][0][0]][winning_lines[i][0][0][1]].tag,self.matrix[winning_lines[i][0][0][0]][winning_lines[i][0][0][1]].multiplyer+self.lines_multiplyer[str(len(winning_lines[i][0]))]])
                
        print(self)
        #wining_lines.append([current_line,self.matrix[line.indexes[0][0]][line.indexes[0][1]].tag, self.lines_multiplyer[str(count)]+self.matrix[line.indexes[0][0]][line.indexes[0][1]].multiplyer])
        print(win_lines)

        roll_output = {
            "matrix": str(self),
            "win_lines": win_lines
            }
        return json.dumps(roll_output)

    class symbol:
        def __init__(self, tag, multiplyer, probability, _range):
            self.tag = tag
            self.multiplyer = multiplyer
            self.probability = probability
            self.range = _range
        
        def print(self):
            return str(self.tag) +", " + str(self.probability)+", " + str(self.range)
    
        def __str__(self):
            return str(self.tag)

    class line:
        def __init__(self, indexes):
            self.indexes = indexes
        def __str__ (self):
            return str(self.indexes)



