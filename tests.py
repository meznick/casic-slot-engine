import json
from slot_machine import slot

sl = slot()

while(True):
    flag = input("Roll ?")
    if flag == "":
        sl.roll()
    else:
        break

with open("roll_output.json", 'w') as json_out:
    json_out.write(sl.roll())
