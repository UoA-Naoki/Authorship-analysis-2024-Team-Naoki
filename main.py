from src import system
from src import action
from src import file

system.init()
while True:
    print()
    try:
        command=input("Action?> ")
    except EOFError:
        system.close()
    file.existancecheck()
    if system.casesensitive:
        item=command.split()
    else:
        item=command.lower().split()
    num=len(item)
    if item[0]=="create":
        if num==3:
            action.create(item[1],item[2])
        else:
            print("No such action. Input help for command list.")
    elif item[0]=="retrieve":
        if num==1:
            action.showall()
        elif num==3:
            action.retrieve(item[1],item[2])
        else:
            print("No such action. Input help for command list.")
    elif item[0]=="update":
        if num==4:
            action.update(item[1],item[2],item[3])
        else:
            print("No such action. Input help for command list.")
    elif item[0]=="delete":
        if num==3:
            action.delete(item[1],item[2])
        else:
            print("No such action. Input help for command list.")
    elif item[0]=="quit":
        break
    elif item[0]=="help":
        action.help()
    else:
        print("No such action. Input help for command list.")
system.close()