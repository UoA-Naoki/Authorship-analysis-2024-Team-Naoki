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
        things=command.split()
    else:
        things=command.lower().split()
    num=len(things)
    if things[0]=="create":
        if num==3:
            action.create(things[1],things[2])
        elif num>3:
            items=[]
            for item in things[2:]:
                items.append(item)
            action.masscreate(things[1],items)
        else:
            print("No such action. Input help for command list.")
    elif things[0]=="retrieve":
        if num==1:
            action.showall()
        elif num==3:
            action.retrieve(things[1],things[2])
        else:
            print("No such action. Input help for command list.")
    elif things[0]=="update":
        if num==4:
            action.update(things[1],things[2],things[3])
        else:
            print("No such action. Input help for command list.")
    elif things[0]=="delete":
        if num==3:
            action.delete(things[1],things[2])
        elif num>3:
            items=[]
            for item in things[2:]:
                items.append(item)
            action.massdelete(things[1],items)
        else:
            print("No such action. Input help for command list.")
    elif things[0]=="quit":
        break
    elif things[0]=="help":
        action.help()
    else:
        print("No such action. Input help for command list.")
system.close()