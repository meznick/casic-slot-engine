import json
from slot_machine import slot

sl = slot()

a = [[0,1],[0,2]]

b = [[0,1],[0,2],[0,3]]

print (a in b)

while(True):
    flag = input("Roll ?")
    if flag == "":
        sl.roll()
    else:
        break

with open("roll_output.json", 'w') as json_out:
    json_out.write(sl.roll())


a = ((0,1),(0,2),(0,3))

b = ((0,1),(0,2),(0,3))