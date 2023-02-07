import json
from slot_machine import SlotMachine

CONFIG_PATH = 'tests/test_config.json'
OUTPUT_PATH = 'tests/roll_output.json'

sl = SlotMachine(CONFIG_PATH)


while(True):
    flag = input("Roll ?")
    if flag == "":
        roll = json.loads(sl.roll())
        #for win_lines in roll["win_lines"]:
        win = 0
        for win_line in roll["win_lines"]:
            win = win+win_line["multiplier"]
            print(win_line)
        if win != 0:
            print("You won " + str(win) + "! Congratulations!")
        else:
            print("Better luck next time!")
    else:
        break


with open(OUTPUT_PATH, 'w') as json_out:
    json_out.write(sl.roll())



a = ((0,1),(0,2),(0,3))

b = ((0,1),(0,2),(0,3))