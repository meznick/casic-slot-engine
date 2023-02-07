import json
from slot_machine import slot

sl = slot()


while(True):
    flag = input("Roll ?")
    if flag == "":
        roll = json.loads(sl.roll())
        #for win_lines in roll["win_lines"]:
        win = 0
        for win_line in roll["win_lines"]:
            win = win+win_line["multiplyer"]
        if win != 0:
            print("You won " + str(win) + "! Congratulations!")
        else:
            print("Better luck next time!")
    else:
        break


with open("roll_output.json", 'w') as json_out:
    json_out.write(sl.roll())



a = ((0,1),(0,2),(0,3))

b = ((0,1),(0,2),(0,3))