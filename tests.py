import json
from slot_machine import slot

sl = slot()

while(True):
    flag = input("Roll ?")
    if flag == "":
        sl.roll()
    else:
        break
