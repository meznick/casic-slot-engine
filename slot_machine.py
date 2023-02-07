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

    def create_tag_matrix(self):
        tag_matrix = [["x"]*(len(self.matrix)) for i in range(len(self.matrix[0]))]
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                tag_matrix[i][j] = str(self.matrix[i][j])
        return tag_matrix

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
        
        print(self)
        slot_lines = list()
        #заполнение линий символами со слота
        for line in self.lines:
            line_ = list()
            for pos in line.indexes:
                line_.append([pos[0],pos[1],self.matrix[pos[0]][pos[1]]])
            slot_lines.append(line_)
        
        win_lines = list()
        for line in slot_lines:
            line_ = list()
            line_.append(line[0])
            for i in range(1,len(line)):
                check = False
                if line[i-1][2].tag == " wild":
                    if line[i][2].tag == " wild":
                        check = True
                    else:
                        k = 0
                        while (k < i-1):
                            if (line[k][2].tag == line[i][2].tag) or (line[k][2].tag == " wild"):
                                check = True
                            else:
                                check = False
                                break
                            k = k + 1
                else:
                    if (line[i][2].tag == line[i-1][2].tag) or (line[i][2].tag == " wild"):
                        check = True
                if check:
                    line_.append(line[i])
                else:
                    break
            if len(line_) >= 3:
                win_lines.append(line_)
        
        #удаление ненужных линий (повторы, одна линия уже содержится в другой):
        blacklist = list()
        for i in range(len(win_lines)):
            for k in range(len(win_lines)):
                if i != k:    
                    if len(win_lines[i]) <= len(win_lines[k]):
                        if (win_lines[i] == win_lines[k][:len(win_lines[i])]):
                            blacklist.append(i)
        
        lines_out = list()
        for i in range(len(win_lines)):
            if i not in blacklist:
                lines_ = list()
                symbols_ = list()
                for pos in win_lines[i]:
                    lines_.append([pos[0],pos[1]])
                    symbols_.append(pos[2])
                #win_lines.append([winning_lines[i][0],self.matrix[winning_lines[i][0][0][0]][winning_lines[i][0][0][1]].tag, self.lines_multiplyer[str(count)]+self.matrix[winning_lines[i][0][0][0]][winning_lines[i][0][0][1]].multiplyer])
                win_symbol = list()
                for symbol in symbols_:
                    if symbol.tag == " wild":
                        win_symbol = [symbol.tag,len(win_lines[i])+symbol.multiplyer]
                    else:
                        win_symbol = [symbol.tag,len(win_lines[i])+symbol.multiplyer]
                        break
                    
                lines_out.append([lines_] + win_symbol)

        print(lines_out)

        roll_output = {
            "matrix": self.create_tag_matrix(),
            "win_lines": lines_out
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



